import streamlit as st
import requests
import re
from googletrans import Translator
from pykakasi import kakasi
import streamlit.components.v1 as components

# ----------------- Helpers -----------------
def contains_kanji(text):
    return bool(re.search(r'[\u4e00-\u9faf]', text))

def translate_word(word):
    try:
        translator = Translator()
        return translator.translate(word, src="en", dest="ja").text
    except:
        return None

def kana_and_romaji(japanese_text):
    kks = kakasi()
    result = kks.convert(japanese_text)

    kana = "".join(item.get("hira", item.get("kana", item["orig"])) for item in result)
    romaji = "".join(item.get("hepburn", item["orig"]) for item in result)
    return kana, romaji

# ----------------- Page -----------------
st.set_page_config(page_title="Random Japanese Word", layout="centered")
st.title("🎌 Random Japanese Word Generator")

# ----------------- Button -----------------
if st.button("Generate Random Word"):

    # Random English word
    try:
        res = requests.get("https://random-word-api.vercel.app/api?words=1")
        english = res.json()[0]
    except:
        st.error("Failed to fetch word")
        st.stop()

    # Translate
    japanese = translate_word(english)
    if not japanese:
        st.error("Translation failed")
        st.stop()

    # Kana & Romaji
    kana, romaji = kana_and_romaji(japanese)
    if not contains_kanji(japanese):
        kana = ""

    # Optional Kana block
    kana_block = ""
    if kana:
        kana_block = f"""
        <div class="inner-card">
            <div class="title">Kana</div>
            <div class="jp-big">{kana}</div>
        </div>
        """

    # ----------------- DISPLAY -----------------
    components.html(
        f"""
        <style>
        :root {{
            --txt: var(--text-color, #e6e6e6);
        }}

        .outer-card {{
            border: 2px solid #6b6b6b;
            border-radius: 16px;
            padding: 18px;
            background: transparent;
            font-family: sans-serif;
            color: var(--txt);
        }}

        .inner-card {{
            border: 1.5px solid #6b6b6b;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 14px;
            text-align: center;
            background: transparent;
        }}

        .title {{
            font-size: 18px;
            font-weight: 600;
            opacity: 0.75;
            margin-bottom: 6px;
            color: var(--txt);
        }}

        .content {{
            font-size: 28px;
            font-weight: 700;
            color: var(--txt);
        }}

        /* BIG FONT FOR JAPANESE & KANA */
        .jp-big {{
            font-size: 42px;
            font-weight: 700;
            letter-spacing: 1px;
            color: var(--txt);
        }}

        .sub {{
            font-size: 18px;
            opacity: 0.85;
            color: var(--txt);
        }}
        </style>

        <div class="outer-card">

            <div class="inner-card">
                <div class="title">English</div>
                <div class="content">{english}</div>
            </div>

            <div class="inner-card">
                <div class="title">Japanese</div>
                <div class="jp-big">{japanese}</div>
            </div>

            {kana_block}

            <div class="inner-card">
                <div class="title">Romaji</div>
                <div class="sub">{romaji}</div>
            </div>

        </div>
        """,
        height=600
    )
