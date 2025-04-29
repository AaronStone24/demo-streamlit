import time
import threading
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

if "task_done" not in st.session_state:
    st.session_state.task_done = False
if "count" not in st.session_state:
    st.session_state.count = 0

def task():
    time.sleep(5)
    st.session_state.task_done = True
    st.session_state.count += 100
    print("Task complete!")

st.title("Threading Example")

with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Trigger long task"):
            thread = threading.Thread(target=task)
            ctx = get_script_run_ctx()
            add_script_run_ctx(thread, ctx)
            thread.start()
        if st.session_state.task_done:
            st.success("Background task completed!")
        else:
            st.info("Task running in the background...")
    with col2:
        if st.button("Increase count"):
            st.session_state.count += 1
        st.write(f"Count: {st.session_state.count}")
