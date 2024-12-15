import openai
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request
from langdetect import detect, LangDetectException
from datetime import datetime

# Configuración de correo y seguimiento
ADMIN_EMAIL = "ing.gabriel.romero@gmail.com"
MAX_TOKENS = 1000000  # Ajusta este valor según tu límite
usage_count = 0
total_tokens = 0

app = Flask(__name__)

# Configurar clave de API
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_system_prompt(lang):
    prompts = {
        'es': """Eres un asistente experto en el cuidado de pollos y mascotas, especializado en proporcionar consejos prácticos y soluciones útiles en español.""",
        'en': """You are an expert assistant in chicken and pet care, specialized in providing practical advice and useful solutions in English.""",
        'fr': """Vous êtes un assistant expert en soins des poulets et des animaux de compagnie, spécialisé dans la fourniture de conseils pratiques et de solutions utiles en français.""",
        'pt': """Você é um assistente especialista em cuidados com galinhas e animais de estimação, especializado em fornecer conselhos práticos e soluções úteis em português."""
    }
    return prompts.get(lang, prompts['en'])
#-------------------------------
@app.route('/')
def home():
    history = []
    try:
        with open("log.txt", "r", encoding="utf-8") as file:
            content = file.read().split('-'*50)
            for entry in content:
                if entry.strip():
                    parts = entry.strip().split('\n')
                    if len(parts) >= 2:
                        question = parts[0].replace('Pregunta: ', '')
                        answer = parts[1].replace('Respuesta: ', '')
                        history.append({'question': question, 'answer': answer})
    except FileNotFoundError:
        pass
    return render_template('index.html', history=history[::-1])

#-------------------------------
@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question'].strip()
    
    if not question:
        return render_template('response.html', 
                             question="", 
                             answer="Por favor, ingresa una pregunta válida.")
    
    if len(question) > 500:
        return render_template('response.html',
                             question=question,
                             answer="Por favor, ingresa una pregunta más corta (máximo 500 caracteres).")
    
    try:
        detected_lang = detect(question)
    except LangDetectException:
        detected_lang = 'es'  # Default to Spanish if detection fails

    # Llamada a OpenAI GPT usando ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": get_system_prompt(detected_lang) + " Proporciona respuestas completas y bien estructuradas, asegurándote de concluir adecuadamente cada idea."},
            {"role": "user", "content": question}
        ],
        max_tokens=500,  # Aumentado para respuestas más completas
        temperature=0.7,  # Aumentado para más creatividad
        presence_penalty=0.2,  # Mayor penalización para evitar repeticiones
        frequency_penalty=0.2,  # Mayor penalización para variedad léxica
        top_p=0.95,  # Aumentado para mayor variedad manteniendo coherencia
        stop=["Fin.", "---", "Conclusión:"]  # Marcadores de finalización
    )

    # Extraer la respuesta generada por OpenAI
    answer = response.choices[0].message.content.strip().replace('\n', '<br>').replace('• ', '<br>• ')
    
    # Actualizar contadores
    global usage_count, total_tokens
    usage_count += 1
    tokens_used = response.usage.total_tokens
    total_tokens += tokens_used
    
    # Verificar límites y enviar notificaciones
    if total_tokens >= MAX_TOKENS:
        try:
            msg = MIMEMultipart()
            msg['From'] = os.getenv('EMAIL_USER')
            msg['To'] = ADMIN_EMAIL
            msg['Subject'] = "ADVERTENCIA: Límite de tokens alcanzado - Asistente de Mascotas"
            
            body = f"Se ha alcanzado el límite de tokens ({MAX_TOKENS}).\nUso total: {total_tokens}\nConsultas totales: {usage_count}"
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
            server.send_message(msg)
            server.quit()
            return render_template('response.html', 
                                question=question,
                                answer="Lo siento, se ha alcanzado el límite de uso. Contacta al administrador.")
        except Exception as e:
            print(f"Error enviando email: {e}")
    
    # Enviar reporte diario
    if usage_count % 10 == 0:  # Cada 10 usos
        try:
            msg = MIMEMultipart()
            msg['From'] = os.getenv('EMAIL_USER')
            msg['To'] = ADMIN_EMAIL
            msg['Subject'] = "Gasto en App de Asistente de Mascotas"
            
            body = f"Reporte de uso:\nConsultas totales: {usage_count}\nTokens totales: {total_tokens}\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Error enviando reporte: {e}")

    # Guardar la pregunta y respuesta en un archivo
    with open("log.txt", "a", encoding="utf-8") as file:
        file.write(f"Pregunta: {question}\nRespuesta: {answer}\n{'-'*50}\n")

    # Renderizar la plantilla response.html
    return render_template('response.html', question=question, answer=answer)



#----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
