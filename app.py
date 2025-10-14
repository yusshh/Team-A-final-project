import streamlit as st
from mvp.combinedPipeline import SummarizationPipeline
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Text Morph",
    page_icon="📝",
    layout="wide"
)

# Get API key from environment
HF_API_KEY = os.getenv('HF_API_KEY')

if not HF_API_KEY:
    st.error("⚠️ Hugging Face API key not found! Please add HF_API_KEY to your .env file")
    st.info("Get your API key from: https://huggingface.co/settings/tokens")
    st.stop()

# Initialize pipeline
@st.cache_resource
def load_pipeline():
    return SummarizationPipeline(HF_API_KEY)

try:
    pipeline = load_pipeline()
except Exception as e:
    st.error(f"Failed to initialize pipeline: {str(e)}")
    st.stop()

# Header
st.title("📝 Text Morph ")
st.markdown("🚀 **Created by Ayush** - Advanced Text Summarization and Paraphrasing")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    method = st.radio(
        "Summarization Method",
        ["Extractive", "Abstractive"],
        help="Extractive: Selects important sentences. Abstractive: Generates new summary."
    )
    
    length = st.select_slider(
        "Summary Length",
        options=["Short", "Medium", "Long"],
        value="Medium"
    )
    
    st.markdown("---")
    st.markdown("### 🔑 API Status")
    if HF_API_KEY:
        st.success("✓ API Key Loaded")
    
    st.markdown("---")
    st.markdown("### About")
    st.info(
        "**No Downloads Required!**\n\n"
        "Uses Hugging Face Inference API\n\n"
        "**Extractive**: Picks key sentences\n\n"
        "**Abstractive**: Creates new sentences"
    )

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Input Text")
    input_text = st.text_area(
        "Paste your text here",
        height=300,
        placeholder="Enter the text you want to summarize or paraphrase..."
    )
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        summarize_btn = st.button("✨ Summarize", use_container_width=True, type="primary")
    
    with col_btn2:
        paraphrase_btn = st.button("🔄 Paraphrase", use_container_width=True)

with col2:
    st.subheader("📊 Output")
    
    if summarize_btn and input_text:
        with st.spinner("🔄 Calling Hugging Face API..."):
            try:
                summary = pipeline.summarize(
                    input_text,
                    method=method.lower(),
                    length=length.lower()
                )
                
                if summary.startswith("❌") or summary.startswith("⚠️"):
                    st.error(summary)
                else:
                    st.success("✅ Summary Generated!")
                    st.text_area("Summary", summary, height=300, key="summary_output")
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Summary",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif paraphrase_btn and input_text:
        with st.spinner("🔄 Calling Groq API..."):
            try:
                paraphrased = pipeline.paraphrase(input_text)
                
                if paraphrased.startswith("❌") or paraphrased.startswith("⚠️"):
                    st.error(paraphrased)
                else:
                    st.success("✅ Text Paraphrased!")
                    st.text_area("Paraphrased Text", paraphrased, height=300, key="paraphrase_output")
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Paraphrase",
                        data=paraphrased,
                        file_name="paraphrase.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif not input_text:
        st.info("👈 Enter some text and click a button to get started!")
        
        # Show API info
        st.markdown("### 🌟 Features")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("""
            ✓ API-based processing  
            ✓ No model downloads  
            ✓ Fast cloud inference  
            """)
        
        with col_b:
            st.markdown("""
            ✓ Secure API keys  
            ✓ Multiple models  
            ✓ Real-time results  
            """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Built with Streamlit • Powered by Hugging Face API • No Local Models Required"
    "</div>",
    unsafe_allow_html=True
)