import streamlit as st
from groq import Groq

# Set page configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)

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
