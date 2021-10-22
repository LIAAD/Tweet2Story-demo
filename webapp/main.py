import streamlit as st
from session_state import SessionState, get
import input_phase, output_phase

import requests, json
url = 'http://localhost:8888/'

def init():
    st.set_page_config(page_title='Text2Story', page_icon = None, layout = 'wide', initial_sidebar_state = 'auto')
    st.markdown("""<style> .title {font-size:100px !important;} </style>""", unsafe_allow_html=True)

def draw_title():
    st.markdown('<p class="title">Text2Story</p>', unsafe_allow_html=True)

def rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))

def request(lang, publication_time, text, tools):
    request = {'lang': lang,
             'text': text,
             'publication_time': publication_time,
             'actor_extraction_tools': tools['actor_extraction_tools'],
             'time_extraction_tools': tools['time_extraction_tools'],
             'event_extraction_tools': tools['event_extraction_tools'],
             'objectal_link_extraction_tools': tools['objectal_link_extraction_tools'],
             'semantic_role_link_extraction_tools': tools['semantic_role_link_extraction_tools']}

    response = requests.post(url, data=json.dumps(request, indent=1))
    return response.text

session_state = SessionState(phase='input', text='', annotation='', visualization_option='')
def main():
    draw_title()

    session_state = get(phase='input', text='', annotation='', visualization_option='')

    if session_state.phase == 'input':
        session_state.input = input_phase.app()
        if session_state.input:
            session_state.text = session_state.input[2]
            session_state.annotation = request(lang=session_state.input[0],
                                               publication_time=session_state.input[1],
                                               text=session_state.input[2],
                                               tools=session_state.input[3])
            session_state.phase = 'output'
            rerun()

    elif session_state.phase == 'output':
        session_state.visualization_option = output_phase.app(session_state.text, session_state.annotation)

if __name__ == '__main__':
    init()
    main()
