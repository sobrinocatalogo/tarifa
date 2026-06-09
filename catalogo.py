import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE TU CLOUDINARY
# Mantengo el Cloud Name que vimos en tu captura anterior
CLOUD_NAME = "dwydwjpos" 
CARPETA_CLOUDINARY = "productos" 

# 2. Configuración de la interfaz de la página web
st.set_page_config(page_title="Catálogo de Productos", page_icon="📦", layout="wide")

st.title("📦 Catálogo Digital para Comerciales")
st.write("Consulta la lista de precios e imágenes en tiempo real.")

# 3. Cargar los datos del Excel
try:
    df = pd.read_excel("base_datos.xlsx")
except Exception as e:
    st.error(f"No se pudo leer el archivo Excel. Asegúrate de que se llama 'base_datos.xlsx'. Error: {e}")
    st.stop()

# 4. Buscador en la parte superior
busqueda = st.text_input("🔍 Buscar por descripción o código:", "")

# Filtrar el Excel según tus campos reales ('Descripcion' y 'Codigo')
if busqueda:
    df_filtrado = df[
        df['Descripcion'].astype(str).str.contains(busqueda, case=False) |
        df['Codigo'].astype(str).str.contains(busqueda, case=False)
    ]
else:
    df_filtrado = df

# 5. Mostrar los productos en una cuadrícula de 3 columnas
cols = st.columns(3)

for indice, fila in df_filtrado.iterrows():
    with cols[indice % 3]:
        with st.container(border=True):
            
            # --- GESTIÓN DE LA IMAGEN DESDE CLOUDINARY ---
            nombre_foto = str(fila['foto']).strip()
            
            if nombre_foto and nombre_foto != "nan":
                # Fabricamos la URL combinando tu nube con el nombre real de tu celda (ej: 68020142.jpg)
                url_foto = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/{CARPETA_CLOUDINARY}/{nombre_foto}"
                st.image(url_foto, use_container_width=True)
            else:
                st.warning("📸 Foto no especificada")
            
            # --- DATOS REALES DE TU EXCEL ---
            st.subheader(fila['Descripcion'])
            st.write(f"**Código:** {fila['Codigo']}")
            
            # Mostramos el PVP formateado con dos decimales
            try:
                precio_pvp = float(fila['PVP'])
                st.metric(label="PVP", value=f"{precio_pvp:.2f} €")
            except:
                st.metric(label="PVP", value=f"{fila['PVP']} €")