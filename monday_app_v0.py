# -------------------////------------------///------------------
# monday -- Hybrid version with Gemini API + Ollama Local (Fixed)
# ---------------------by----devak------------------------------
import os
import streamlit as st
import google.generativeai as genai
import time
import requests
import json
import html

# -----------------------------------------------------page metadata
st.set_page_config(page_title="Monday", page_icon="🟣", layout="centered")

# ----------------------------------------------styling
st.markdown(
    """
    <style>
    .stApp{background:#000;min-height:100vh;}
    html,body,[class*="css"]{color:#fff;font-family:'Fira Mono','Menlo',monospace;}
    h1,h2,h3,h4,h5,h6{color:#c084fc;}
    .orange{color:#ff9f43;font-weight:600;}
    .feature-card{border-left:4px solid #ff9f43;padding:0.25rem 0 0.25rem 0.75rem;
                  margin-bottom:0.75rem;background:rgba(192,132,252,0.07);border-radius:0.5rem;}
    .main .block-container{padding-top:2rem;}
    .subtitle{font-style:italic;text-align:center;text-transform:lowercase;color:#bdbdbd;
              font-size:1.1rem;margin-top:-0.5rem;margin-bottom:1.5rem;}
    .core-box{background:rgba(30,0,50,0.18);border:1.5px solid #2d1457;border-radius:1.1rem;
              padding:2.2rem 1.5rem 1.5rem 1.5rem;margin:2rem auto 2.5rem auto;max-width:540px;
              box-shadow:0 2px 16px 0 rgba(80,0,120,0.04);}

    /* Floating navbar (centered, wide) */
    .floating-navbar {
        margin: 2px auto 32px auto;
        background: rgba(30,0,50,0.92);
        border-radius: 1.2rem;
        box-shadow: 0 4px 24px 0 rgba(192,132,252,0.10), 0 0 0 0 #c084fc;
        padding: 0.7rem 2.2rem 0.7rem 2.2rem;
        max-width: 1100px;
        min-width: 320px;
        width: 96vw;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        border: 1.5px solid #2d1457;
        transition: box-shadow 0.2s;
        position: relative;
        left: 50%;
        transform: translateX(-50%);

    .navbar-left {
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }
    .navbar-title {
        color: #c084fc;
        font-style: italic;
        font-size: 1.5rem;
        margin: 0;
        line-height: 1.1;
        letter-spacing: 0.01em;
    }
    .navbar-right {
        color: #bdbdbd;
        font-size: 1.05rem;
        font-style: italic;
        text-transform: lowercase;
        letter-spacing: 0.01em;
        margin: 0;
        text-align: right;
    }
    @media (max-width: 1200px) {
        .floating-navbar {max-width: 98vw; width: 98vw;}
    }
    @media (max-width: 900px) {
        .floating-navbar {max-width: 99vw; width: 99vw;}
    }
    @media (max-width: 600px) {
        .floating-navbar {padding: 0.5rem 0.7rem; min-width: 0; max-width: 100vw; width: 100vw; margin: 16px auto;}
        .navbar-title {font-size: 1.1rem;}
        .navbar-right {font-size: 0.85rem;}
    }

    /* Email Display Styling */
    .email-container {
        background: linear-gradient(135deg, rgba(192,132,252,0.05) 0%, rgba(255,159,67,0.03) 100%);
        border: 1px solid rgba(192,132,252,0.3);
        border-radius: 12px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(192,132,252,0.1);
        position: relative;
        overflow: hidden;
    }

    .email-container::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #c084fc, #ff9f43, #c084fc);
        border-radius: 12px;
        opacity: 0.1;
        z-index: -1;
        animation: pulse 3s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.1; }
        50% { opacity: 0.2; }
    }

    .email-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(192,132,252,0.2);
    }

    .email-label {
        color: #c084fc;
        font-weight: 600;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .email-content {
        color: #ffffff;
        line-height: 1.8;
        font-size: 15px;
        white-space: pre-wrap;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .typewriter {
        overflow: hidden;
        white-space: pre-wrap;
        animation: typing 0.5s steps(1) infinite;
    }

    @keyframes typing {
        from { border-right: 2px solid #ff9f43; }
        to { border-right: 2px solid transparent; }
    }

    .model-selector {
        background: rgba(192,132,252,0.1);
        border: 1px solid rgba(192,132,252,0.3);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 16px;
    }

    .provider-toggle {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 20px;
    }

    .provider-button {
        padding: 8px 20px;
        border-radius: 20px;
        border: 1px solid rgba(192,132,252,0.3);
        background: rgba(192,132,252,0.1);
        color: #c084fc;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .provider-button.active {
        background: rgba(192,132,252,0.3);
        border-color: #c084fc;
    }

    .local-badge {
        background: rgba(76, 175, 80, 0.2);
        color: #4CAF50;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        margin-left: 8px;
    }

    .cloud-badge {
        background: rgba(33, 150, 243, 0.2);
        color: #2196F3;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        margin-left: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Floating navbar
st.markdown(
    """
    <div class="floating-navbar">
        <div class="navbar-left">
            <span class="navbar-title">monday</span>
        </div>
        <div class="navbar-right">your week starts with a better email.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# -----------api configs
GEMINI_API_KEY = "AIzaSyBy-QaFFjpyDwN3cAj1MUMrBHfjKYgG_PI"
OLLAMA_API_URL = "http://localhost:11434"


# ------status and additive helpers
def check_ollama_status():
    """Check if Ollama is running and accessible."""
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


@st.cache_data(ttl=60)  # Cache for 1 minute
def get_ollama_models():
    """Get list of available Ollama models."""
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags")
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
    except:
        pass
    return []


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_gemini_models():
    """Get list of available Gemini models."""
    genai.configure(api_key=GEMINI_API_KEY)
    models = []
    model_info = {}

    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name.split('/')[-1]  # Remove 'models/' prefix
            models.append(model_name)
            model_info[model_name] = {
                'display_name': m.display_name,
                'description': getattr(m, 'description', 'No description available')
            }

    return sorted(models), model_info


def clean_email_text(text):
    """Clean and sanitize email text."""
    # Remove any potential HTML tags or malformed content
    # Remove content between < and >
    import re
    text = re.sub(r'<[^>]+>', '', text)

    # Remove any standalone < or > that might cause issues
    text = text.replace('<', '').replace('>', '')

    # Clean up any other problematic characters
    text = text.strip()

    return text


def generate_email_ollama(topic1, topic2, sender, recipient, tone, model_name, word_count, context, ai_human_scale,
                          return_thought=False):
    """Generate email using Ollama local model. If return_thought is True, return the 'thought' if present."""
    tone_descriptions = {
        "Formal": "formal and professional",
        "Motivated": "enthusiastic and motivating",
        "Concerned": "concerned but constructive",
        "Disappointed": "disappointed but professional"
    }
    style_instruction = """
- If the Human vs AI Style scale is closer to 0, make the email more formal, structured, and neutral (AI-like).
- If the scale is closer to 100, make the email more conversational, warm, and personal (human-like).
- The current scale value is: {ai_human_scale} (0 = AI-like, 100 = human-like).
"""
    prompt = f"""
You are an expert email assistant. The sender is '{sender}' and the recipient is '{recipient}'.
Write a complete, natural, and well-structured email from the sender to the recipient, as if the sender is writing it themselves. The sender is the person sending the email, and the recipient is the person receiving it. The AI should generate the email for the sender to send to the recipient.

Compose an exceptional {tone_descriptions.get(tone, 'professional')} email that:
1. Opens with an appropriate greeting tailored to the recipient's relationship with {sender}
2. Clearly addresses both {topic1} and {topic2} with logical flow between topics
3. Maintains a {tone_descriptions.get(tone, 'professional')} tone throughout
4. Closes with a purposeful conclusion and professional sign-off

Guidelines for excellence:
- Be concise yet thorough (aim for around {word_count} words, but do not stop abruptly at the word limit; write a complete, natural email that feels finished)
- Use professional but natural language appropriate for workplace communication
- Structure with clear paragraph breaks for readability
- Include transitional phrases for smooth topic progression
- End with a clear purpose (request, next steps, or thoughtful closing)
{f'- Additional context: {context}' if context else ''}
{style_instruction}

Format requirements:
>>> Provide subject line, header, body, conclusion and footnote with whatever is most suitable to the given topic lines
>>> Use plain text only (no formatting, HTML, or markdown)
>>> Maintain proper email etiquette throughout
"""

    try:
        response = requests.post(
            f"{OLLAMA_API_URL}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": int(word_count * 1.5)  # rough token estimate
                }
            },
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            # If Ollama returns a 'thought' field, handle it
            thought = data.get('thought', None)
            email_text = data.get('response', '').strip()
            # Clean the text to remove any problematic content
            if return_thought:
                return thought or "No thought available."
            return clean_email_text(email_text)
        else:
            return f"Error: Ollama returned status code {response.status_code}"

    except requests.exceptions.Timeout:
        return "Error: Request timed out. The model might be loading or processing."
    except Exception as e:
        return f"Error generating email with Ollama: {str(e)}"


