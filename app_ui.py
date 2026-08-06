import streamlit as st
import httpx

# Configuración de la página
st.set_page_config(
    page_title="LLMOps Proxy Chat",
    page_icon="🤖",
    layout="centered"
)

# URL de tu proxy FastAPI (si corre por docker, o localmente en el 8000)
PROXY_URL = "http://localhost:8000/api/v1/chat"  # Ajusta la ruta según tu endpoint principal del proxy

st.title("🤖 Chat Inteligente con LLMOps Proxy")
st.markdown("Interfaz conectada a tu proxy seguro con Guardrails, DLP y métricas.")

# Inicializar el historial de chat en la sesión de Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores en pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto del usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Añadir mensaje del usuario al historial visual
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Enviar la petición al proxy de FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Pensando y validando seguridad..."):
            try:
                # Ajusta el payload según lo que reciba tu endpoint en FastAPI (ej. {"prompt": prompt} o {"message": prompt})
                payload = {"prompt": prompt}
                response = httpx.post(PROXY_URL, json=payload, timeout=60.0)
                
                if response.status_code == 200:
                    data = response.json()
                    # Extrae la respuesta dependiendo de cómo devuelva los datos tu API
                    bot_response = data.get("response", data.get("message", str(data)))
                    st.markdown(bot_response)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                else:
                    # <--- ¡AQUÍ ES DONDE LO REEMPLAZAS! --->
                    # Esto te mostrará el código y el texto exacto que devuelve FastAPI
                    st.error(f"⚠️ Código {response.status_code}: {response.text}")
                    st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Error {response.status_code}: {response.text}"})

            except httpx.ConnectError:
                st.error("❌ No se pudo conectar con el Proxy. Asegúrate de que FastAPI esté corriendo en el puerto 8000.")
            except Exception as e:
                st.error(f"❌ Ocurrió un error inesperado: {str(e)}")