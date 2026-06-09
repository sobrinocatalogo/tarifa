import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE TU CLOUDINARY
CLOUD_NAME = "dwydwjpos" 
CARPETA_CLOUDINARY = "productos" 

# 2. Configuración de la página web (Diseño ancho)
st.set_page_config(page_title="Catálogo de Productos", page_icon="📦", layout="wide")

st.title("📦 Catálogo Digital para Comerciales")
st.write("Consulta la lista de precios e imágenes en tiempo real desde la nube.")

# 3. Cargar los datos del Excel
try:
    # Busca tu archivo; recuerda que debe llamarse exactamente así en tu carpeta
    df = pd.read_excel("base_datos.xlsx") 
except Exception as e:
    st.error(f"No se pudo leer el archivo Excel. Asegúrate de que se llama 'base_datos.xlsx'. Error: {e}")
    st.stop()

# 4. Buscador en la parte superior
busqueda = st.text_input("🔍 Buscar por descripción o código de artículo:", "")

# Filtrar las filas del Excel según lo que escriba el comercial
if busqueda:
    df_filtrado = df[
        df['Descripcion'].astype(str).str.contains(busqueda, case=False) |
        df['Codigo'].astype(str).str.contains(busqueda, case=False)
    ]
else:
    df_filtrado = df

# 5. ESTRUCTURA DE 3 COLUMNAS POR FILA
cols = st.columns(3)

# Recorremos los artículos del Excel uno a uno
for indice, fila in df_filtrado.iterrows():
    # Este truco matemática (% 3) va repartiendo los artículos en las 3 columnas de forma limpia
    with cols[indice % 3]:
        # Creamos una tarjeta con borde para cada producto
        with st.container(border=True):
            
            # --- CONTROL DE LA IMAGEN DESDE CLOUDINARY ---
            nombre_foto = str(fila['foto']).strip()
            
            if nombre_foto and nombre_foto != "nan" and nombre_foto != "None":
                # Creamos la URL que apunta directamente a tu foto subida (ej: 68020142.jpg)
                url_foto = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/{CARPETA_CLOUDINARY}/{nombre_foto}"
                st.image(url_foto, use_container_width=True)
            else:
                st.warning("📸 Foto no disponible")
            
            # --- DATOS REALES DE TU EXCEL ---
            st.subheader(fila['Descripcion'])
            st.write(f"**Código:** {fila['Codigo']}")
            
            # Mostramos el PVP formateado con dos decimales de forma segura
            try:
                precio_pvp = float(fila['PVP'])
                st.metric(label="PVP", value=f"{precio_pvp:.2f} €")
            except:
                st.metric(label="PVP", value=f"{fila['PVP']} €")