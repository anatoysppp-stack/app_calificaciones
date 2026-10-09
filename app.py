import streamlit as st
import pandas as pd

# 1. Configurar el título y diseño de la página
st.set_page_config(page_title="Asistente de Calificaciones", layout="wide")

# 2. Mensaje de bienvenida del asistente
st.title("🎓 Asistente de Calificaciones del Salón")
st.markdown("""
¡Hola! Soy tu asistente virtual de calificaciones. 
Aquí puedes consultar y modificar las calificaciones de los alumnos. 
**Si cambias un dato en la tabla y guardas, el archivo Excel se actualizará automáticamente con los datos más recientes.**
""")

archivo_excel = "Calificaciones_Parciales.xlsx"

# 3. Función para cargar los datos desde el Excel
def cargar_datos():
    try:
        # Leemos el archivo Excel
        return pd.read_excel(archivo_excel)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo '{archivo_excel}'. Asegúrate de que esté en la misma carpeta.")
        return None

# 4. Función para guardar los cambios de vuelta al Excel
def guardar_datos(df_nuevo):
    # Recalcular la Calificación Final automáticamente (opcional, basado en tus columnas)
    df_nuevo["Calificacion_Final"] = (
        df_nuevo["Investigacion"] + 
        df_nuevo["linea de tiempo"] + 
        df_nuevo["participacion"] + 
        df_nuevo["Asistencia"] + 
        df_nuevo["Evaluacion"]
    )
    # Actualizar Estatus (Aprobado >= 70, por ejemplo)
    df_nuevo["ESTATUS"] = df_nuevo["Calificacion_Final"].apply(lambda x: "APROBADO" if x >= 70 else "REPROBADO")
    
    # Guardar en el Excel
    df_nuevo.to_excel(archivo_excel, index=False)
    st.success("✅ ¡Datos guardados y actualizados correctamente en el Excel!")

# 5. Lógica principal de la App
df = cargar_datos()

if df is not None:
    st.divider()
    
    # Buscador tipo asistente
    st.subheader("🔍 Buscar Alumno")
    busqueda = st.text_input("Ingresa el Nombre o Número de Control para ver su estado actual:")
    
    if busqueda:
        # Filtrar la tabla si el profe busca a alguien en específico
        df_filtrado = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
        st.dataframe(df_filtrado, use_container_width=True)
    
    st.divider()
    
    # Tabla interactiva
    st.subheader("📝 Base de Datos Principal (Editable)")
    st.write("Profesor: Haz doble clic en cualquier celda para modificar un punto o tarea.")
    
    # st.data_editor permite modificar el dataframe directamente en la web
    df_editado = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    
    # Botón para guardar los cambios
    if st.button("💾 Guardar Cambios"):
        guardar_datos(df_editado)