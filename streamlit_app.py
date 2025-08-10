import streamlit as st
import json
import random
import time
from typing import Dict, List

# Configure page
st.set_page_config(
    page_title="Truth or Dare 💀",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load prompts data
@st.cache_data
def load_prompts() -> Dict:
    """Load truth and dare prompts from JSON file"""
    import os
    BASE_DIR = os.path.dirname(__file__)  # directory where app.py is located
    file_path = os.path.join(BASE_DIR, "data", "prompts.json")
    with open(file_path, "r") as f:
        return json.load(f)

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 'mild'
    if 'last_prompt' not in st.session_state:
        st.session_state.last_prompt = ""
    if 'prompt_type' not in st.session_state:
        st.session_state.prompt_type = ""
    if 'show_prompt' not in st.session_state:
        st.session_state.show_prompt = False

def shuffle_animation():
    """Create a shuffle animation effect"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    shuffle_messages = [
        "🎲 Rolling the dice...",
        "🔮 Reading your vibe...",
        "✨ Manifesting chaos...",
        "🎯 Picking the perfect prompt...",
        "💫 Almost there..."
    ]
    
    for i in range(100):
        progress_bar.progress(i + 1)
        if i % 20 == 0 and i // 20 < len(shuffle_messages):
            status_text.text(shuffle_messages[i // 20])
        time.sleep(0.02)
    
    progress_bar.empty()
    status_text.empty()

def get_random_prompt(prompts_data: Dict, prompt_type: str, level: str) -> str:
    """Get a random prompt based on type and level"""
    prompts_list = prompts_data[prompt_type][level]
    return random.choice(prompts_list)

def main():
    """Main application function"""
    initialize_session_state()
    prompts_data = load_prompts()
    
    # Header with Gen-Z vibes
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 style='font-size: 3rem; margin-bottom: 0;'>💀 Truth or Dare 💀</h1>
        <p style='font-size: 1.2rem; opacity: 0.8; margin-top: 0;'>for the chronically online generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Level selection
    st.markdown("### Choose Your Chaos Level 🎯")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("😇 Mild", use_container_width=True, 
                    type="primary" if st.session_state.current_level == 'mild' else "secondary"):
            st.session_state.current_level = 'mild'
            st.session_state.show_prompt = False
            st.rerun()
    
    with col2:
        if st.button("😈 Spicy", use_container_width=True,
                    type="primary" if st.session_state.current_level == 'spicy' else "secondary"):
            st.session_state.current_level = 'spicy'
            st.session_state.show_prompt = False
            st.rerun()
    
    with col3:
        if st.button("🤪 Chaotic", use_container_width=True,
                    type="primary" if st.session_state.current_level == 'chaotic' else "secondary"):
            st.session_state.current_level = 'chaotic'
            st.session_state.show_prompt = False
            st.rerun()
    
    # Display current level
    level_emojis = {'mild': '😇', 'spicy': '😈', 'chaotic': '🤪'}
    level_descriptions = {
        'mild': 'Keep it wholesome (mostly)',
        'spicy': 'Things are heating up 🔥',
        'chaotic': 'Prepare for unhinged energy'
    }
    
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); 
         border-radius: 10px; margin: 1rem 0;'>
        <h3 style='margin: 0; color: white;'>
            {level_emojis[st.session_state.current_level]} {st.session_state.current_level.upper()} MODE
        </h3>
        <p style='margin: 0; color: white; opacity: 0.9;'>{level_descriptions[st.session_state.current_level]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Truth or Dare buttons
    st.markdown("### Pick Your Poison 💊")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📢 TRUTH", use_container_width=True, key="truth_btn"):
            shuffle_animation()
            st.session_state.last_prompt = get_random_prompt(prompts_data, 'truth', st.session_state.current_level)
            st.session_state.prompt_type = 'truth'
            st.session_state.show_prompt = True
            st.rerun()
    
    with col2:
        if st.button("🎭 DARE", use_container_width=True, key="dare_btn"):
            shuffle_animation()
            st.session_state.last_prompt = get_random_prompt(prompts_data, 'dare', st.session_state.current_level)
            st.session_state.prompt_type = 'dare'
            st.session_state.show_prompt = True
            st.rerun()
    
    # Display prompt
    if st.session_state.show_prompt and st.session_state.last_prompt:
        prompt_colors = {
            'truth': 'linear-gradient(45deg, #667eea, #764ba2)',
            'dare': 'linear-gradient(45deg, #f093fb, #f5576c)'
        }
        
        prompt_icons = {
            'truth': '📢',
            'dare': '🎭'
        }
        
        st.markdown(f"""
        <div style='background: {prompt_colors[st.session_state.prompt_type]}; 
             padding: 2rem; border-radius: 15px; margin: 2rem 0; text-align: center;
             box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
            <h2 style='color: white; margin-bottom: 1rem;'>
                {prompt_icons[st.session_state.prompt_type]} {st.session_state.prompt_type.upper()}
            </h2>
            <h3 style='color: white; line-height: 1.6; font-weight: 400;'>
                {st.session_state.last_prompt}
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons after showing prompt
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Get Another One", use_container_width=True):
                shuffle_animation()
                st.session_state.last_prompt = get_random_prompt(
                    prompts_data, st.session_state.prompt_type, st.session_state.current_level
                )
                st.rerun()
    
    # Instructions
    st.markdown("---")
    
    with st.expander("📖 How to Play"):
        st.markdown("""
        **Welcome to the most unhinged Truth or Dare experience! 🎉**
        
        1. **Choose your chaos level** - Start mild or go straight to chaotic (we don't judge)
        2. **Pick Truth or Dare** - Both will test your limits differently
        3. **Complete the challenge** - No skipping allowed bestie! 
        4. **Pass the phone** - Take turns with your friends
        
        **Pro Tips:**
        - Mild = Safe for around parents 😇
        - Spicy = Things get interesting 😈  
        - Chaotic = Absolutely unhinged 🤪
        
        **Rules:**
        - What happens in Truth or Dare, stays in Truth or Dare 🤐
        - No screenshots without permission! 📸❌
        - Have fun and stay safe! ✨
        """)
    
    with st.expander("ℹ️ About This App"):
        st.markdown("""
        Created for the chronically online generation 💻
        
        - **600+ prompts** curated for Gen-Z humor
        - **Mobile-first design** for those group hangouts
        - **Three difficulty levels** from wholesome to chaotic
        - **Constantly updated** with fresh content
        
        Made with 💜 for creating unforgettable memories
        """)

if __name__ == "__main__":
    main()