def generate_email_gemini(topic1, topic2, sender, recipient, tone, model_name, word_count, context, ai_human_scale):
    """Generate email using Gemini API."""
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        model = genai.GenerativeModel(model_name)
    except Exception as e:
        return f"Error loading model {model_name}: {str(e)}"
    tone_descriptions = {
        "Formal": "formal and professional",
        "Motivated": "enthusiastic and motivating",
        "Concerned": "concerned but constructive",
        "Disappointed": "disappointed but professional"
    }
    style_instruction = """
- If the Human vs AI Style scale is closer to 0, make the email more formal, structured, and neutral (AI-like).
- If the scale is closer to 100, make the email more conversational, warm, and personal (human-like).
- The current scale value is: {ai_human_scale} (0 = AI-like, 100 = human-like).
"""
    prompt = f"""
You are an expert email assistant. The sender is '{sender}' and the recipient is '{recipient}'.
Write a complete, natural, and well-structured email from the sender to the recipient, as if the sender is writing it themselves. The sender is the person sending the email, and the recipient is the person receiving it. The AI should generate the email for the sender to send to the recipient.

Compose an exceptional {tone_descriptions.get(tone, 'professional')} email that:
1. Opens with an appropriate greeting tailored to the recipient's relationship with {sender}
2. Clearly addresses both {topic1} and {topic2} with logical flow between topics
3. Maintains a {tone_descriptions.get(tone, 'professional')} tone throughout
4. Closes with a purposeful conclusion and professional sign-off

Guidelines for excellence:
- Be concise yet thorough (aim for around {word_count} words, but do not stop abruptly at the word limit; write a complete, natural email that feels finished)
- Use professional but natural language appropriate for workplace communication
- Structure with clear paragraph breaks for readability
- Include transitional phrases for smooth topic progression
- End with a clear purpose (request, next steps, or thoughtful closing)
{f'- Additional context: {context}' if context else ''}
{style_instruction}

Format requirements:
>>> Provide subject line, header, body, conclusion and footnote with whatever is most suitable to the given topic lines
>>> Use plain text only (no formatting, HTML, or markdown)
>>> Maintain proper email etiquette throughout
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=int(word_count * 1.5),
            )
        )

        return response.text.strip()

    except Exception as e:
        return f"Error generating email: {str(e)}"


def typewriter_effect(text, placeholder):
    """Display text with typewriter effect."""
    # Escape HTML characters to prevent rendering issues
    escaped_text = html.escape(text)
    displayed_text = ""

    for i, char in enumerate(escaped_text):
        displayed_text += char
        placeholder.markdown(
            f"""
            <div class="email-container">
                <div class="email-header">
                    <span class="email-label">📧 Generated Email</span>
                </div>
                <div class="email-content typewriter">{displayed_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.01)  # Adjust speed here

    # Final display without cursor
    placeholder.markdown(
        f"""
        <div class="email-container">
            <div class="email-header">
                <span class="email-label">📧 Generated Email</span>
            </div>
            <div class="email-content">{escaped_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ───────────── Core workflow UI ─────────────
st.markdown(
    "<div class='core-box'><h3 style='text-align:center;margin-top:0;"
    "margin-bottom:1.5rem;color:#c084fc;'>Core workflow (MVP)</h3>",
    unsafe_allow_html=True,
)

# Provider selection
provider = st.radio(
    "Select AI Provider",
    ["Gemini (Cloud) [best]", "Ollama (Local) [cracked]"],
    horizontal=True,
    help="Choose between cloud-based Gemini or local Ollama"
)

is_local = "Ollama" in provider

# Check Ollama status if local is selected
if is_local:
    ollama_status = check_ollama_status()
    if not ollama_status:
        st.error("⚠️ Ollama is not running! Please start Ollama first with: `ollama serve`")
        st.info("Then make sure you have pulled deepseek-r1:1.5b with: `ollama pull deepseek-r1:1.5b`")

# WhatsApp module (locked)
st.markdown(
    """
    <div style='display:flex;justify-content:flex-end;margin-bottom:1.2rem;'>
        <button disabled style='background:linear-gradient(90deg,#25d366 0%,#e0ffe5 100%);color:#222;font-weight:600;border:none;border-radius:1.2rem;padding:0.7rem 1.7rem;box-shadow:0 2px 8px #25d36633;cursor:not-allowed;opacity:0.7;font-size:1.1rem;'>
            WhatsApp Messaging (Coming Soon)
        </button>
    </div>
    """,
    unsafe_allow_html=True
)

# Add Gemini deprecation notice above cloud model selector
st.markdown(
    """
    <div style='margin:0 auto 1.2rem auto;max-width:700px;'>
        <span style='background:linear-gradient(90deg,#e0ffe5 0%,#b2f7cc 100%);color:#1a7f37;font-weight:600;padding:0.7rem 1.5rem;border-radius:0.8rem;box-shadow:0 2px 8px #25d36622;font-size:1.08rem;display:inline-block;'>
            Gemini 1.0 Pro Vision has been deprecated on July 12, 2024. Consider switching to a different model, for example gemini-1.5-flash.
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# Add model selection quality notice above Gemini model selection
st.markdown(
    """
    <div style='margin:0 auto 0.7rem auto;max-width:700px;'>
        <span style='background:linear-gradient(90deg,#f8fafc 0%,#e0ffe5 100%);color:#1a7f37;font-weight:500;padding:0.5rem 1.2rem;border-radius:0.7rem;box-shadow:0 1px 4px #25d36611;font-size:1.01rem;display:inline-block;'>
            Model selection may impact email quality.
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# Model selection based on provider
st.markdown("<div class='model-selector'>", unsafe_allow_html=True)

gemini_down_label = '<span style="color:#bdbdbd;font-size:0.95em;padding-left:8px;background:rgba(255,0,0,0.08);border-radius:8px;padding:2px 8px;vertical-align:middle;">down</span>'


def gemini_format_func(x):
    if x == "gemini-1.0":
        return f"{x} {gemini_down_label}"
    return x


if is_local and ollama_status:
    # Get Ollama models
    ollama_models = get_ollama_models()
    if ollama_models:
        selected_model = st.selectbox(
            "🤖 Select Local Model",
            options=ollama_models,
            index=ollama_models.index("deepseek-r1:1.5b") if "deepseek-r1:1.5b" in ollama_models else 0,
            help="Choose your local Ollama model"
        )
        st.caption("🟢 Running locally - No API costs!")
    else:
        st.error("No Ollama models found. Pull a model with: `ollama pull deepseek-r1:1.5b`")
        selected_model = None
else:
    # Get Gemini models
    try:
        gemini_models, model_info = get_gemini_models()
        # If gemini-1.0 is present, add 'down' badge
        selected_model = st.selectbox(
            "Select Cloud Model",
            options=gemini_models,
            index=0 if gemini_models else None,
            help="Choose the Gemini model for email generation",
            format_func=gemini_format_func
        )
        st.caption("☁Cloud-based - API costs apply")
        if selected_model == "gemini-1.0":
            st.markdown(
                """
                <div style='margin-top:0.5rem;margin-bottom:0.7rem;'>
                    <span style='background:linear-gradient(90deg,#e0ffe5 0%,#b2f7cc 100%);color:#1a7f37;font-weight:600;padding:0.4rem 1.2rem;border-radius:0.8rem;box-shadow:0 2px 8px #25d36622;font-size:1.01rem;display:inline-block;'>
                        Gemini 1.0 Pro Vision has been deprecated on July 12, 2024. Consider switching to a different model, for example gemini-1.5-flash.
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
    except Exception as e:
        st.error(f"Error fetching Gemini models: {str(e)}")
        selected_model = None

st.markdown("</div>", unsafe_allow_html=True)

# Pre-made prompts
pre_prompts = [
    "",
    "Write a friendly follow-up email after connecting with someone at a conference",
    "Write an email to a friend asking for their opinion on a recent movie or book",
    "Write an email to a potential client introducing your services",
    "Write an email for a follow-up after a game-changing interview"
]
pre_prompt = st.selectbox("Choose a pre-made prompt (optional)", pre_prompts, index=0,
                          help="Select a pre-made prompt to auto-fill the email context.")

# Email generation form
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        topic1 = st.text_input("Topic line 1", placeholder="e.g. project update", key="topic1")
    with c2:
        topic2 = st.text_input("Topic line 2", placeholder="e.g. next steps", key="topic2")

    c3, c4 = st.columns(2)
    with c3:
        sender = st.text_input("Sender", placeholder="your name", key="sender")
    with c4:
        recipient = st.text_input("Recipient", placeholder="recipient's name", key="recipient")

    # Additional details/context input
    context = st.text_area("Additional details or context (optional)",
                           placeholder="Add any extra info, background, or specifics for the email here…",
                           key="context_box")

    # If pre_prompt is selected, append to context
    if pre_prompt and pre_prompt.strip():
        context = (context + "\n" + pre_prompt).strip() if context else pre_prompt

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    tone_options = ["Formal", "Motivated", "Concerned", "Disappointed", "Other (type your own)"]
    selected_tone = st.selectbox("Tone", tone_options, index=0, key="tone_select")
    if selected_tone == "Other (type your own)":
        tone = st.text_input("Type your custom tone", key="custom_tone")
    else:
        tone = selected_tone
    # --- Word count slider ---
    word_count = st.slider(
        "Approximate word count",
        min_value=50,
        max_value=400,
        value=180,
        step=10,
        help="Control the length of the generated email",
        format="%d words",
        key="word_count_slider"
    )
    # --- Human/AI scale ---
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    ai_human_scale = st.slider(
        "Human vs AI Style",
        min_value=0,
        max_value=100,
        value=60,
        step=1,
        help="0 = Most AI-like (formal), 100 = Most human-like (informal)",
        format="%d",
        key="ai_human_slider"
    )
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    if "generated_email" not in st.session_state:
        st.session_state.generated_email = ""

    if st.button("Generate Email", use_container_width=True, type="primary"):
        # If a pre-made prompt is selected, topic1/topic2 are not required
        if not (pre_prompt and pre_prompt.strip()) and not all([topic1, topic2]):
            st.warning("Please fill in both topic lines or select a pre-made prompt.")
        elif not all([sender, recipient, tone, selected_model]):
            st.warning("Please fill in all fields and select a model.")
        elif is_local and not ollama_status:
            st.error("Cannot generate: Ollama is not running!")
        else:
            with st.spinner(f"Generating email with {selected_model}…"):
                if is_local:
                    email_text = generate_email_ollama(
                        topic1, topic2, sender, recipient, tone, selected_model, word_count, context, ai_human_scale,
                        return_thought=False
                    )
                    # Store the thought for later if available
                    st.session_state.ollama_thought = generate_email_ollama(
                        topic1, topic2, sender, recipient, tone, selected_model, word_count, context, ai_human_scale,
                        return_thought=True
                    )
                else:
                    email_text = generate_email_gemini(
                        topic1, topic2, sender, recipient, tone, selected_model, word_count, context, ai_human_scale
                    )
                st.session_state.generated_email = email_text

            # Display with typewriter effect
            if not email_text.startswith("Error"):
                email_placeholder = st.empty()
                typewriter_effect(email_text, email_placeholder)
            else:
                st.error(email_text)

    # Copy, clear, regenerate, share options
    if st.session_state.generated_email and not st.session_state.generated_email.startswith("Error"):
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Copy", use_container_width=True, key="copy_btn"):
                st.session_state.copied = True
        with col2:
            if st.button("🧹 Clear", use_container_width=True, key="clear_btn"):
                st.session_state.generated_email = ""
                st.session_state.ollama_thought = ""
                st.session_state.copied = False
        # Always show the generated email in a code box below the buttons
        st.code(st.session_state.generated_email, language=None)
        if st.session_state.get('copied'):
            st.success("Copied to clipboard!")

    # Ollama 'thought' button (only in local mode)
    if is_local and ollama_status and st.session_state.get('ollama_thought'):
        if st.button("💡 Show AI Thought", key="show_thought_btn"):
            st.info(f"**AI Thought:**\n\n{st.session_state['ollama_thought']}")

st.markdown("</div>", unsafe_allow_html=True)

# ───────────── Provider Info ─────────────
with st.expander("About AI Providers"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Ollama Local")
        st.markdown("""
        **Advantages:**
        - Completely free
        - No API limits
        - Full privacy
        - Works Offline

        **Requirements:**
        - Install Ollama
        - Pull models locally
        - More RAM/CPU usage
        """)

    with col2:
        st.markdown("### Gemini Cloud")
        st.markdown("""
        **Advantages:**
        - Higher quality
        - Faster generation
        - Multiple models
        - No local resources

        **Costs:**
        - Free tier available
        - ~$0.001 per email after[for reference only]
        """)

# ───────────── Extras (unchanged) ─────────────
st.header("Monday is not like any other 'day'. Here's what's next...")
power_feats = [
    "Tone slider (0-100) for granular voice control.",
    "Multi-language generation & auto-translation.",
    "Brand-voice training -- paste 3--5 sample emails, we learn your style.",
    "Generate three variants + A/B picker.",
    "Attach PDF / DOCX / URLs** as background context.",
    "Advanced controls: temperature & length.",
]
for feat in power_feats:
    st.markdown(f"<div class='feature-card'>{feat}</div>", unsafe_allow_html=True)

st.header("Growth & integrations")
growth_feats = [
    "One-click Gmail / Outlook send (OAuth).",
    "Team workspaces with shared history & roles.",
    "Free-tier + refer-a-friend credits.",
    "Zapier & Webhook connectors.",
    "In-app analytics dashboard (open / reply rates).",
]
for feat in growth_feats:
    st.markdown(f"<div class='feature-card'>{feat}</div>", unsafe_allow_html=True)

st.divider()
st.markdown(
    "<p style='text-align:center;'>Built by <span class='orange'>devak</span> "
    "and crafted with ❤ via Streamlit. Powered by Gemini & Ollama.</p>",
    unsafe_allow_html=True,
)

# Gemini rate limit meter (if possible)
if not is_local:
    st.markdown(
        """
        <div style='margin:2.5rem auto 1.5rem auto;max-width:420px;text-align:center;'>
            <div style='background:linear-gradient(90deg,#e0ffe5 0%,#b2f7cc 100%);border-radius:1.2rem;padding:0.7rem 1.2rem;box-shadow:0 2px 8px #25d36622;display:flex;align-items:center;justify-content:center;gap:1.2rem;'>
                <span style='color:#1a7f37;font-weight:600;font-size:1.1rem;'>Gemini API Rate Limit</span>
                <span style='background:#fff;color:#1a7f37;border-radius:0.7rem;padding:0.3rem 0.8rem;font-weight:700;font-size:1.05rem;'>60/min</span>
                <span style='color:#1a7f37;font-size:0.95rem;'>Try not to exceed this limit</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Feedback section
st.markdown(
    """
    <div style='margin:2.5rem auto 1.5rem auto;max-width:520px;text-align:center;'>
        <a href='https://docs.google.com/forms/d/e/1FAIpQLSfZck5FMb72D7-LKSFveCq_O9LNwpoEu3dswCeuwlz-j_XIFg/viewform?usp=dialog' target='_blank' style='text-decoration:none;'>
            <button style='background:linear-gradient(90deg,#25d366 0%,#e0ffe5 100%);color:#222;font-weight:600;border:none;border-radius:1.2rem;padding:0.9rem 2.2rem;box-shadow:0 2px 8px #25d36633;cursor:pointer;font-size:1.15rem;'>
                Share Feedback ❤️
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)