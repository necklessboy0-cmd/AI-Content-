import streamlit as st
from groq import Groq

# Set page configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)

# Custom CSS for Gold-to-Dark-Gold Gradient with Twinkling Stars Background
custom_css = """
<style>
/* Main app background gradient */
.stApp {
    background: linear-gradient(180deg, #D4AF37 0%, #AA771C 40%, #5B3A00 70%, #1A1100 100%);
    background-attachment: fixed;
    color: #FFFFFF;
    position: relative;
    overflow-x: hidden;
}

/* Twinkling background stars layer */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    background-image: 
        radial-gradient(2px 2px at 20px 30px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 40px 70px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1px 1px at 90px 40px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 160px 120px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1.5px 1.5px at 230px 190px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 310px 80px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1px 1px at 370px 150px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 450px 220px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1.5px 1.5px at 520px 60px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 600px 180px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1px 1px at 680px 280px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 750px 110px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1.5px 1.5px at 820px 240px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 900px 50px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1px 1px at 960px 200px, #ffffff, rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 1000px 400px;
    opacity: 0.85;
    z-index: 0;
}

/* Glassmorphism content container */
div[data-testid="stVerticalBlock"] > div {
    z-index: 1;
}

/* Card styling for inputs and controls */
.stSelectbox, .stTextInput, .stTextArea {
    background-color: rgba(20, 15, 5, 0.4);
    border-radius: 10px;
    padding: 8px;
    backdrop-filter: blur(5px);
}

/* Typography styles */
h1 {
    color: #FFF8DC !important;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
    font-weight: 700 !important;
}

.stCaption {
    color: #F0E68C !important;
    font-weight: 500;
}

/* Custom button styling */
div.stButton > button {
    background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
    color: #1A1100 !important;
    font-weight: bold !important;
    border: 1px solid #FFE4B5 !important;
    border-radius: 10px !important;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.3s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 6px 20px rgba(255, 215, 0, 0.6) !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("✍️ AI Content Assistant")
st.caption("Generate tailored social media posts, captions, and hashtags instantly.")

# Retrieve API key securely from Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing from Streamlit Secrets. Please configure secrets in app dashboard.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# User Input Controls
col1, col2 = st.columns(2)

with col1:
    content_type = st.selectbox(
        "Content Type",
        ["Social Media Post", "Blog Intro", "Product Announcement", "Newsletter Snippet", "Short Video Script"]
    )
    platform = st.selectbox(
        "Target Platform",
        ["LinkedIn", "Instagram", "X (Twitter)", "Facebook", "YouTube Shorts / TikTok"]
    )

with col2:
    tone = st.selectbox(
        "Tone / Style",
        ["Professional", "Casual & Engaging", "Witty & Humorous", "Educational", "Persuasive / Sales"]
    )
    target_audience = st.text_input(
        "Target Audience",
        placeholder="e.g., Tech Professionals, Fitness Enthusiasts, Students"
    )

topic = st.text_area(
    "Topic / Core Message",
    placeholder="e.g., Introducing our new AI product that helps developers automate unit tests...",
    height=100
)

# Generate Button
if st.button("Generate Content", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a topic or core message before generating.")
    else:
        # Construct the Prompt
        prompt = f"""
You are an expert social media content creator and copywriter.
Generate a complete post based on the following requirements:

- **Content Type:** {content_type}
- **Platform:** {platform}
- **Tone:** {tone}
- **Target Audience:** {target_audience if target_audience else "General Public"}
- **Topic:** {topic}

### Instructions:
1. Provide a strong hook that captures attention.
2. Structure the body content to match the chosen platform (e.g., appropriate line breaks, formatting).
3. Conclude with a clear Call to Action (CTA).
4. Provide a section at the bottom with 5–8 highly relevant, high-performing hashtags.
"""

        with st.spinner("Drafting your post with Groq AI..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": "You are a professional social media content assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                generated_content = response.choices[0].message.content

                st.subheader("🎉 Your Generated Content")
                st.markdown(generated_content)

            except Exception as e:
                st.error(f"An error occurred while generating content: {e}")
