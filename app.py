import streamlit as st
<<<<<<< HEAD
from mvp.mvp_pipeline import SummarizationPipeline
import os
from dotenv import load_dotenv

# Load env & page settings
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="TextMorph - Advanced Text Summarization and Paraphrasing",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Streamlit-safe CSS + HTML
CUSTOM_STYLE = r"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">

<style>
:root {
  --glass-bg: rgba(255,255,255,0.08);
  --glass-border: rgba(255,255,255,0.1);
  --muted: rgba(255,255,255,0.78);
  --shadow-glow: rgba(99,102,241,0.2);
}

/* page base */
html, body, [class*="css"] {
  height: 100%;
  font-family: 'Inter', sans-serif;
  background: #020617;
  color: #fff;
  overflow-x: hidden;
}

/* full-screen animated gradient layer */
.rainbow-wrap {
  position: fixed;
  inset: 0;
  z-index: -3;
  overflow: hidden;
  pointer-events: none;
  background: #020617;
}

/* animated flowing gradient */
.rainbow-bg {
  position: absolute;
  inset: -30% -30%;
  background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(6,182,212,0.2), rgba(236,72,153,0.18), rgba(59,130,246,0.18));
  filter: blur(80px) saturate(1.3);
  transform: rotate(0deg) scale(1.2);
  animation: floatGradient 16s ease-in-out infinite;
  opacity: 0.95;
}

.rainbow-bg.two {
  background: linear-gradient(210deg, rgba(99,102,241,0.22), rgba(20,184,166,0.18), rgba(244,63,94,0.16), rgba(14,165,233,0.15));
  animation-duration: 24s;
  mix-blend-mode: screen;
  filter: blur(100px) saturate(1.4);
  transform: rotate(30deg) scale(1.4);
  opacity: 0.92;
}

@keyframes floatGradient {
  0% { transform: translateX(-8%) translateY(0) rotate(0deg) scale(1.1); }
  50% { transform: translateX(8%) translateY(-4%) rotate(5deg) scale(1.15); }
  100% { transform: translateX(-8%) translateY(0) rotate(0deg) scale(1.1); }
}

/* particle / orb layer */
.orb-layer {
  position: absolute;
  inset: 0;
  z-index: -2;
  pointer-events: none;
}

/* orbital shapes (colored, soft glows) */
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(30px) saturate(1.2);
  opacity: 0.55;
  mix-blend-mode: screen;
  animation: drift 24s ease-in-out infinite;
}
.orb.small { width: 90px; height: 90px; }
.orb.mid   { width: 180px; height: 180px; }
.orb.large { width: 360px; height: 360px; }

.orb.one { background: rgba(124,58,237,0.22); top: 15%; left: 8%; animation-duration: 30s; }
.orb.two { background: rgba(6,182,212,0.16); top: 65%; left: 15%; animation-duration: 26s; }
.orb.three { background: rgba(236,72,153,0.12); top: 35%; left: 70%; animation-duration: 20s; }
.orb.four { background: rgba(59,130,246,0.12); top: 75%; left: 85%; animation-duration: 38s; }
.orb.five { background: rgba(14,165,233,0.1); top: 50%; left: 40%; animation-duration: 44s; }

@keyframes drift {
  0% { transform: translateY(0) translateX(0) scale(1); opacity: 0.65; }
  25% { transform: translateY(-5%) translateX(3%) scale(1.06); opacity: 0.9; }
  50% { transform: translateY(3%) translateX(-6%) scale(0.94); opacity: 0.6; }
  75% { transform: translateY(5%) translateX(5%) scale(1.03); opacity: 0.85; }
  100% { transform: translateY(0) translateX(0) scale(1); opacity: 0.65; }
}

/* subtle star-like moving dots */
.star-field {
  position: absolute;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background-image: radial-gradient(circle at 15% 25%, rgba(255,255,255,0.04) 1.2px, transparent 2.2px),
                    radial-gradient(circle at 45% 65%, rgba(255,255,255,0.03) 1.2px, transparent 2.2px),
                    radial-gradient(circle at 75% 35%, rgba(255,255,255,0.03) 1.2px, transparent 2.2px);
  background-size: 220px 220px;
  animation: starMove 50s linear infinite;
  opacity: 0.6;
}
@keyframes starMove { 0% { background-position: 0 0; } 100% { background-position: 900px -900px; } }

