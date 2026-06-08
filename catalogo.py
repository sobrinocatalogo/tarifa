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

# ---------------------------------------------------------
        # SECCIÓN 4: DISEÑO DE LAS TARJETAS (AGRUPADO POR CÓDIGO)
        # ---------------------------------------------------------
        
        # Agrupamos el Excel filtrado por Código para juntar los duplicados
productos_agrupados = df_filtrado.groupby("Codigo")

for codigo, filas_producto in productos_agrupados:
    primera_fila = filas_producto.iloc[0]
    # (El resto de tu código de las tarjetas que va aquí dentro...)
            # Cogemos la primera fila para los datos fijos del producto
    primera_fila = filas_producto.iloc[0]
            
            # Creamos el contenedor visual para la tarjeta del producto
    with st.container(border=True):
                
                # Fila 1: Imagen del producto
                # --- CAMBIA TU LÍNEA DE ST.IMAGE POR ESTE BLOQUE SEGURO ---
                import os

                ruta_foto = f"fotos/{primera_fila['foto']}"

                # Comprobamos si la foto existe físicamente antes de intentar pintarla
                if os.path.exists(ruta_foto):
                    st.image(ruta_foto, width=150)
                else:
                    # Si no existe, ponemos un aviso amigable o un icono de una caja
                    st.warning("📷 Imagen no disponible")
                
                # Fila 2: Título del artículo y su Código único
                st.subheader(primera_fila["Descripcion"])
                st.caption(f"Código: {codigo}")
                
                # Fila 3: Precio Neto estándar (Base)
                st.metric(label="Precio Neto Base", value=f"{primera_fila['neto']:.2f} €")
                
                # Fila 4: Comprobamos si tiene ofertas por volumen en sus filas
                tiene_oferta = False
                
                # Recorremos las filas agrupadas para ver si alguna tiene precio de oferta
                for _, fila in filas_producto.iterrows():
                    if pd.notna(fila["oferta"]) and fila["oferta"] > 0:
                        tiene_oferta = True
                        break # En cuanto encuentra una, ya sabemos que tiene promo
                
                # Si se confirma que hay ofertas, pintamos el desglose
                if tiene_oferta:
                    st.markdown("---") # Línea fina de separación
                    st.markdown("💥 **Precios Especiales por Cantidad:**")
                    
                    # Dibujamos cada tramo de oferta que venga en el Excel
                    for _, fila in filas_producto.iterrows():
                        if pd.notna(fila["oferta"]) and fila["oferta"] > 0:
                            # Leemos la cantidad mínima (si está vacía, por defecto es 1)
                            cantidad_minima = int(fila["cant of"]) if pd.notna(fila["cant of"]) else 1
                            
                            # Imprimimos la línea de la oferta formateada
                            st.write(f"📦 Llevando **{cantidad_minima} ud.** o más ➔ **{fila['oferta']:.2f} €** / ud")