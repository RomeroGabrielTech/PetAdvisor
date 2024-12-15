import openai
import os
from flask import Flask, render_template, request
from langdetect import detect, LangDetectException

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
    return render_template('index.html')

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
            {"role": "system", "content": get_system_prompt(detected_lang)},
            {"role": "user", "content": question}
        ],
        max_tokens=300,  # Reducido para optimizar costos
        temperature=0.5,  # Reducido para respuestas más consistentes
        presence_penalty=0.1,  # Ligera penalización para evitar repeticiones
        frequency_penalty=0.1,  # Ligera penalización para variedad léxica
        top_p=0.9  # Núcleo de muestreo para mantener respuestas relevantes
    )

    # Extraer la respuesta generada por OpenAI
    answer = response.choices[0].message.content.strip()

    # Guardar la pregunta y respuesta en un archivo
    with open("log.txt", "a", encoding="utf-8") as file:
        file.write(f"Pregunta: {question}\nRespuesta: {answer}\n{'-'*50}\n")

    # Renderizar la plantilla response.html
    return render_template('response.html', question=question, answer=answer)



#----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