/* container cards (enhanced glass effect) */
.stApp .neo-card {
  background: rgba(10,12,24,0.5);
  border-radius: 18px;
  padding: 24px;
  border: 1px solid var(--glass-border);
  box-shadow: 0 12px 40px rgba(2,6,23,0.65), 0 0 20px var(--shadow-glow);
  backdrop-filter: blur(10px) saturate(1.2);
  transition: transform 0.3s cubic-bezier(.2,.8,.2,1), box-shadow 0.3s;
}
.stApp .neo-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 28px 64px rgba(3,8,32,0.8), 0 0 24px var(--shadow-glow);
}

/* header */
.header-row {
  display: flex;
  align-items: center;
  gap: 14px;
}
.app-title {
  font-weight: 800;
  font-size: 24px;
  margin: 0;
}
.app-sub {
  color: var(--muted);
  margin: 0;
  font-size: 14px;
}

/* buttons */
div.stButton > button {
  border: none;
  border-radius: 14px;
  padding: 0.7rem 1.2rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  background: linear-gradient(90deg, rgba(124,58,237,1), rgba(6,182,212,1));
  color: white;
  box-shadow: 0 8px 20px rgba(6,182,212,0.15);
}
div.stButton > button:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 34px rgba(99,102,241,0.18);
}

/* text areas and outputs */
textarea, .stTextArea textarea {
  border-radius: 12px !important;
  padding: 14px !important;
  background: rgba(255,255,255,0.03) !important;
  color: #fff !important;
  border: 1px solid var(--glass-border) !important;
}

/* small helpers */
.muted { color: var(--muted); font-size: 14px; }
.section-title { font-weight: 700; margin-bottom: 8px; font-size: 18px; }

/* responsive tweaks */
@media (max-width: 880px) {
  .header-row { flex-direction: column; align-items: flex-start; gap: 8px; }
  .app-title { font-size: 20px; }
  .stApp .neo-card { padding: 18px; }
}
</style>

<!-- Animated background layers -->
<div class="rainbow-wrap" aria-hidden="true">
  <div class="rainbow-bg"></div>
  <div class="rainbow-bg two"></div>
  <div class="orb-layer">
    <div class="orb large one"></div>
    <div class="orb mid two"></div>
    <div class="orb mid three"></div>
    <div class="orb large four"></div>
    <div class="orb small five"></div>
  </div>
  <div class="star-field"></div>
