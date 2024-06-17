import streamlit as st
import requests
import time

# Dirección IP del ESP32 y puerto donde corre el servidor web
esp32_ip = "192.168.137.124"
port = 80

# Ruta en el ESP32 para obtener los datos de las mediciones
data_route = f"http://{esp32_ip}/data"

# Función para obtener los datos de las mediciones desde el ESP32
def fetch_data():
    try:
        response = requests.get(data_route)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error al obtener datos: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")
        return None

# Configuración inicial de la aplicación Streamlit
st.title('Visualización de Mediciones de CO2')

# Usar st.empty() para crear un contenedor para el gráfico dinámico
chart_container = st.empty()

# Variable para almacenar la última actualización de datos
last_update = 0

# Loop principal para actualizar el gráfico
while True:
    current_time = time.time()
    
    # Actualizar datos si han pasado al menos 10 segundos desde la última actualización
    if current_time - last_update >= 10:
        data = fetch_data()
        if data:
            # Limpiar el contenedor del gráfico y actualizar con los nuevos datos
            chart_container.line_chart(data)
            last_update = current_time  # Actualizar el tiempo de la última actualización
    
    time.sleep(1)  # Esperar 1 segundo antes de revisar de nuevo

