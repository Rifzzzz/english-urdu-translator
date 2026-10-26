
import html
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="English to Urdu Translator",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 English to Urdu Translator")
st.write("Translate English text into natural Urdu using AI.")

english_text = st.text_area(
    "Enter English text:",
    placeholder="Type your English text here...",
    height=150
)

if st.button("Translate to Urdu", type="primary"):
    if not english_text.strip():
        st.warning("Please enter some English text first.")
    else:
        try:
            client = Groq(
                api_key=st.secrets["GROQ_API_KEY"]
            )

            with st.spinner("Translating..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Translate the user's text from English "
                                "into natural, accurate Urdu using Urdu "
                                "script. Preserve the original meaning. "
                                "Return only the Urdu translation."
                            )
                        },
                        {
                            "role": "user",
                            "content": english_text.strip()
                        }
                    ]
                )

                translation = (
                    response.choices[0].message.content
                )

            st.subheader("Urdu Translation")

            safe_translation = html.escape(translation or "")
            safe_translation = safe_translation.replace(
                "\n", "<br>"
            )

            st.markdown(
                f'<div dir="rtl" style="text-align:right; '
                f'font-size:22px; line-height:1.9;">'
                f'{safe_translation}</div>',
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Translation failed: {e}")
