import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE TU CLOUDINARY
CLOUD_NAME = "dwydwjpos" 

# 2. Configuración de la página web
st.set_page_config(page_title="Catálogo de Productos", page_icon="📦", layout="wide")

st.title("📦 Catálogo Digital para Comerciales")
st.write("Consulta la lista de precios e imágenes en tiempo real desde la nube.")

# 3. Cargar los datos del Excel
try:
    df = pd.read_excel("base_datos.xlsx") 
    # 🟢 ORDENAMOS POR DESCRIPCIÓN AL PRINCIPIO
    df = df.sort_values(by='Descripcion', ascending=True)
except Exception as e:
    st.error(f"No se pudo leer el archivo Excel. Error: {e}")
    st.stop()

# 4. Buscador en la parte superior
busqueda = st.text_input("🔍 Buscar por descripción o código de artículo:", "")

# Filtrar las filas del Excel según la búsqueda del comercial
if busqueda:
    df_filtrado = df[
        df['Descripcion'].astype(str).str.contains(busqueda, case=False) |
        df['Codigo'].astype(str).str.contains(busqueda, case=False)
    ]
else:
    df_filtrado = df

# 🟢 SOLUCIÓN AQUÍ: Al añadir "sort=False", mantenemos intacto el orden alfabético por descripción que logramos arriba
articulos_unicos = df_filtrado.groupby('Codigo', sort=False)

# 5. ESTRUCTURA DE 3 COLUMNAS POR FILA
cols = st.columns(3)

# Recorremos cada producto único
for indice, (codigo, filas_articulo) in enumerate(articulos_unicos):
    primera_fila = filas_articulo.iloc[0]
    
    with cols[indice % 3]:
        with st.container(border=True):
            # --- 1. IMAGEN DESDE CLOUDINARY CON AUTO-RECORTE UNIFORME ---
            # 🟢 CAMBIO LLAVE: Usamos directamente la variable 'codigo' (el código del artículo)
            nombre_foto = str(codigo).strip()
            
            if nombre_foto and nombre_foto != "nan" and nombre_foto != "None":
                # Forzamos a Cloudinary a reescalar la foto a 300x300 en un contenedor cuadrado limpio
                url_foto = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/c_pad,g_center,h_300,w_300,b_auto/{nombre_foto}.jpg"
                st.image(url_foto, use_container_width=True)
            else:
                st.warning("📸 Sin foto asignada")
            
                      
            # --- 2. TÍTULO Y CÓDIGO ---
            st.subheader(primera_fila['Descripcion'])
            st.write(f"**Código:** {codigo}")
            
            st.markdown("---")
            
            # --- 3. BLOQUE DE PRECIOS BASE ---
            precios_cols = st.columns(2)
            with precios_cols[0]:
                try:
                    val_pvp = float(primera_fila['PVP'])
                    st.write(f"**PVP:** {val_pvp:.2f} €")
                except:
                    st.write(f"**PVP:** {primera_fila['PVP']}")
                    
            with precios_cols[1]:
                try:
                    val_dto = float(primera_fila['Dto'])
                    st.write(f"**Dto:** {val_dto:.0f}%")
                except:
                    st.write(f"**Dto:** {primera_fila['Dto']}")
            
            # Precio Neto
            try:
                val_neto = float(primera_fila['neto'])
                st.metric(label="Precio Neto", value=f"{val_neto:.2f} €")
            except:
                st.metric(label="Precio Neto", value=f"{primera_fila['neto']} €")
                
            # --- 4. BLOQUE MULTI-CANTIDAD (ESCANDALLOS) ---
            tiene_ofertas = False
            for _, fila_precios in filas_articulo.iterrows():
                cant_of = str(fila_precios['cant of']).strip()
                oferta = str(fila_precios['oferta']).strip()
                
                if cant_of and cant_of != "nan" and cant_of != "None":
                    if not tiene_ofertas:
                        st.markdown("<p style='color: #ffaa00; margin-top: 10px; margin-bottom: 2px; font-weight: bold;'>⚠️ Precios por Volumen:</p>", unsafe_allow_html=True)
                        tiene_ofertas = True
                    
                    try:
                        val_oferta = float(fila_precios['oferta'])
                        st.write(f"🔹 A partir de **{float(cant_of):.0f} uds.** ➔ **{val_oferta:.2f} €**")
                    except:
                        st.write(f"🔹 Lote: **{cant_of} uds.**")