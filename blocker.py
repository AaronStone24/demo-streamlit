import streamlit as st
import time

if "run_long_task" not in st.session_state:
    st.session_state.run_long_task = False
if "count" not in st.session_state:
    st.session_state.count = 0

def toggle_state(var_name):
    st.session_state[var_name] = not st.session_state[var_name]

st.title("Blocking Example")

with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Trigger long task", on_click=toggle_state, args=["run_long_task",])
        if st.session_state.get("run_long_task", False):
            st.write("Starting a long task....")
            time.sleep(5)
            st.write("Done!")
            toggle_state("run_long_task")
    with col2:
        if st.button("Increase count"):
            st.session_state.count += 1
        st.write(f"Count: {st.session_state.count}")
