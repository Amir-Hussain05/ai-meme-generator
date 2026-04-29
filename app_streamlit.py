import streamlit as st
from meme_engine import create_meme
from caption_generator import generate_caption
from template_selector import get_template
from image_generator import generate_ai_image
import os

st.set_page_config(page_title="MemeGPT", layout="wide")

if "mode" not in st.session_state:
    st.session_state.mode = "template"

st.title("😂 MemeGPT")
st.write("Create memes using AI 🚀")

scenario = st.text_input("Enter your meme scenario")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📂 Template"):
        st.session_state.mode = "template"

with col2:
    if st.button("🖼 Upload"):
        st.session_state.mode = "upload"

with col3:
    if st.button("🤖 AI Generate"):
        st.session_state.mode = "ai"

mode = st.session_state.mode
st.write("Selected:", mode)

image_path = None

if mode == "template":
    template = st.selectbox(
        "Choose Template",
        ["coding.png", "exam.png", "office.png", "student.png", "cricket.png"]
    )
    image_path = f"templates/{template}"

elif mode == "upload":
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg"])

    if uploaded_file:
        os.makedirs("uploads", exist_ok=True)
        image_path = f"uploads/{uploaded_file.name}"

        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(image_path, width=300)

if st.button("🚀 Generate Meme"):

    if scenario.strip() == "":
        st.warning("Enter a scenario")
    else:
        with st.spinner("Generating meme..."):

            top, bottom, category = generate_caption(scenario)

            if mode == "ai":
                image_path = generate_ai_image(scenario)

                if image_path is None:
                    image_path = f"templates/{get_template(category)}"

            if image_path is None:
                st.error("No image available")
                st.stop()

            output = create_meme(image_path, top, bottom)

        st.image(output, width=350)

        with open(output, "rb") as f:
            st.download_button("Download Meme", f, file_name="meme.png")

st.sidebar.title("Meme History")

if os.path.exists("outputs"):
    images = sorted(os.listdir("outputs"), reverse=True)

    for img in images[:10]:
        if st.sidebar.button(img):
            st.image(f"outputs/{img}")