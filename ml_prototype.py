import time
import random
import asyncio
import threading
import streamlit as st
from utils import delay
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

async def fetch_live_stock_price():
    await asyncio.sleep(1) # Simulate API request delay
    return round(random.uniform(100, 200), 2)

def train_model():
    loop = asyncio.new_event_loop()
    st.session_state.training_status = 0
    for i in range(5):
        stock_price = loop.run_until_complete(fetch_live_stock_price())
        st.session_state.stock_prices.append(stock_price + st.session_state.stock_price_correction)
        print(f"Current stock price: {stock_price}")
        time.sleep(2) # Simulate model training computations
        st.session_state.training_progress = (i + 1) * 20
        print(f"Training Progress: {st.session_state.training_progress}")
    st.session_state.training_status = 1
    loop.close()
    
if "training_progress" not in st.session_state:
    st.session_state.training_progress = 0
if "training_status" not in st.session_state:
    # -1 -> training not started, 0 -> under progress, 1 -> training complete
    st.session_state.training_status = -1
if "stock_prices" not in st.session_state:
    st.session_state.stock_prices = []
if "stock_price_correction" not in st.session_state:
    st.session_state.stock_price_correction = 0

st.set_page_config(layout="wide")
st.title("Live Stock Dashboard + Background Training Demo")

@st.fragment(run_every=0.5)
def live_feed():
    if st.session_state.training_status == 0:
        if "progress_placeholder" not in st.session_state:
            st.session_state.progress_placeholder = st.empty()
        with st.session_state.progress_placeholder.container():
            st.progress(st.session_state.training_progress, text="Training under progress. Please wait.")
    with st.container():
        if st.session_state.training_status == -1:
            st.info("No training under progress")
        elif st.session_state.training_status == 1:
            st.session_state.progress_placeholder = st.empty()
            st.success("Training Completed!")
    
    st.divider()
    with st.container():
        if len(st.session_state.stock_prices):
            st.write(f"Average stock price: {sum(st.session_state.stock_prices) / len(st.session_state.stock_prices)}")

with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Start Training Model"):
            thread = threading.Thread(target=train_model)
            ctx = get_script_run_ctx()
            add_script_run_ctx(thread, ctx)
            thread.start()
        
        time.sleep(0.1)
        live_feed()

    with col2:
        if st.button("Increase Correction"):
            st.session_state.stock_price_correction += 5
        if st.button("Decrease Correction"):
            st.session_state.stock_price_correction -= 5
        st.write(f"Current stock price correction: {st.session_state.stock_price_correction}")
        