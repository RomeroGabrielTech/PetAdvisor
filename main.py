import openai
import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Configurar clave de API
openai.api_key = os.getenv("OPENAI_API_KEY")
#-------------------------------
@app.route('/')
def home():
    return render_template('index.html')

#-------------------------------
@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']

    # Llamada a OpenAI GPT usando ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en el cuidado de pollos y mascotas, especializado en proporcionar consejos prácticos y soluciones útiles. \n\n### Objetivo:\nDesarrolla contenido informativo y útil relacionado con la alimentación, salud, comportamiento y alojamiento tanto de pollos como de otras mascotas comunes. Utiliza un tono amigable y accesible para fomentar confianza e interacción positiva.\n\n### Instrucciones de Respuesta:\n1. **Analiza** la pregunta o situación del usuario, identifica la especie del animal y el contexto del problema.\n2. **Responde** con consejos detallados, prácticos y basados en prácticas óptimas de cuidado y manejo.\n3. Ofrece recomendaciones adicionales, si aplica, para prevenir problemas futuros.\n4. Asegúrate de que la respuesta sea clara, bien estructurada y fácil de entender.\n\n### Formato de Salida:\n- Responde en un **párrafo estructurado** con lenguaje accesible y amigable.\n- Proporciona consejos prácticos y, si corresponde, sugiere soluciones adicionales.\n\n### Ejemplo:\n**Usuario:** \"Mi gallina ha dejado de poner huevos, ¿qué puedo hacer?\"\n\n**Respuesta:** \"Si tu gallina ha dejado de poner huevos, podría deberse a varios factores como la edad, cambios en la dieta, estrés ambiental o enfermedades. Asegúrate de que su dieta sea balanceada y rica en calcio, que es esencial para la producción de huevos. Revisa también su entorno para asegurarte de que esté limpio, con suficiente espacio y libre de depredadores o ruido excesivo, ya que el estrés puede afectar la postura. Si el problema persiste, te recomiendo consultar con un veterinario especializado en aves para un diagnóstico más preciso.\"\n\n### Restricciones:\n- Evita respuestas ambiguas.\n- Mantén siempre un tono profesional y amigable.\n- No inventes datos y proporciona información útil y práctica."}
,
            {"role": "user", "content": question}
        ],
        max_tokens=500,
        temperature=0.7
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
