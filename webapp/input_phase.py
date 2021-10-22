import streamlit as st

default_tweets = """ts fred continues to weaken as it moves away from the cape verde islands.
tropical storm grace forms in eastern atlantic.
ts grace is strengthening with 50 mph winds however the system is expected to weaken in the extended forecast.
tropical storm grace packing wind gusts of 58 mph.
tropical storm grace will likely dissipate east of the lesser antilles.
grace is likely to weaken to a tropical rainstorm prior to reaching the lesser antilles.
"""

def draw_sidebar():
    # Language
    lang_name_format = {'Portuguese' : 'pt', 'English' : 'en'}
    st.sidebar.header('Language')
    lang = st.sidebar.radio('', ('English', 'Portuguese'))
    lang = lang_name_format[lang]

    # Tools
    st.sidebar.header('Extraction tools')

    st.sidebar.subheader('Actor entity extraction')
    ACTOR_ENTITY_EXTRACTION_TOOLS = {'spacy' : False, 'nltk' : False}
    ACTOR_ENTITY_EXTRACTION_TOOLS['spacy']    = st.sidebar.checkbox('spaCy', key='1', value=True)
    ACTOR_ENTITY_EXTRACTION_TOOLS['nltk']     = st.sidebar.checkbox('NLTK', key='2', value=False)
    # ACTOR_ENTITY_EXTRACTION_TOOLS['sparknlp'] = st.sidebar.checkbox('Spark NLP', '3')

    st.sidebar.subheader('Time entity extraction')
    TIME_ENTITY_EXTRACTION_TOOLS = {'py_heideltime' : False}
    TIME_ENTITY_EXTRACTION_TOOLS['py_heideltime'] = st.sidebar.checkbox('py_heideltime', key='4', value=True)

    st.sidebar.subheader('Event entity extraction')
    EVENT_ENTITY_EXTRACTION_TOOLS = {'allennlp' : False}
    EVENT_ENTITY_EXTRACTION_TOOLS['allennlp'] = st.sidebar.checkbox('Allen NLP', key='5', value=True)

    st.sidebar.subheader('Objectal link extraction')
    OBJECTAL_LINK_EXTRACTION_TOOLS  = {'allennlp' : False}
    OBJECTAL_LINK_EXTRACTION_TOOLS['allennlp'] = st.sidebar.checkbox('Allen NLP', key='6', value=True)

    st.sidebar.subheader('Semantic Role link extraction')
    SEMANTICROLE_LINK_EXTRACTION_TOOLS = {'allennlp' : False}
    SEMANTICROLE_LINK_EXTRACTION_TOOLS['allennlp'] = st.sidebar.checkbox('Allen NLP', key='7', value=True)

    return lang, {'actor_extraction_tools'              : [tool for tool in ACTOR_ENTITY_EXTRACTION_TOOLS if ACTOR_ENTITY_EXTRACTION_TOOLS[tool]],
                  'time_extraction_tools'               : [tool for tool in TIME_ENTITY_EXTRACTION_TOOLS if TIME_ENTITY_EXTRACTION_TOOLS[tool]],
                  'event_extraction_tools'              : [tool for tool in EVENT_ENTITY_EXTRACTION_TOOLS if EVENT_ENTITY_EXTRACTION_TOOLS[tool]],
                  'objectal_link_extraction_tools'      : [tool for tool in OBJECTAL_LINK_EXTRACTION_TOOLS if OBJECTAL_LINK_EXTRACTION_TOOLS[tool]],
                  'semantic_role_link_extraction_tools' : [tool for tool in SEMANTICROLE_LINK_EXTRACTION_TOOLS if SEMANTICROLE_LINK_EXTRACTION_TOOLS[tool]]
                 }


def valid_input(tools, narrative_text):
    # Check if it's selected, at least, one tool per extraction
    for key in tools:
        if len(tools[key]) == 0:
            signal_error(key)
            return False

    # Check if narrative text isn't empty
    if narrative_text == '':
        signal_error('narrative_text')
        return False

    return True


def signal_error(input_error_code):
    if input_error_code == 'actor_extraction_tools':
        st.error('You need to specify at least one tool to the actor extraction!')
    elif input_error_code == 'timex_extraction_tools':
        st.error('You need to specify at least one tool to the time extraction!')
    elif input_error_code == 'event_extraction_tools':
        st.error('You need to specify at least one tool to the event extraction!')
    elif input_error_code == 'objectal_extraction_tools':
        st.error('You need to specify at least one tool to the objectal extraction!')
    elif input_error_code == 'semanticrole_extraction_tools':
        st.error('You need to specify at least one tool to the semantic role extraction!')

def app():
    """
    Returns
    -------
    [] - If no valid configuration to start extraction
    [lang : str, publication_time : str, narrative_text : str, tools : {str -> [str]}] - If valid configuration to start extraction (follow to output phase)
    """
    lang, tools = draw_sidebar()

    publication_time = str(st.date_input('Publication Date'))
    narrative_text = st.text_area(label='Narrative Text', value=default_tweets, height=300)

    pressed_extract = st.button('Extract!')

    if pressed_extract and valid_input(tools, narrative_text):
        return [lang, publication_time, narrative_text, tools]
    else:
        return []
