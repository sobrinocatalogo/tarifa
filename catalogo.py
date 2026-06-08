import streamlit as st
import pandas as pd
import os

# 1. Configuración de la página web (Título e icono en la pestaña)
st.set_page_config(page_title="Catálogo de Productos", page_icon="📦", layout="wide")

st.title("📦 Catálogo Digital para Comerciales")
st.write("Consulta la lista de precios y stock en tiempo real.")

# 2. Cargar los datos del Excel
# Usamos un try/except por si el archivo no se encuentra o está abierto
try:
    df = pd.read_excel("base_datos.xlsx")
except Exception as e:
    st.error(f"No se pudo leer el archivo Excel. Asegúrate de que se llama 'base_datos.xlsx'. Error: {e}")
    st.stop()

# 3. Buscador en la parte superior
busqueda = st.text_input("🔍 Buscar por producto, código o categoría:", "")

# Filtrar el Excel según lo que escriba el comercial
if busqueda:
    # Convertimos de forma segura cada columna a texto y rellenamos los vacíos con ""
    descripcion_str = df['Descripcion'].fillna('').astype(str)
    codigo_str = df['Codigo'].fillna('').astype(str)
    dto_str = df['Dto'].fillna('').astype(str)
    neto_str = df["neto"].fillna("").astype(str)
    
    # Busca coincidencias sin importar mayúsculas o minúsculas
    df_filtrado = df[
        descripcion_str.str.contains(busqueda, case=False) |
        codigo_str.str.contains(busqueda, case=False) |
        dto_str.str.contains(busqueda, case=False)
    ]
else:
    df_filtrado = df

# 4. Mostrar los productos en un diseño de cuadrícula (Tarjetas limpias y alineadas)
# Procesamos los productos filtrados en bloques de 3 en 3
for i in range(0, len(df_filtrado), 3):
    # Selecciona un grupo de hasta 3 productos
    bloque = df_filtrado.iloc[i:i+3]
    
    # Crea 3 columnas limpias para esta fila concreta
    cols = st.columns(3)
    
    # Coloca cada producto del bloque en su columna correspondiente (0, 1 o 2)
    for idx, (_, fila) in enumerate(bloque.iterrows()):
        with cols[idx]:
            with st.container(border=True):
                # Ruta de la foto
                ruta_foto = os.path.join("fotos", str(fila['foto']))
                
                # Muestra la foto o el aviso si no existe
                if os.path.exists(ruta_foto):
                    st.image(ruta_foto, use_container_width=True)
                else:
                    st.warning("📸 Foto no disponible")
                
                # Datos del producto
                st.subheader(fila['Descripcion'])
                st.write(f"**Código:** {fila['Codigo']}")
                st.write(f"**PVP:** {fila['PVP']}")
                st.write(f"**Dto:** {fila['Dto']}")
                
                
                # Precio
                
                st.metric(label="Precio Neto", value=f"{fila['neto']:.2f} €")