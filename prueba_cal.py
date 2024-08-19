from streamlit_calendar import calendar
import streamlit as st

st.markdown(
    "## Demo for [streamlit-calendar](https://github.com/im-perativa/streamlit-calendar) 📆"
)

st.markdown(
    "[![](https://img.shields.io/github/stars/im-perativa/streamlit-calendar?style=social)](https://github.com/im-perativa/streamlit-calendar)"
)


events = [
    {
        "title": "Event 1",
        "color": "#FF6C6C",
        "start": "2023-07-03",
        "end": "2023-07-05",
        "resourceId": "a",
    }
]
#calendar_resources = [
    #{"id": "a", "building": "Building A", "title": "Room A"},
    #{"id": "b", "building": "Building A", "title": "Room B"},
    #{"id": "c", "building": "Building B", "title": "Room C"},
    #{"id": "d", "building": "Building B", "title": "Room D"},
    #{"id": "e", "building": "Building C", "title": "Room E"},
    #{"id": "f", "building": "Building C", "title": "Room F"},
#]

calendar_options = {
    "editable": "true",
    "navLinks": "true",
    #"resources": calendar_resources,
    "selectable": "true",
}

calendar_options = {
    **calendar_options,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridDay,dayGridWeek,dayGridMonth",
    },
    "initialDate": "2023-07-01",
    "initialView": "dayGridMonth",
}
   
state = calendar(
    events=st.session_state.get("events", events),
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

if state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

