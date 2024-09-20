import os
import openai
from openai import OpenAI
import docx
from markdown import markdown
from tqdm import tqdm

# Obtener la clave API de OpenAI desde la variable de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

# Solicitar el role de "system" y "user" al usuario
system_role = input("Ingrese el role de 'system': ")
user_role = input("Ingrese el role de 'user': ")

# Mensaje inicial con los roles personalizados ingresados por el usuario
messages = [
    {
        "role": "system",
        "content": system_role
    },
    {
        "role": "user",
        "content": user_role
    }
]

print("Generando el esquema de la política...")

try:
    client = OpenAI()  # Inicialización del cliente
    response = client.chat.completions.create(  # Llamada a la API
        model="chatgpt-4o-latest",
        messages=messages,
        max_tokens=500,
        temperature=0.2,
    )
except Exception as e:
    print("Ocurrió un error al conectarse a la API de OpenAI:", e)
    exit(1)

# Obtener el esquema de la respuesta
outline = response.choices[0].message.content.strip()  # Actualización de la llamada a la API

print(outline + "\n")

# Dividir el esquema en secciones
sections = outline.split("\n\n")

# Preparar el documento en formato HTML
html_text = ""

# Generar detalles para cada sección en el esquema
for i, section in tqdm(enumerate(sections, start=1), total=len(sections), leave=False):
    print(f"\nGenerando detalles para la sección {i}...")

    # Preparar mensajes con los detalles solicitados para cada sección
    messages = [
        {
            "role": "system",
            "content": system_role
        },
        {
            "role": "user",
            "content": f"Actualmente estás redactando una política de ciberseguridad. Escribe la narrativa, contexto y detalles para la siguiente sección (y solo esta sección): {section}. Usa tantos detalles y explicaciones como sea posible. No escribas nada que deba ir en otra sección de la política."
        }
    ]

    try:
        response = client.chat.completions.create(  # Llamada a la API
            model="chatgpt-4o-latest",
            messages=messages,
            max_tokens=500,
            temperature=0.2,
        )
    except Exception as e:
        print("Ocurrió un error al conectarse a la API de OpenAI:", e)
        exit(1)

    # Obtener los detalles generados
    detailed_info = response.choices[0].message.content.strip()  # Actualización de la llamada a la API

    # Convertir markdown a HTML y añadirlo al texto HTML
    html_text += markdown(detailed_info)

# Guardar el documento en formato HTML
with open("Cybersecurity_Policy.html", 'w') as f:
    f.write(html_text)

print("\nHecho.")

#TODO integrar que no mencione pero que considera estdar PCI 4.0.1 y cumplimiento framework NIST