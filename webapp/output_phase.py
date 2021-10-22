import streamlit as st

def draw_sidebar():
    st.sidebar.header('Visualization')
    visualization_option = st.sidebar.radio('', ('Narrative', 'Annotation', 'DRS', 'MSC', 'Knowledge Graph'))
    return visualization_option

def app(narrative_text, narrative_annotation):
    visualization_option = draw_sidebar()

    if visualization_option == 'Narrative':
        st.write(narrative_text)
    elif visualization_option == 'Annotation':
        st.write(narrative_annotation)
    elif visualization_option == 'DRS':
        pass
    elif visualization_option == 'MSC':
        pass
    elif visualization_option == 'Knowledge Graph':
        pass

    return visualization_option
