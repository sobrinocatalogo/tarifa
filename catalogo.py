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

# =========================================================
# SECCIÓN 3: EL BUSCADOR
# =========================================================

busqueda = st.text_input("🔍 Buscar por producto, código o categoría:")

# Convertimos a texto las columnas clave para poder buscar en ellas de forma segura
descripcion_str = df["Descripcion"].fillna("").astype(str)
codigo_str = df["Codigo"].fillna("").astype(str)

# Filtramos el Excel: si el usuario escribe algo, busca coincidencias
if busqueda:
    df_filtrado = df[
        descripcion_str.str.contains(busqueda, case=False) |
        codigo_str.str.contains(busqueda, case=False)
    ]
else:
    df_filtrado = df  # Si no hay búsqueda, mostramos todos los productos

# =========================================================
# =========================================================
# SECCIÓN 4: DISEÑO EN 3 COLUMNAS (AGRUPADO POR CÓDIGO)
# =========================================================

# Agrupamos el Excel filtrado por la columna 'Codigo' para juntar los duplicados
productos_agrupados = list(df_filtrado.groupby("Codigo"))

# Recorremos los productos agrupados de 3 en 3 para armar las filas
for i in range(0, len(productos_agrupados), 3):
    # Creamos un bloque de 3 columnas en la pantalla
    cols = st.columns(3)
    
    # Colocamos cada producto en su columna correspondiente
    for j in range(3):
        if i + j < len(productos_agrupados):
            codigo, filas_producto = productos_agrupados[i + j]
            
            # Tomamos la primera fila para los datos generales del producto
            primera_fila = filas_producto.iloc[0]
            
            # Dibujamos la tarjeta del producto dentro de la columna asignada
            with cols[j].container(border=True):
                
                # 1. Control de la imagen (Bloque seguro)
                import os
                ruta_foto = f"fotos/{primera_fila['foto']}"
                if os.path.exists(ruta_foto):
                    st.image(ruta_foto, use_container_width=True)
                else:
                    st.warning("📷 Imagen no disponible")
                
                # 2. Textos del producto
                st.subheader(primera_fila["Descripcion"])
                st.caption(f"Código: {codigo}")
                
                st.markdown("---") # Una línea fina separadora
                
                # 3. Bloque de precios detallados (PVP, Dto y Neto)
                pvp_valor = primera_fila["PVP"]
                dto_valor = primera_fila["Dto"]
                neto_valor = primera_fila["neto"]
                
                st.write(f"🔹 **PVP:** {pvp_valor:.2f} €")
                st.write(f"📉 **Descuento:** {dto_valor}%")
                
                # Mostramos el Precio Neto Comercial en grande destacado
                st.metric(label="Precio Neto Comercial", value=f"{neto_valor:.2f} €")
                
                # 4. Comprobación y desglose de ofertas por cantidad
                tiene_oferta = any(pd.notna(f["oferta"]) and f["oferta"] > 0 for _, f in filas_producto.iterrows())
                
                if tiene_oferta:
                    st.markdown("---")
                    st.markdown("💥 **Precios por Cantidad:**")
                    
                    # Pintamos cada escala que tenga este artículo en el Excel
                    for _, fila in filas_producto.iterrows():
                        if pd.notna(fila["oferta"]) and fila["oferta"] > 0:
                            cantidad_minima = int(fila["cant of"]) if pd.notna(fila["cant of"]) else 1
                            st.write(f"📦 **{cantidad_minima} ud.** ➔ **{fila['oferta']:.2f} €**")