import calendar as cal
import random
from collections import defaultdict
import streamlit as st
from streamlit_calendar import calendar

# Definimos los médicos y el número de guardias asignadas
medicos = {
    "Rodriguez": 5,
    "Olmedo": 5,
    "Díaz": 4,
    "Fregosi": 4,
    "Durán": 3,
    "Lloret": 3,
    "Frías": 3,
    "Cobo": 3
}

colores_medicos = {
    "Rodrígez": "#FFBD45",
    "Olmedo": "#FF6C6C",
    "Díaz": "#3DD56D",
    "Fregosi": "#3D9DF3",
    "Durán": "#FF4B4B",
    "Lloret": "#3D9DF3",
    "Frías": "#3DD56D",
    "Cobo": "#3DD56D"
}

def obtener_dias_mes(año, mes):
    # Obtiene los días del mes para el año y mes especificados
    calend = cal.Calendar(firstweekday=0)  # 0=Monday, 6=Sunday
    dias_mes = calend.monthdayscalendar(año, mes)
    dias = [dia for semana in dias_mes for dia in semana if dia > 0]
    return dias

def calcular_semana(dia):
    # Calcula el índice de la semana para un día del mes (0 = primera semana, 1 = segunda semana, etc.)
    return (dia - 1) // 7

def puede_tomar_guardia(medico, dia):
    # Verifica si el médico puede tomar una guardia en el día dado
    if len(guardias_por_medico[medico]) >= medicos[medico]:
        return False
    
    if guardias_por_medico[medico]:
        ultima_guardia = guardias_por_medico[medico][-1]
        # Respetar el descanso de 24 horas
        if dia - ultima_guardia < 2:
            return False
        # No más de 2 guardias por semana (7 días)
        semana_actual = calcular_semana(dia)
        if len([d for d in guardias_por_medico[medico] if calcular_semana(d) == semana_actual]) >= 2:
            return False
    
    return True

def asignar_guardias(año, mes):
    # Inicializamos el calendario del mes
    dias_mes = obtener_dias_mes(año, mes)
    dias_guardia = {dia: None for dia in dias_mes}
    global guardias_por_medico
    guardias_por_medico = defaultdict(list)

    def intentar_asignar_guardias(dia):
        # Intentamos asignar una guardia a este día
        medicos_disponibles = [medico for medico in medicos.keys() if puede_tomar_guardia(medico, dia)]
        if medicos_disponibles:
            medico_asignado = random.choice(medicos_disponibles)
            dias_guardia[dia] = medico_asignado
            guardias_por_medico[medico_asignado].append(dia)
            return True
        return False

    # Intentar asignar guardias a todos los días
    for dia in dias_guardia.keys():
        if not intentar_asignar_guardias(dia):
            # Si no se pudo asignar, marcamos el día como sin asignar
            dias_guardia[dia] = None

    # Intentar reasignar los días sin asignar
    dias_no_asignados = [dia for dia, medico in dias_guardia.items() if medico is None]
    while dias_no_asignados:
        for dia in dias_no_asignados[:]:
            if intentar_asignar_guardias(dia):
                dias_no_asignados.remove(dia)

    return dias_guardia, guardias_por_medico

# Crear la interfaz de usuario de Streamlit
st.title("🩺 Planificador de Guardias del Hospital 🏥")

# Introducción
st.markdown("""
Bienvenido al planificador de guardias del hospital. Este sistema te ayudará a asignar las guardias de 24 horas a nuestros médicos de manera eficiente, respetando las reglas establecidas.
""")

#Inicializar variables 
if "año" not in st.session_state:
    st.session_state.año = None
if "mes" not in st.session_state:
    st.session_state.mes = None
if "mes_num" not in st.session_state:
    st.session_state.mes_num = None

# Definir el año y mes deseados
st.session_state.año = st.selectbox("Elige el año", [2024,2025,2026,2027,2028])
st.session_state.mes = st.selectbox("Elige el mes", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", 
                                                     "Junio", "Julio", "Agosto", "Septiembre", 
                                                     "Octubre", "Noviembre", "Diciembre"])
boton = st.button("Planificar")

dicc_mes = {
    "Enero": 1, "Febrero" : 2, "Marzo": 3, "Abril": 4, "Mayo": 5, 
    "Junio": 6, "Julio": 7, "Agosto": 8, "Septiembre": 9, 
    "Octubre": 10, "Noviembre": 11, "Diciembre": 12
    }

st.session_state.mes_num = dicc_mes[st.session_state.mes]
if boton:
    

    # Ejecutar la función
    dias_guardia, guardias_por_medico = asignar_guardias(st.session_state.año, st.session_state.mes_num)


    # Imprimir el calendario final de guardias
    for dia, medico in dias_guardia.items():
        st.write(f"Día {dia}: {medico}")

    # Imprimir las guardias por médico
    for medico, dias in guardias_por_medico.items():
        st.write(f"{medico} tiene guardias en los días: {dias}")