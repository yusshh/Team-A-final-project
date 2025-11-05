# app.py (Final Polished Version with About at Bottom)
import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# === Path Setup ===
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

# === Import Local Pipeline ===
from src.combinedPipeline import SummarizationPipeline

# === Load Environment Variables ===
load_dotenv(SRC_DIR / ".env")
HF_TOKEN = os.getenv("HF_API_KEY")

# === Streamlit Page Setup ===
st.set_page_config(
    page_title="AI Text Summarizer and Paraphraser",
    page_icon="📝",
    layout="wide"
)

# === Custom CSS Styling ===
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-weight: 600;
    transition: 0.25s;
}
.stButton>button:hover {
    transform: scale(1.03);
}

/* Output box */
.output-box {
    background: #f7f9fc;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
    min-height: 300px;
}

/* Sidebar About Section */
.about-box {
    background: #f9fafb;
    padding: 1rem;
    border-radius: 12px;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.about-box summary {
    font-weight: 700;
    cursor: pointer;
    font-size: 1rem;
    margin-bottom: 0.25rem;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    transition: background 0.2s;
}
.about-box summary:hover {
    background: #e0e7ff;
}
.about-box ul {
    margin: 0.25rem 0 0.5rem 1rem;
    padding: 0;
    font-size: 0.9rem;
    list-style: none;
}
.about-box ul li::before {
    content: "•";
    color: #6366f1;
    font-weight: bold;
    display: inline-block; 
    width: 1em;
    margin-left: -1em;
}
</style>
""", unsafe_allow_html=True)

# === Function: Save File ===
def save_file(content: str, filename: str):
    """Save text output to Downloads folder."""
    try:
        downloads = Path.home() / "Downloads"
        path = downloads / filename
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return str(path)
    except Exception:
        return None

# === Initialize Session Variables ===
for key in ("text_input", "text_output", "mode"):
    if key not in st.session_state:
        st.session_state[key] = ""

# === API Key Check ===
if not HF_TOKEN:
    st.error("⚠️ Missing Hugging Face API Key. Add it in `src/.env`.")
    st.markdown(
        "Get one here: [Hugging Face Tokens](https://huggingface.co/settings/tokens)"
    )
    st.stop()

# === Load Pipeline ===
@st.cache_resource
def get_pipeline():
    return SummarizationPipeline(HF_TOKEN)

try:
    model_pipeline = get_pipeline()
except Exception as e:
    st.error(f"Failed to initialize pipeline: {e}")
    st.stop()

# === Sidebar ===
with st.sidebar:
    st.header("Settings")
    task = st.radio("Select Task", ["Summarization", "Paraphrasing"])
    if task == "Summarization":
        style = st.selectbox("Summarization Type", ["Abstractive", "Extractive"])
        length = st.select_slider("Summary Length", ["Short", "Medium", "Long"], "Medium")
    else:
        style, length = None, None

    st.markdown("---")
    st.success("Hugging Face API Connected")
    st.caption("Using Inference API — no local model download required")

    # === About Section (Bottom of Sidebar) ===
    st.header("About")
    st.markdown("""
    <div class="about-box">
        <details open>
            <summary>🟣 Abstractive Summarization</summary>
            <ul>
                <li>Generates new sentences capturing the meaning of the text.</li>
                <li>Paraphrases original content instead of copying it verbatim.</li>
            </ul>
        </details>
        <details>
            <summary>🔵 Extractive Summarization</summary>
            <ul>
                <li>Selects key sentences from the original text.</li>
                <li>Combines them to form a concise summary without rephrasing.</li>
            </ul>
        </details>
        <details>
            <summary>🟢 Paraphrasing</summary>
            <ul>
                <li>Rewrites text using different words.</li>
                <li>Maintains original meaning while improving readability.</li>
            </ul>
        </details>
    </div>
    """, unsafe_allow_html=True)

# === Main Header (Plain) ===
st.markdown("## 📝 AI Text Summarizer and Paraphraser")
st.markdown("Powered by Hugging Face Inference (no local model download required)")

# === Input Section with Icon ===
st.subheader("🖊️ Input Text")
input_text = st.text_area(
    "Enter your text below:",
    value=st.session_state.text_input,
    height=250,
    label_visibility="collapsed"
)
st.session_state.text_input = input_text

col1, col2, col3 = st.columns(3)
run_btn = col1.button("▶️ Run")
clear_btn = col2.button("🧹 Clear")
save_btn = col3.button("💾 Save Output")

if clear_btn:
    for k in st.session_state:
        st.session_state[k] = ""
    st.rerun()

# === Output Section with Icon ===
st.subheader("📄 Output")

if run_btn and input_text:
    with st.spinner("Processing with AI..."):
        try:
            if task == "Summarization":
                result = model_pipeline.summarize(
                    input_text,
                    method=style.lower(),
                    length=length.lower()
                )
                st.session_state.mode = "summary"
            else:
                result = model_pipeline.paraphrase(input_text)
                st.session_state.mode = "paraphrase"

            st.session_state.text_output = result
            st.success("✅ Completed successfully.")
            st.text_area("Result", result, height=300, label_visibility="collapsed")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

elif st.session_state.text_output:
    st.text_area("Previous Output", st.session_state.text_output, height=300, label_visibility="collapsed")
else:
    st.markdown("<div class='output-box'><em>Enter text above and click Run to start...</em></div>", unsafe_allow_html=True)

# === Save Button ===
if save_btn and st.session_state.text_output:
    filename = "AI_output.txt" if st.session_state.mode == "summary" else "AI_paraphrase.txt"
    saved_path = save_file(st.session_state.text_output, filename)
    if saved_path:
        st.success(f"💾 File saved to: {saved_path}")
    else:
        st.error("⚠️ Could not save file")

# === Clean Footer ===
st.markdown("""
<hr style='border: none; height: 2px; background: linear-gradient(90deg, #6a11cb, #2575fc); margin-top: 2rem;'/>
<div style='text-align:center; padding:10px 0; color:#555;'>
    <p style='margin:0; font-size:0.9rem;'>
        Built with <b>Streamlit</b> and <b>Hugging Face Inference API</b><br>
        © 2025 <b>AI Text Summarizer and Paraphraser</b> | All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)