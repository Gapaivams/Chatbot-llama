import streamlit as st
import ollama



st.title("Chat Senai") 

with st.sidebar:
    st.header("Configurações")
    modelos = "llama3:8b"
    modelo_selecionado = st.selectbox(
        "Escolha o modelo:",
        options=modelos,
        index=0
    )


    if st.button("Nova conversa"):
        st.session_state.messages = []
        st.rerun()

    


if "messages" not in st.session_state:
    st.session_state.messages = []




for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("digite sua mensagem..."):
    st.session_state.messages.append({"role":"user", "content": prompt})

with st.chat_message("user"):
    if prompt is None:
        st.markdown('Digite algo')
    else:
        st.markdown(prompt)
    

if not st.session_state.messages:
    message_placeholder = st.empty()
else:
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = ollama.chat(
                model=modelo_selecionado,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream = True
            )

            for chunk in stream:
                if chunk['message']['content']:
                    full_response += chunk['message']['content']
                    message_placeholder.markdown(full_response + " ")
                message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f'Erro ao gerar resposta: {str(e)}')
            full_response = "desculpe, ocorreu um erro ao processar sua mensagem"
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({'role': 'assistant', 'content': full_response})





st.markdown("----")

#streamlit run main.py


