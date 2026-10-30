"""CodeAlpha Task 1 - Language Translation Tool (Streamlit + Microsoft Translator)."""

import html
import io

import streamlit as st
from gtts import gTTS

from translator import AUTO_DETECT, LANGUAGES, TranslationError, is_configured, translate

CODE_TO_NAME = {code: name for name, code in LANGUAGES.items()}
# gTTS uses slightly different codes for a few languages
GTTS_CODES = {"zh-Hans": "zh-CN"}
RTL_LANGUAGES = {"ar", "fa", "ur"}

st.set_page_config(page_title="Language Translator", page_icon="🌐", layout="wide")

# ---------- session state ----------
st.session_state.setdefault("source_lang", AUTO_DETECT)
st.session_state.setdefault("target_lang", "French")
st.session_state.setdefault("input_text", "")
st.session_state.setdefault("result", None)


def swap_languages():
    source = st.session_state.source_lang
    if source == AUTO_DETECT:
        # Fall back to the detected language from the last translation, if any
        detected = (st.session_state.result or {}).get("detected")
        source = CODE_TO_NAME.get(detected)
        if not source:
            return
    st.session_state.source_lang, st.session_state.target_lang = (
        st.session_state.target_lang,
        source,
    )
    # Move the last translation into the input box
    if st.session_state.result:
        st.session_state.input_text = st.session_state.result["text"]
        st.session_state.result = None


@st.cache_data(show_spinner=False)
def text_to_speech(text: str, lang_code: str) -> bytes:
    buffer = io.BytesIO()
    gTTS(text=text, lang=GTTS_CODES.get(lang_code, lang_code)).write_to_fp(buffer)
    return buffer.getvalue()


# ---------- header ----------
st.title("🌐 Language Translation Tool")
st.caption("Powered by Microsoft Translator · CodeAlpha AI Internship — Task 1")

if not is_configured():
    st.warning(
        "Microsoft Translator is not configured. Copy `.env.example` to `.env`, "
        "add your key and region, then restart the app."
    )

# ---------- language selectors ----------
col_src, col_swap, col_tgt = st.columns([5, 1, 5], vertical_alignment="bottom")
with col_src:
    st.selectbox("From", [AUTO_DETECT, *LANGUAGES], key="source_lang")
with col_swap:
    st.button("⇄", on_click=swap_languages, help="Swap languages", use_container_width=True)
with col_tgt:
    st.selectbox("To", list(LANGUAGES), key="target_lang")

# ---------- text areas ----------
col_in, col_out = st.columns(2)

with col_in:
    st.text_area(
        "Text to translate",
        key="input_text",
        height=220,
        max_chars=5000,
        placeholder="Type or paste your text here…",
    )
    translate_clicked = st.button("Translate", type="primary", use_container_width=True)

if translate_clicked:
    source_name = st.session_state.source_lang
    target_code = LANGUAGES[st.session_state.target_lang]
    source_code = None if source_name == AUTO_DETECT else LANGUAGES[source_name]

    if source_code == target_code:
        st.session_state.result = {"text": st.session_state.input_text, "detected": None, "score": None}
    else:
        try:
            with st.spinner("Translating…"):
                st.session_state.result = translate(
                    st.session_state.input_text, target_code, source_code
                )
        except TranslationError as exc:
            st.session_state.result = None
            st.error(str(exc))

with col_out:
    st.markdown("**Translation**")
    result = st.session_state.result
    if result:
        target_code = LANGUAGES[st.session_state.target_lang]
        direction = "rtl" if target_code in RTL_LANGUAGES else "ltr"
        st.markdown(
            f'<div dir="{direction}" style="min-height:180px;padding:1rem;border-radius:0.5rem;'
            'border:1px solid rgba(128,128,128,0.3);font-size:1.1rem;white-space:pre-wrap;">'
            f'{html.escape(result["text"])}</div>',
            unsafe_allow_html=True,
        )

        if result.get("detected"):
            name = CODE_TO_NAME.get(result["detected"], result["detected"])
            score = f" ({result['score']:.0%} confidence)" if result.get("score") else ""
            st.caption(f"Detected language: {name}{score}")

        # Copy: st.code renders a built-in copy-to-clipboard button
        with st.expander("📋 Copy translation"):
            st.code(result["text"], language=None, wrap_lines=True)

        if st.button("🔊 Listen", use_container_width=True):
            try:
                with st.spinner("Generating audio…"):
                    st.audio(text_to_speech(result["text"], target_code), format="audio/mp3")
            except Exception as exc:  # gTTS raises various errors (unsupported lang, network)
                st.error(f"Text-to-speech unavailable for this language: {exc}")
    else:
        st.info("Your translation will appear here.")
