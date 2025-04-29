import streamlit as st
from utils import delay
import asyncio

if "run_long_task" not in st.session_state:
    st.session_state.run_long_task = False
if "count" not in st.session_state:
    st.session_state.count = 0

def run_task_clbk():
    if not st.session_state.run_long_task:
        st.session_state.run_long_task = True

async def task():
    st.write("Starting a long task....")
    st.session_state.run_long_task = False
    sec = await delay(5)
    print(sec)
    st.write("Done!")

st.title("Asyncio Example")

async def main():
    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("Trigger long task", on_click=run_task_clbk)
            if st.session_state.get("run_long_task", False):
                await task()
        with col2:
            if st.button("Increase count"):
                st.session_state.count += 1
            st.write(f"Count: {st.session_state.count}")

asyncio.run(main())