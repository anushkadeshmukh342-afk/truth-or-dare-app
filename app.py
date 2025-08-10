
import streamlit as st
import json
import random
import time
from typing import Dict, List

# Configure page
st.set_page_config(
    page_title="Truth or Dare ⚡",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load prompts data
@st.cache_data
def load_prompts() -> Dict:
    """Load truth and dare prompts from JSON file"""
    with open('data/prompts.json', 'r', encoding='utf-8') as f:
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

def loading_animation():
    """Create a loading animation effect"""
    st.markdown("""
    <div class="card" style='text-align: center; padding: 2rem;'>
        <h3 class="glow-text">🎯 Loading Challenge... 🎯</h3>
    </div>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    loading_messages = [
        "🎮 Initializing game engine...",
        "⚡ Generating random challenge...",
        "🎯 Calibrating difficulty...",
        "🔥 Preparing your dare...",
        "✅ Challenge ready!"
    ]
    
    for i in range(100):
        progress_bar.progress(i + 1)
        if i % 20 == 0 and i // 20 < len(loading_messages):
            status_text.markdown(f"""
            <p class="loading-text" style='text-align: center; font-style: italic; margin: 1rem 0;'>
                {loading_messages[i // 20]}
            </p>
            """, unsafe_allow_html=True)
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
    
    # Modern dark theme CSS
    st.markdown("""
    <style>
    .main-container {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #1a1a2e 100%);
        min-height: 100vh;
        padding: 2rem 1rem;
        border-radius: 15px;
        margin: -1rem;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .hero-section {
        text-align: center;
        padding: 3rem 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        margin: 2rem 0;
    }
    
    .level-card {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .level-card:hover {
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    }
    
    .glow-text {
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
        font-weight: 400;
        letter-spacing: 1px;
    }
    
    .loading-text {
        color: #cccccc;
        font-size: 0.9rem;
    }
    
    .accent-blue { color: #00d4ff; text-shadow: 0 0 15px rgba(0, 212, 255, 0.5); }
    .accent-orange { color: #ff6b35; text-shadow: 0 0 15px rgba(255, 107, 53, 0.5); }
    .accent-red { color: #ff3333; text-shadow: 0 0 15px rgba(255, 51, 51, 0.5); }
    
    .prompt-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin: 3rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .prompt-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .truth-gradient { background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); }
    .dare-gradient { background: linear-gradient(135deg, #ff6b35 0%, #cc5529 100%); }
    
    .game-button {
        background: linear-gradient(45deg, #333333, #555555);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
        padding: 1rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .game-button:hover {
        background: linear-gradient(45deg, #555555, #777777);
        transform: translateY(-2px);
    }
    </style>
    
    <div class="main-container">
        <div class="hero-section">
            <h1 class="glow-text" style='font-size: 3.5rem; margin: 0;'>⚡ TRUTH OR DARE ⚡</h1>
            <p class="glow-text" style='font-size: 1.4rem; margin: 1rem 0; opacity: 0.9;'>The Ultimate Challenge Game</p>
            <p class="glow-text" style='font-size: 1rem; opacity: 0.7;'>Are you ready to face the truth or take the dare?</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Level selection
    st.markdown("""
    <div class="card">
        <h2 class="glow-text" style='text-align: center; margin-bottom: 2rem;'>🎯 Choose Your Difficulty Level</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    level_data = {
        'mild': {'emoji': '🟢', 'title': 'EASY MODE', 'desc': 'Safe and friendly challenges', 'class': 'accent-blue'},
        'spicy': {'emoji': '🟡', 'title': 'HARD MODE', 'desc': 'Bold and daring questions', 'class': 'accent-orange'},
        'chaotic': {'emoji': '🔴', 'title': 'EXTREME MODE', 'desc': 'No limits, no mercy', 'class': 'accent-red'}
    }
    
    with col1:
        st.markdown(f"""
        <div class="level-card">
            <div style='font-size: 3rem; margin-bottom: 1rem;'>{level_data['mild']['emoji']}</div>
            <h3 class="glow-text {level_data['mild']['class']}" style='margin: 0.5rem 0;'>{level_data['mild']['title']}</h3>
            <p class="glow-text" style='font-size: 0.9rem; opacity: 0.8;'>{level_data['mild']['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("SELECT EASY", use_container_width=True, 
                    type="primary" if st.session_state.current_level == 'mild' else "secondary"):
            st.session_state.current_level = 'mild'
            st.session_state.show_prompt = False
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="level-card">
            <div style='font-size: 3rem; margin-bottom: 1rem;'>{level_data['spicy']['emoji']}</div>
            <h3 class="glow-text {level_data['spicy']['class']}" style='margin: 0.5rem 0;'>{level_data['spicy']['title']}</h3>
            <p class="glow-text" style='font-size: 0.9rem; opacity: 0.8;'>{level_data['spicy']['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("SELECT HARD", use_container_width=True,
                    type="primary" if st.session_state.current_level == 'spicy' else "secondary"):
            st.session_state.current_level = 'spicy'
            st.session_state.show_prompt = False
            st.rerun()
    
    with col3:
        st.markdown(f"""
        <div class="level-card">
            <div style='font-size: 3rem; margin-bottom: 1rem;'>{level_data['chaotic']['emoji']}</div>
            <h3 class="glow-text {level_data['chaotic']['class']}" style='margin: 0.5rem 0;'>{level_data['chaotic']['title']}</h3>
            <p class="glow-text" style='font-size: 0.9rem; opacity: 0.8;'>{level_data['chaotic']['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("SELECT EXTREME", use_container_width=True,
                    type="primary" if st.session_state.current_level == 'chaotic' else "secondary"):
            st.session_state.current_level = 'chaotic'
            st.session_state.show_prompt = False
            st.rerun()
    
    # Display current level
    level_status = {
        'mild': {'color': 'accent-blue', 'status': 'Playing it safe with easy challenges'},
        'spicy': {'color': 'accent-orange', 'status': 'Ready for some bold questions'},
        'chaotic': {'color': 'accent-red', 'status': 'Extreme mode - no holding back!'}
    }
    
    st.markdown(f"""
    <div class="card" style='text-align: center;'>
        <h3 class="glow-text" style='margin-bottom: 1rem;'>
            Current Level: <span class="{level_status[st.session_state.current_level]['color']}">{level_data[st.session_state.current_level]['title']}</span>
        </h3>
        <p class="glow-text" style='font-style: italic; opacity: 0.8;'>{level_status[st.session_state.current_level]['status']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Truth or Dare selection
    st.markdown("""
    <div class="card">
        <h2 class="glow-text" style='text-align: center; margin-bottom: 2rem;'>⚔️ Make Your Choice ⚔️</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="level-card truth-gradient" style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(0, 153, 204, 0.2));'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🎯</div>
            <h3 class="glow-text" style='margin: 0.5rem 0;'>TRUTH</h3>
            <p class="glow-text" style='font-size: 0.9rem; opacity: 0.8;'>Answer honestly, no matter what</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎯 CHOOSE TRUTH", use_container_width=True, key="truth_btn"):
            loading_animation()
            st.session_state.last_prompt = get_random_prompt(prompts_data, 'truth', st.session_state.current_level)
            st.session_state.prompt_type = 'truth'
            st.session_state.show_prompt = True
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="level-card dare-gradient" style='background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(204, 85, 41, 0.2));'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>⚡</div>
            <h3 class="glow-text" style='margin: 0.5rem 0;'>DARE</h3>
            <p class="glow-text" style='font-size: 0.9rem; opacity: 0.8;'>Accept the challenge if you dare</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚡ CHOOSE DARE", use_container_width=True, key="dare_btn"):
            loading_animation()
            st.session_state.last_prompt = get_random_prompt(prompts_data, 'dare', st.session_state.current_level)
            st.session_state.prompt_type = 'dare'
            st.session_state.show_prompt = True
            st.rerun()
    
    # Display prompt
    if st.session_state.show_prompt and st.session_state.last_prompt:
        prompt_colors = {
            'truth': '#00d4ff',
            'dare': '#ff6b35'
        }
        
        prompt_icons = {
            'truth': '🎯',
            'dare': '⚡'
        }
        
        prompt_titles = {
            'truth': 'TRUTH CHALLENGE',
            'dare': 'DARE CHALLENGE'
        }
        
        st.markdown(f"""
        <div class="prompt-card">
            <div style='position: relative; z-index: 1;'>
                <div style='font-size: 5rem; margin-bottom: 1rem; filter: drop-shadow(0 0 20px {prompt_colors[st.session_state.prompt_type]});'>
                    {prompt_icons[st.session_state.prompt_type]}
                </div>
                <h2 class="glow-text" style='margin-bottom: 2rem; font-size: 1.8rem; color: {prompt_colors[st.session_state.prompt_type]};'>
                    {prompt_titles[st.session_state.prompt_type]}
                </h2>
                <div style='
                    background: rgba(255, 255, 255, 0.1); 
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 15px; 
                    padding: 2rem; 
                    margin: 1rem 0;
                '>
                    <h3 class="glow-text" style='
                        line-height: 1.6; 
                        font-weight: 400; 
                        font-size: 1.3rem;
                        margin: 0;
                    '>
                        "{st.session_state.last_prompt}"
                    </h3>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="card" style='text-align: center; padding: 1.5rem;'>
                <p class="glow-text" style='margin-bottom: 1rem; opacity: 0.8;'>
                    Want another challenge?
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 GET ANOTHER CHALLENGE", use_container_width=True):
                loading_animation()
                st.session_state.last_prompt = get_random_prompt(
                    prompts_data, st.session_state.prompt_type, st.session_state.current_level
                )
                st.rerun()
    
    # Instructions and rules
    st.markdown("""
    <div class="card" style='margin-top: 4rem;'>
        <h2 class="glow-text" style='text-align: center; margin-bottom: 2rem;'>📋 Game Rules & Instructions</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 class="glow-text accent-blue" style='margin-bottom: 1rem;'>🎮 How to Play</h3>
            <div class="glow-text" style='line-height: 1.8; font-size: 0.95rem;'>
                <p><strong>1.</strong> Choose your difficulty level</p>
                <p><strong>2.</strong> Select Truth or Dare</p>
                <p><strong>3.</strong> Complete the challenge</p>
                <p><strong>4.</strong> Pass to the next player</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3 class="glow-text accent-orange" style='margin-bottom: 1rem;'>⚡ Difficulty Levels</h3>
            <div class="glow-text" style='line-height: 1.8; font-size: 0.95rem;'>
                <p><strong>🟢 Easy:</strong> Safe and friendly for everyone</p>
                <p><strong>🟡 Hard:</strong> Bold questions and challenges</p>
                <p><strong>🔴 Extreme:</strong> No limits, adults only</p>
                <p><strong>⚠️ Warning:</strong> Play responsibly!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card" style='text-align: center; margin-top: 2rem;'>
        <h3 class="glow-text" style='margin-bottom: 1rem;'>🏆 About This Game</h3>
        <div class="glow-text" style='line-height: 1.6; font-size: 0.95rem;'>
            <p>The ultimate Truth or Dare experience for the modern generation</p>
            <p>⚡ <strong>600+ Challenges</strong> across all difficulty levels</p>
            <p>📱 <strong>Mobile Optimized</strong> for perfect group gameplay</p>
            <p>🎯 <strong>Three Difficulty Modes</strong> for any crowd</p>
            <p>🔄 <strong>Fresh Content</strong> with every play session</p>
            <br>
            <p style='font-style: italic; opacity: 0.8;'>Built for unforgettable moments and endless fun</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Close the main container
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
