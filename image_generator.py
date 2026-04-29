import os
import streamlit as st

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

# ---------- API KEY ----------
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        api_key = None

client = None
if OPENAI_AVAILABLE and api_key:
    client = OpenAI(api_key=api_key)


def generate_ai_image(scenario):
    if client is None:
        print("No API → skipping AI image")
        return None

    try:
        prompt = f"Generate a funny meme-style image for: {scenario}"

        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        import base64
        image_bytes = response.data[0].b64_json

        os.makedirs("outputs", exist_ok=True)
        filename = "outputs/ai_generated.png"

        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_bytes))

        return filename

    except Exception as e:
        print("AI image error:", e)
        return None