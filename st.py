import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json
st.set_page_config(
    page_title="代码小助手",
    page_icon="./ruishao/e8dc8bad6d56d367f4f8e79204140a4d.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.runoob.com/',
        'Report a bug': "https://www.bilibili.com/video/BV1ox4y1e71S?vd_source=14569b9a1c46b1aa05f666d2c0b941b6",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.title("代码小助手")
def get_time():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")
def save_session():
    if st.session_state.time:
        session_zj = {
            'time': st.session_state.time,
            'message': st.session_state.message
        }
        if not os.path.exists('session'):
            os.mkdir('session')

        with open(f'session/{st.session_state.time}.json', 'w', encoding='utf-8') as f:
            json.dump(session_zj, f, ensure_ascii=False, indent=2)
def load_session():
    session_list = []
    if os.path.exists('session'):
        for file in os.listdir('session'):
            if file.endswith('.json'):
                session_list.append(file[:-5])
    return session_list

def load_sessions(session_name):
    try:
        with open(f'session/{session_name}.json', 'r', encoding='utf-8') as f:
            session_zj = json.load(f)
            st.session_state.time = session_name
            st.session_state.message = session_zj['message']
    except:
        st.error("会话不存在")
def sc_session(session_name):
    if os.path.exists(f'session/{session_name}.json'):
        os.remove(f'session/{session_name}.json')
        if st.session_state.time == session_name:
            st.session_state.time = get_time()
            st.session_state.message = []

xitong_prompt='你是一个回答python代码知识的助手'

if 'message' not in st.session_state:
    st.session_state.message = []

if 'time' not in st.session_state:
    st.session_state.time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

st.text(f'当前会话:{st.session_state.time}')

for message in st.session_state.message:
    st.chat_message(message['role']).write(message['content'])

with st.sidebar :

    st.subheader("控制面板")

    if st.button('新建会话',width="stretch"):
        save_session()

        if st.session_state.message:
            st.session_state.message = []
            st.session_state.time = get_time()
            save_session()
            st.rerun()
    st.text('会话历史')
    session_list=load_session()
    for session in session_list:
        c1, c2 = st.columns([4, 1])
        with c1:
            if st.button(session, width="stretch", key=f"load_{session}",type="primary" if session==st.session_state.time else 'secondary'):
                load_sessions(session)
                st.rerun ()
        with c2:
            if st.button('', width="stretch", icon='❌️', key=f"del_{session}"):
                sc_session(session)
                st.rerun()

prompt=st.chat_input('请输入')

if prompt:
    st.chat_message("user").write(prompt)

    st.session_state.message.append({'role': 'user', 'content': prompt})

    client = OpenAI(api_key='sk-64a9242efc1149b6ade21c6029139aa0', base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": xitong_prompt},
            *st.session_state.message,
        ],
        stream=True
    )
    rq=st.empty()

    responsefull=''

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content=chunk.choices[0].delta.content
            responsefull+=content
            rq.chat_message("assistant").write(responsefull)

    st.session_state.message.append({'role': 'assistant', 'content':responsefull})
    save_session()

    print('调用的结果',responsefull)





