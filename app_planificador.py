import calendar as cal
import random
from collections import defaultdict
import streamlit as st
from streamlit_calendar import calendar


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

def guardar(doctor, guardias, color):
    dicc = {
        "doctor" : doctor,
        "guardias" : guardias,
        "color" : color
    }
    st.session_state.medicos.append(dicc)
    st.success("Se ha añadido correctamente al doctor/a {}".format(doctor))


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
if "eventos" not in st.session_state:
    st.session_state.eventos = []
if "state" not in st.session_state:
    st.session_state.state = []
if "fecha_inicio" not in st.session_state:
    st.session_state.fecha_inicio = "2024-08-01"
if "medicos" not in st.session_state:
    st.session_state.medicos = []

col0,col1, col2 = st.columns(3)
with col0:
    doctor = st.text_input("introduce el apellido del doctor/a")
with col1:
    guardias = st.number_input("Introduce el número de guardias", step = 1)
with col2: 
    color = st.color_picker("Elige el color")

boton_doctor = st.button("Añadir doctor/a")
if boton_doctor:
    guardar(doctor, guardias, color)

# Definir el año y mes deseados
st.session_state.año = st.selectbox("Elige el año", [2024,2025,2026,2027,2028])
st.session_state.mes = st.selectbox("Elige el mes", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", 
                                                     "Junio", "Julio", "Agosto", "Septiembre", 
                                                     "Octubre", "Noviembre", "Diciembre"])


dicc_mes = {
    "Enero": 1, "Febrero" : 2, "Marzo": 3, "Abril": 4, "Mayo": 5, 
    "Junio": 6, "Julio": 7, "Agosto": 8, "Septiembre": 9, 
    "Octubre": 10, "Noviembre": 11, "Diciembre": 12
    }

st.session_state.mes_num = dicc_mes[st.session_state.mes]

boton = st.button("Planificar")


calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "selectable": "true",
}

calendar_options = {
    **calendar_options,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridDay,dayGridWeek,dayGridMonth",
    },
    "initialDate": "{}".format(st.session_state.fecha_inicio),
    "initialView": "dayGridMonth",
}
   
st.session_state.state = calendar(
    events= st.session_state.eventos,
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
)

if st.session_state.state.get("eventsSet") is not None:
    st.session_state["events"] = st.session_state.state["eventsSet"]
if boton:
    medicos = { dicc["doctor"] : dicc["guardias"] for dicc in st.session_state.medicos}
    colores_medicos = { dicc["doctor"] : dicc["color"] for dicc in st.session_state.medicos}
    dias_guardia, guardias_por_medico = asignar_guardias(st.session_state.año, st.session_state.mes_num)

    if st.session_state.mes_num <10:
        mes_numerico = "0{}".format(st.session_state.mes_num)
    else:
        mes_numerico = st.session_state.mes_num
    # Imprimir el calendario final de guardias
    for dia, medico in dias_guardia.items():
        if dia <10:
            fecha = "{}-{}-0{}".format(st.session_state.año, mes_numerico,dia)
        else:
            fecha = "{}-{}-{}".format(st.session_state.año, mes_numerico,dia)
        dicc_evento = {
            "title": "{}".format(medico),
            "color": "{}".format(colores_medicos[medico]),
            "start": "{}".format(fecha),
            "end": "{}".format(fecha),
        }
        st.session_state.eventos.append(dicc_evento)
    st.session_state.fecha_inicio = "{}-{}-01".format(st.session_state.año, mes_numerico)
    

    