</div>
"""

st.markdown(CUSTOM_STYLE, unsafe_allow_html=True)


# Helper: pipeline loader
@st.cache_resource
def get_pipeline():
    return SummarizationPipeline()

# If API key missing -> stop with an explanation (clean)
if not HF_API_KEY:
    st.markdown(
        "<div class='neo-card'><h3 style='margin:0'>⚠️ Missing Hugging Face API Key</h3>"
        "<p class='muted'>Add <code>HF_API_KEY</code> to your .env and restart. The UI is ready and colorful; the backend needs the key.</p></div>",
        unsafe_allow_html=True
    )
    st.stop()

# Try to initialize the pipeline, but don't crash the page if it fails
try:
    pipeline = get_pipeline()
    pipeline_ready = True
except Exception as e:
    pipeline = None
    pipeline_ready = False
    st.error(f"Failed to initialize SummarizationPipeline: {str(e)}")

# -------------------------
# App header + sidebar
# -------------------------
st.markdown(
    "<div class='neo-card' style='margin-bottom:16px;'>"
    "<div class='header-row'>"
    "<div style='display:flex;flex-direction:column;'>"
    "<div style='display:flex;align-items:center;gap:12px;'>"
    "<div style='font-size:30px'>🧬</div>"
    "<div><div class='app-title'>TextMorph - Advanced Text Summarization and Paraphrasing</div>"
    "<div class='muted'>Colorful background • glass UI • Hugging Face inference</div></div>"
    "</div>"
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

# Sidebar controls (retain original options)
with st.sidebar:
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.header("⚙️ Controls")
    method = st.radio("Summarization Method", ["Extractive", "Abstractive"], index=1)
    length = st.select_slider("Summary Length", ["Short", "Medium", "Long"], value="Medium")
    st.markdown("---")
    st.markdown("### 🔐 API Status")
    if pipeline_ready:
        st.success("✓ Pipeline ready")
        st.caption(f"Key: {HF_API_KEY[:8]}...{HF_API_KEY[-4:]}")
    else:
        st.error("Pipeline failed to initialize — check logs")
    st.markdown("---")
    st.markdown("<div class='muted'>Theme: Chromatic • Animations: CSS</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Main columns
# -------------------------
col1, col2 = st.columns([1.1, 1])
with col1:
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📄 Input</div>", unsafe_allow_html=True)
    input_text = st.text_area("Paste the text to summarize or paraphrase", height=320, placeholder="Enter long article, notes, or meeting transcript...")

    ##1st chnage 
    # --- Input text stats ---
    if input_text:
        input_words = len(input_text.split())
        input_chars = len(input_text)
        st.caption(f"📝 **Input Stats:** {input_words} words | {input_chars} characters")


    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1,1])
=======
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
>>>>>>> c5d7e95f3717af68b93e0cf92388076031fa494d
    with c1:
        summarize_btn = st.button("✨ Summarize", use_container_width=True)
    with c2:
        paraphrase_btn = st.button("🔄 Paraphrase", use_container_width=True)
<<<<<<< HEAD
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 Output</div>", unsafe_allow_html=True)

    if 'last_action' not in st.session_state:
        st.session_state.last_action = None

    if summarize_btn:
        st.session_state.last_action = 'summarize'
    if paraphrase_btn:
        st.session_state.last_action = 'paraphrase'

    if not input_text:
        st.info("👈 Paste some text in the left panel and choose Summarize or Paraphrase.")
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.write("Quick sample ideas to try:")
        st.markdown("- Meeting notes (5-15 paragraphs)\n- Blog post draft\n- Research paper abstract + intro")
    else:
        if st.session_state.last_action == 'summarize':
            if not pipeline_ready:
                st.error("Summarization backend not available. Check API key and pipeline logs.")
            else:
                with st.spinner("Generating summary..."):
                    try:
                        summary = pipeline.summarize(input_text, method=method.lower(), length=length.lower())
                        if isinstance(summary, str) and (summary.startswith("Error") or summary.startswith("API Error")):
                            st.error(summary)
                        else:
                            st.success("✅ Summary ready")
                            st.text_area("Summary", value=summary, height=320)
                            #2nd change
                            # --- Summary stats ---
                            summary_words = len(summary.split())
                            summary_chars = len(summary)
                            st.caption(f"📊 **Summary Stats:** {summary_words} words | {summary_chars} characters")

                            # Optional: show word reduction %
                            reduction = ((len(input_text.split()) - summary_words) / len(input_text.split())) * 100
                            st.info(f"🧾 Word Reduction: {reduction:.2f}%")



                            st.download_button("⬇️ Download Summary", data=summary, file_name="summary.txt", mime="text/plain")
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
        elif st.session_state.last_action == 'paraphrase':
            if not pipeline_ready:
                st.error("Paraphrase backend not available. Check API key and pipeline logs.")
            else:
                with st.spinner("Paraphrasing..."):
                    try:
                        paraphrased = pipeline.paraphrase(input_text)
                        if isinstance(paraphrased, str) and (paraphrased.startswith("Error") or paraphrased.startswith("API Error")):
                            st.error(paraphrased)
                        else:
                            st.success("✅ Paraphrase ready")
                            st.text_area("Paraphrased Text", value=paraphrased, height=320)
                            #3rd change
                            # --- Paraphrased stats ---
                            para_words = len(paraphrased.split())
                            para_chars = len(paraphrased)
                            st.caption(f"📊 **Paraphrased Stats:** {para_words} words | {para_chars} characters")


                            st.download_button("⬇️ Download Paraphrase", data=paraphrased, file_name="paraphrase.txt", mime="text/plain")
                    except Exception as e:
                        st.error(f"Error paraphrasing: {str(e)}")
        else:
            st.info("Press Summarize or Paraphrase after entering text.")

    st.markdown("</div>", unsafe_allow_html=True)


# Footer

st.markdown(
    '<div style="margin-top:20px;text-align:center;color:rgba(255,255,255,0.7);font-size:14px;">'
    "Built with 💜 —  TextMorph • Powered by Hugging Face"
    "</div>",
    unsafe_allow_html=True,
)
=======
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
>>>>>>> c5d7e95f3717af68b93e0cf92388076031fa494d
