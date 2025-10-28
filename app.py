import streamlit as st
from mvp.combinedPipeline import SummarizationPipeline
import os
from dotenv import load_dotenv

# ---------- Load Local CSS ----------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# Optional animation support
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except Exception:
    LOTTIE_AVAILABLE = False

# ---------- Load Environment ----------
load_dotenv()

# ---------- Page Setup ----------
st.set_page_config(page_title="Text Morph", page_icon="🧠", layout="wide")

# ---------- Custom Header ----------
st.markdown("""
    <style>
    .title {
        font-size: 4rem;
        font-weight: 800;
        text-align: left;
        margin-bottom: 0.3rem;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #818cf8, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(167, 139, 250, 0.4);
    }
    .subtitle {
        font-size: 1.2rem;
        color: #d1d5db !important;
        margin-bottom: 1.5rem;
        opacity: 0.9;
    }
    .footer {
        text-align: center;
        margin-top: 4rem;
        padding: 1rem 0;
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(156, 163, 175, 0.3);
        color: #f3f4f6 !important;
        font-size: 15px;
        box-shadow: 0 -2px 20px rgba(99, 102, 241, 0.2);
    }
    .footer span {
        color: #a78bfa;
        font-weight: 700;
        text-shadow: 0 0 8px rgba(167, 139, 250, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="title">Text Morph</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-powered summarization & paraphrasing — fast, clean, and simple.</div>', unsafe_allow_html=True)
with col2:
    if LOTTIE_AVAILABLE:
        st_lottie(
            {
                "v": "5.5.7",
                "fr": 30,
                "ip": 0,
                "op": 60,
                "w": 200,
                "h": 200,
                "nm": "spark",
                "ddd": 0,
                "assets": [],
                "layers": [],
            },
            height=120,
        )
    else:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)

st.markdown("---")

# ---------- API Key ----------
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    st.error("⚠ Hugging Face API key not found. Please add HF_API_KEY to your .env or Streamlit secrets.")
    st.stop()

# ---------- Pipeline Initialization ----------
@st.cache_resource
def load_pipeline():
    return SummarizationPipeline(HF_API_KEY)

pipeline = load_pipeline()

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙ Settings")
    method = st.radio("Summarization Type", ["Extractive", "Abstractive"], index=1)
    length = st.select_slider("Summary Length", ["Short", "Medium", "Long"], value="Medium")
    st.markdown("---")
    st.info("✅ API Connected")

    # ---------- About Section ----------
    st.markdown(
        """
        <div class="about-section">
            <h2>🧠 About My App</h2>
            <p>
                This AI-powered Text Summarizer and Paraphraser helps you quickly condense large text 
                into concise summaries or rephrase it for better readability. 
                It’s built using <b>Streamlit</b> and <b>Natural Language Processing (NLP)</b> models.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    

# ---------- Layout ----------
left, right = st.columns([1.1, 1])

# ---------- Input Section ----------
with left:
    st.subheader("📝 Input")
    input_text = st.text_area("Paste or type your text here", height=320, placeholder="Paste article, paragraph, or notes…")

    c1, c2, c3 = st.columns(3)
    with c1:
        summarize_btn = st.button("✨ Summarize", use_container_width=True)
    with c2:
        paraphrase_btn = st.button("🔄 Paraphrase", use_container_width=True)
    with c3:
        clear_btn = st.button("🧹 Clear")

    if clear_btn:
        st.session_state.clear()
        st.experimental_rerun()

# ---------- Output Section ----------
with right:
    st.subheader("📊 Output")

    if summarize_btn and input_text:
        with st.spinner("🔄 Summarizing your text... Please wait."):
            try:
                summary = pipeline.summarize(
                    input_text, method=method.lower(), length=length.lower()
                )
                st.success("✅ Summary Generated!")
                st.markdown(
                    f"<div class='output-card'><h4>🧠 Summary</h4><p>{summary}</p></div>",
                    unsafe_allow_html=True,
                )

                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.download_button(
                        "⬇ Download Summary",
                        summary,
                        file_name="summary.txt",
                        mime="text/plain",
                    )
                with col_d2:
                    st.button("📋 Copy", key="copy_summary")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    elif paraphrase_btn and input_text:
        with st.spinner("🔁 Paraphrasing your text... Please wait."):
            try:
                paraphrased_text = pipeline.paraphrase(input_text)
                st.success("✅ Paraphrased Successfully!")
                st.markdown(
                    f"<div class='output-card'><h4>✏ Paraphrased Text</h4><p>{paraphrased_text}</p></div>",
                    unsafe_allow_html=True,
                )

                st.download_button(
                    "⬇ Download Paraphrased",
                    paraphrased_text,
                    file_name="paraphrased.txt",
                    mime="text/plain",
                )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    else:
        st.info("👈 Enter text and click Summarize or Paraphrase to see results here.")

        # ---------- Footer Section ----------
st.markdown(
    """
    <div class='footer'>
        Made with ❤ by <span>Ayush</span>
    </div>
    """,
    unsafe_allow_html=True
)