import os
import streamlit as st

# Try importing OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

# ---------- SAFE API KEY HANDLING ----------
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        api_key = None

# ---------- INIT CLIENT ----------
client = None
if OPENAI_AVAILABLE and api_key:
    client = OpenAI(api_key=api_key)


def generate_caption(scenario):
    # 🔁 Fallback (NO API)
    if client is None:
        s = scenario.lower()

        if "debug" in s:
            return "WHEN BUG FIXED", "ANOTHER BUG APPEARS 😂", "coding"
        elif "exam" in s:
            return "STUDY ALL NIGHT", "FORGET EVERYTHING 😭", "exam"
        elif "cricket" in s:
            return "LAST OVER DRAMA", "HEART ATTACK MATCH 😭🔥", "cricket"
        else:
            return "EXPECTATION 😎", "REALITY 🤡", "student"

    # 🤖 AI CAPTION
    prompt = f"""
    Generate a funny meme caption for:
    "{scenario}"

    Rules:
    - Max 10 words
    - Include emojis
    - Format:
    TOP TEXT | BOTTOM TEXT | CATEGORY
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content.strip()
        parts = text.split("|")

        if len(parts) == 3:
            return parts[0].strip(), parts[1].strip(), parts[2].strip().lower()
        else:
            return text, "", "student"

    except Exception as e:
        print("API Error:", e)
        return "SOMETHING WENT WRONG 😅", "", "student"