import streamlit as st
import random
import datetime
import pandas as pd
import json
from typing import Dict, List, Tuple
import time

# Configure page
st.set_page_config(
    page_title="MoodMuse 🎨",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'nickname' not in st.session_state:
    st.session_state.nickname = ""
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = {}
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Quotes and affirmations database
POSITIVE_QUOTES = [
    "You are poetry in motion, even on your quiet days.",
    "The sky today misses your light.",
    "It's okay to pause — blooming takes time.",
    "Your heart holds galaxies of kindness.",
    "Even the moon has phases, and so do you.",
    "You are art in human form.",
    "Your soul speaks in colors others can't see.",
    "Today, you are exactly where you need to be.",
    "Your existence is a beautiful accident of stardust.",
    "You carry magic in your ordinary moments.",
    "Your vulnerability is your superpower.",
    "The world is softer because you're in it.",
    "You are the author of your own love story.",
    "Your dreams deserve to take up space.",
    "You are becoming, always becoming."
]

MOOD_AFFIRMATIONS = {
    "happy": [
        "Your joy is contagious and beautiful! ✨",
        "Happiness looks wonderful on you! 🌈",
        "Your smile could light up the darkest room! ☀️"
    ],
    "sad": [
        "Your tears water the garden of your growth 🌱",
        "It's okay to feel deeply - you're healing 💙",
        "This feeling will pass, like clouds in the sky ☁️"
    ],
    "anxious": [
        "Breathe, dear one. You are safe in this moment 🕊️",
        "Your worries don't define your worth 🌸",
        "Anxiety is just excitement without breath 🫧"
    ],
    "tired": [
        "Rest is not a reward for work completed 🌙",
        "Your body is asking for kindness - listen 🤗",
        "Tiredness is your soul asking for tenderness 💤"
    ],
    "inspired": [
        "Your creativity is a gift to the world! 🎨",
        "Follow that spark - it knows the way ⭐",
        "You are a creator, a dreamer, a magic-maker! ✨"
    ],
    "overwhelmed": [
        "One breath, one step, one moment at a time 🌊",
        "You don't have to carry it all at once 🦋",
        "You are stronger than the storm you're weathering 🌈"
    ],
    "grateful": [
        "Gratitude turns what we have into enough 🙏",
        "Your heart is a garden of appreciation 🌺",
        "Thank you for seeing beauty in small things 🌻"
    ],
    "lonely": [
        "You are never alone when you're with yourself 🌙",
        "Solitude is where you meet your soul 🦋",
        "Your company is the most important you keep 💜"
    ]
}

# Mood-based image URLs (using Unsplash for variety)
MOOD_IMAGES = {
    "happy": [
        "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400",
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=400",
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
    ],
    "sad": [
        "https://images.unsplash.com/photo-1515378791036-0648a814c963?w=400",
        "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=400",
        "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=400"
    ],
    "anxious": [
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400",
        "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?w=400"
    ],
    "tired": [
        "https://images.unsplash.com/photo-1485470733090-0aae1788d5af?w=400",
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
        "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=400"
    ],
    "inspired": [
        "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400",
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400"
    ],
    "overwhelmed": [
        "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=400",
        "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=400",
        "https://images.unsplash.com/photo-1515378791036-0648a814c963?w=400"
    ],
    "grateful": [
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=400",
        "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400",
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
    ],
    "lonely": [
        "https://images.unsplash.com/photo-1485470733090-0aae1788d5af?w=400",
        "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=400",
        "https://images.unsplash.com/photo-1515378791036-0648a814c963?w=400"
    ]
}

def apply_dark_mode():
    """Apply dark mode styling"""
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
            color: #f8f8f2;
        }
        .mood-card {
            background: rgba(40, 42, 54, 0.8);
            border: 1px solid #44475a;
            color: #f8f8f2;
        }
        .quote-box {
            background: linear-gradient(135deg, #44475a 0%, #6272a4 100%);
            color: #f8f8f2;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #ffeef8 0%, #f0f4ff 100%);
        }
        .mood-card {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #e1e5eb;
        }
        .quote-box {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
            color: #4a4a4a;
        }
        </style>
        """, unsafe_allow_html=True)

def generate_poem(mood: str, time_slot: str) -> str:
    """Generate a unique poem based on mood and time"""
    poems = {
        "happy": [
            f"Morning light dances in your eyes,\nJoy bubbles up like sunrise skies.\nYour laughter paints the world anew,\nHappiness flows from me to you.\nThis {time_slot} holds your golden glow,\nLet happiness freely flow.",
            f"Sunshine lives within your smile,\nMaking every moment worthwhile.\nYour joy is like a gentle breeze,\nPutting worried hearts at ease.\nIn this {time_slot}, you shine so bright,\nFilling the world with pure delight.",
            f"Your happiness is art in motion,\nLike waves of love in a peaceful ocean.\nIt sparkles, dances, lights the way,\nMaking magic of an ordinary day.\nThis {time_slot} celebrates your joy,\nA gift that nothing can destroy."
        ],
        "sad": [
            f"Gentle tears like morning dew,\nWash the world with clearer view.\nSadness holds its own sweet grace,\nHealing comes at its own pace.\nThis {time_slot} honors how you feel,\nTime will help your heart to heal.",
            f"In the quiet of your sorrow,\nSeeds are planted for tomorrow.\nTears are not a sign of weak,\nBut the language hearts do speak.\nLet this {time_slot} hold you tight,\nDarkness always turns to light.",
            f"Your sadness is a sacred thing,\nLike rain that helps the flowers spring.\nIt's okay to feel this deep,\nSometimes hearts just need to weep.\nThis {time_slot} whispers soft and low,\nYou're loved more than you'll ever know."
        ],
        "anxious": [
            f"Breathe in peace, breathe out the fear,\nRemember, love, that you are here.\nAnxiety may cloud your mind,\nBut leave the worst-case thoughts behind.\nThis {time_slot} brings you gentle calm,\nLet serenity be your healing balm.",
            f"Worried thoughts like butterflies,\nFlutter, dance, then say goodbye.\nYour worth is not measured by your fear,\nYou are precious, you are dear.\nIn this {time_slot}, find your ground,\nPeace in breath is always found.",
            f"The storm within will surely pass,\nLike shadows moving through the grass.\nYour anxious heart deserves such care,\nBreathe deep the sweet and gentle air.\nThis {time_slot} holds you safe and sound,\nIn love's embrace, you're always found."
        ],
        "tired": [
            f"Rest now, weary soul of mine,\nLet your tired spirit shine.\nEven moons must sometimes wane,\nBefore they're bright and full again.\nThis {time_slot} grants you gentle ease,\nSleep brings the sweetest peace.",
            f"Your tired heart has worked so hard,\nLike a faithful, beating guard.\nIt's time to let your shoulders drop,\nLet all the endless spinning stop.\nIn this {time_slot}, find your rest,\nYou've truly given your very best.",
            f"Exhaustion is your body's way,\nOf asking for a softer day.\nHonor what your soul requests,\nIn tiredness, healing nests.\nThis {time_slot} whispers, 'It's okay,\nTomorrow brings another day.'"
        ],
        "inspired": [
            f"Lightning strikes within your soul,\nCreativity takes full control.\nIdeas dance like fireflies bright,\nIlluminating inner sight.\nThis {time_slot} holds your magic spark,\nIgniting light within the dark.",
            f"Your inspiration flows like streams,\nCarrying hopes and vivid dreams.\nCreativity runs through your veins,\nLike sunshine following the rains.\nIn this {time_slot}, let your spirit soar,\nThere's always room to dream some more.",
            f"The muse has kissed your waking mind,\nInspiration, pure and kind.\nYour creative heart beats strong,\nLike a beautiful, flowing song.\nThis {time_slot} celebrates your art,\nThe masterpiece within your heart."
        ],
        "overwhelmed": [
            f"The weight upon your shoulders now,\nWill lighten up somehow.\nYou don't need to carry it all,\nIt's okay to sometimes fall.\nThis {time_slot} offers gentle grace,\nA slower, kinder pace.",
            f"When life feels like a raging sea,\nRemember you can simply be.\nNot everything needs solving now,\nTake a breath and make a vow.\nIn this {time_slot}, find your center,\nLet peace and stillness enter.",
            f"Overwhelm is just a sign,\nThat you need to realign.\nPriorities can shift and change,\nYour feelings are not strange.\nThis {time_slot} whispers soft and low,\nYou're stronger than you know."
        ],
        "grateful": [
            f"Gratitude blooms in your heart,\nLike a beautiful work of art.\nEvery blessing, large and small,\nYou notice and cherish them all.\nThis {time_slot} overflows with grace,\nThanks written on your face.",
            f"Your thankful heart sees gold,\nIn stories yet untold.\nGratitude is your superpower,\nBrightening every single hour.\nIn this {time_slot}, appreciation grows,\nLike the sweetest garden rose.",
            f"With grateful eyes, you see,\nThe magic in what others might miss to be.\nThankfulness transforms your view,\nMaking everything feel new.\nThis {time_slot} celebrates your grace,\nGratitude lights up your face."
        ],
        "lonely": [
            f"In solitude, you're not alone,\nYour heart's your truest home.\nLoneliness can teach us how,\nTo love ourselves right now.\nThis {time_slot} holds you tenderly,\nYou're loved more than you can see.",
            f"The quiet moments teach us most,\nAbout the souls we host.\nLoneliness is not a flaw,\nBut wisdom wrapped in awe.\nIn this {time_slot}, embrace your space,\nYou're held in love's embrace.",
            f"Sometimes we need to be alone,\nTo make our hearts our home.\nLoneliness can be a friend,\nOn whom we can depend.\nThis {time_slot} reminds you true,\nThe most important love is you."
        ]
    }
    
    # Get current time for additional uniqueness
    current_time = datetime.datetime.now()
    seed = hash(f"{mood}_{time_slot}_{current_time.microsecond}")
    random.seed(seed)
    
    return random.choice(poems.get(mood, poems["happy"]))

def get_mood_image(mood: str) -> str:
    """Get a random image for the mood"""
    current_time = datetime.datetime.now()
    seed = hash(f"{mood}_{current_time.microsecond}")
    random.seed(seed)
    return random.choice(MOOD_IMAGES.get(mood, MOOD_IMAGES["happy"]))

def get_mood_affirmation(mood: str) -> str:
    """Get a random affirmation for the mood"""
    current_time = datetime.datetime.now()
    seed = hash(f"{mood}_affirmation_{current_time.microsecond}")
    random.seed(seed)
    return random.choice(MOOD_AFFIRMATIONS.get(mood, MOOD_AFFIRMATIONS["happy"]))

def save_mood_entry(date: str, time_slot: str, mood: str, note: str = ""):
    """Save mood entry to session state"""
    if date not in st.session_state.mood_data:
        st.session_state.mood_data[date] = {}
    
    st.session_state.mood_data[date][time_slot] = {
        "mood": mood,
        "note": note,
        "timestamp": datetime.datetime.now().isoformat()
    }

def login_screen():
    """Display login screen"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1 style='color: #ff6b9d; font-size: 3rem; margin-bottom: 1rem;'>🌙 MoodMuse 🎨</h1>
        <p style='font-size: 1.2rem; color: #666; margin-bottom: 2rem;'>
            Your personal sanctuary for mood, art & poetry
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### ✨ Welcome, beautiful soul ✨")
        nickname = st.text_input("What shall I call you?", placeholder="Enter your nickname...")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Enter MoodMuse 🦋", type="primary", use_container_width=True):
                if nickname:
                    st.session_state.nickname = nickname
                    st.session_state.logged_in = True
                    st.rerun()
        
        with col_b:
            dark_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
            if dark_toggle != st.session_state.dark_mode:
                st.session_state.dark_mode = dark_toggle
                st.rerun()

def main_app():
    """Main application interface"""
    apply_dark_mode()
    
    # Header with dark mode toggle
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        # Daily greeting with random quote
        current_time = datetime.datetime.now()
        seed = hash(f"daily_quote_{current_time.date()}")
        random.seed(seed)
        daily_quote = random.choice(POSITIVE_QUOTES)
        
        st.markdown(f"""
        <div class="quote-box" style="padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
            <h2 style="margin-bottom: 1rem;">Hey {st.session_state.nickname}! 🌸</h2>
            <p style="font-style: italic; font-size: 1.1rem; margin: 0;">"{daily_quote}"</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🎲 Surprise Me"):
            st.session_state.show_surprise = True
    
    with col3:
        dark_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
        if dark_toggle != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_toggle
            st.rerun()
    
    # Show surprise if requested
    if hasattr(st.session_state, 'show_surprise') and st.session_state.show_surprise:
        show_surprise()
        st.session_state.show_surprise = False
    
    # Main navigation
    tab1, tab2, tab3 = st.tabs(["📝 Today's Mood Journal", "📅 Mood Calendar", "🎨 My Gallery"])
    
    with tab1:
        mood_journal()
    
    with tab2:
        mood_calendar()
    
    with tab3:
        mood_gallery()

def show_surprise():
    """Show surprise content"""
    surprise_types = ["quote", "poem", "scene", "memory_prompt"]
    current_time = datetime.datetime.now()
    seed = hash(f"surprise_{current_time.microsecond}")
    random.seed(seed)
    surprise_type = random.choice(surprise_types)
    
    st.markdown("### 🎁 Your Daily Surprise!")
    
    if surprise_type == "quote":
        quote = random.choice(POSITIVE_QUOTES)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
            <h3>✨ Random Inspiration ✨</h3>
            <p style="font-style: italic; font-size: 1.2rem;">"{quote}"</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif surprise_type == "poem":
        poems = [
            "Today you are a walking poem,\nYour existence, pure art.\nEvery breath a stanza,\nEvery heartbeat, a new start.\nYou are the author of your story,\nWrite it with love and glory.",
            
            "In the garden of your soul,\nBeautiful flowers grow.\nSome days they're shy and hidden,\nOther days they steal the show.\nTend to them with kindness,\nLet your inner beauty flow.",
            
            "You are made of stardust,\nAnd dreams that learned to fly.\nYour spirit holds the universe,\nBeneath the endless sky.\nRemember this truth always,\nYou're magic, you're alive."
        ]
        poem = random.choice(poems)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
            <h3>📜 Spontaneous Poetry 📜</h3>
            <p style="white-space: pre-line; font-size: 1.1rem; line-height: 1.6;">{poem}</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif surprise_type == "scene":
        scenes = [
            "🌧️ Imagine: A cozy window seat with rain tapping gently outside, a warm cup of tea in your hands, and a good book waiting to be read.",
            "🌟 Picture this: You're lying on soft grass under a blanket of stars, feeling the universe holding you in its gentle embrace.",
            "🌅 Envision: The first light of dawn painting the sky in watercolors, and you're there to witness this daily miracle."
        ]
        scene = random.choice(scenes)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #a8e6cf 0%, #dcedc8 100%); 
                    padding: 2rem; border-radius: 15px; margin: 1rem 0;">
            <h3>🎨 Cozy Scene for You 🎨</h3>
            <p style="font-size: 1.1rem; line-height: 1.6;">{scene}</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:  # memory_prompt
        prompts = [
            "What's a time you felt completely safe and loved?",
            "Describe a moment when you surprised yourself with your own strength.",
            "What's a small thing that always makes you smile?",
            "Tell me about a place that feels like home to your soul.",
            "What's a compliment you received that you still treasure?"
        ]
        prompt = random.choice(prompts)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ffd3a5 0%, #fd9853 100%); 
                    padding: 2rem; border-radius: 15px; margin: 1rem 0;">
            <h3>💭 Gentle Reflection 💭</h3>
            <p style="font-size: 1.1rem; line-height: 1.6;">{prompt}</p>
        </div>
        """, unsafe_allow_html=True)

def mood_journal():
    """Mood journal interface"""
    st.markdown("### 🌅 How are you feeling today?")
    
    today = datetime.date.today().isoformat()
    
    # Time slots
    time_slots = ["Morning", "Afternoon", "Night"]
    mood_options = ["happy", "sad", "anxious", "tired", "inspired", "overwhelmed", "grateful", "lonely"]
    
    cols = st.columns(3)
    
    for i, time_slot in enumerate(time_slots):
        with cols[i]:
            st.markdown(f"#### {['🌅', '☀️', '🌙'][i]} {time_slot}")
            
            # Get existing mood if any
            existing_mood = None
            existing_note = ""
            if today in st.session_state.mood_data and time_slot.lower() in st.session_state.mood_data[today]:
                existing_mood = st.session_state.mood_data[today][time_slot.lower()]["mood"]
                existing_note = st.session_state.mood_data[today][time_slot.lower()].get("note", "")
            
            # Mood selection
            mood_index = mood_options.index(existing_mood) if existing_mood in mood_options else 0
            selected_mood = st.selectbox(
                "How do you feel?",
                mood_options,
                index=mood_index,
                key=f"mood_{time_slot.lower()}"
            )
            
            # Optional note
            note = st.text_area(
                "Optional note:",
                value=existing_note,
                height=80,
                key=f"note_{time_slot.lower()}"
            )
            
            # Save button
            if st.button(f"Save {time_slot}", key=f"save_{time_slot.lower()}", type="primary", use_container_width=True):
                save_mood_entry(today, time_slot.lower(), selected_mood, note)
                st.success(f"{time_slot} mood saved! ✨")
                
                # Show generated content
                st.markdown("---")
                st.markdown("#### 🎨 Generated for you:")
                
                # Image
                image_url = get_mood_image(selected_mood)
                st.image(image_url, width=200)
                
                # Poem
                poem = generate_poem(selected_mood, time_slot.lower())
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h5>📜 Your Poem</h5>
                    <p style="white-space: pre-line; font-style: italic;">{poem}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Affirmation
                affirmation = get_mood_affirmation(selected_mood)
                st.markdown(f"""
                <div style="background: rgba(255,192,203,0.3); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h5>💕 Affirmation</h5>
                    <p>{affirmation}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Gentle suggestions for negative moods
                if selected_mood in ["sad", "overwhelmed", "anxious", "lonely"]:
                    suggestions = {
                        "sad": "💙 Try: Make some tea, listen to gentle music, or write in a journal",
                        "overwhelmed": "🌊 Try: Take 5 deep breaths, make a simple to-do list, or step outside",
                        "anxious": "🕊️ Try: Practice the 5-4-3-2-1 grounding technique or call a friend",
                        "lonely": "🤗 Try: Reach out to someone you care about, or treat yourself with kindness"
                    }
                    st.info(suggestions[selected_mood])

def mood_calendar():
    """Mood calendar view"""
    st.markdown("### 📅 Your Mood Journey")
    
    if not st.session_state.mood_data:
        st.info("Start journaling to see your mood patterns! 🌱")
        return
    
    # Create a simple calendar view
    for date_str, day_data in sorted(st.session_state.mood_data.items(), reverse=True):
        date_obj = datetime.datetime.fromisoformat(date_str).date()
        
        with st.expander(f"📅 {date_obj.strftime('%B %d, %Y')} ({date_obj.strftime('%A')})"):
            cols = st.columns(3)
            
            for i, time_slot in enumerate(["morning", "afternoon", "night"]):
                with cols[i]:
                    if time_slot in day_data:
                        mood_data = day_data[time_slot]
                        mood = mood_data["mood"]
                        note = mood_data.get("note", "")
                        
                        emoji_map = {
                            "happy": "😊", "sad": "😢", "anxious": "😰", 
                            "tired": "😴", "inspired": "✨", "overwhelmed": "😵‍💫",
                            "grateful": "🙏", "lonely": "🥺"
                        }
                        
                        st.markdown(f"""
                        <div class="mood-card" style="padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                            <h5>{['🌅 Morning', '☀️ Afternoon', '🌙 Night'][i]}</h5>
                            <p>{emoji_map.get(mood, '💭')} {mood.title()}</p>
                            {f'<p style="font-size: 0.9rem; font-style: italic;">"{note}"</p>' if note else ''}
                        </div>
                        """, unsafe_allow_html=True)

def mood_gallery():
    """Mood gallery with saved content"""
    st.markdown("### 🎨 Your Personal Gallery")
    
    if not st.session_state.mood_data:
        st.info("Your beautiful creations will appear here as you journal! 🌸")
        return
    
    # Export option
    if st.button("📥 Export My Journey", type="secondary"):
        export_data = {
            "nickname": st.session_state.nickname,
            "mood_data": st.session_state.mood_data,
            "export_date": datetime.datetime.now().isoformat()
        }
        st.download_button(
            label="Download as JSON",
            data=json.dumps(export_data, indent=2),
            file_name=f"moodmuse_journey_{st.session_state.nickname}_{datetime.date.today()}.json",
            mime="application/json"
        )
    
    # Gallery display
    gallery_items = []
    for date_str, day_data in st.session_state.mood_data.items():
        for time_slot, mood_info in day_data.items():
            gallery_items.append({
                "date": date_str,
                "time_slot": time_slot,
                "mood": mood_info["mood"],
                "note": mood_info.get("note", ""),
                "timestamp": mood_info.get("timestamp", "")
            })
    
    # Sort by date (newest first)
    gallery_items.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Display gallery items in a grid
    cols_per_row = 2
    for i in range(0, len(gallery_items), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            if i + j < len(gallery_items):
                item = gallery_items[i + j]
                
                with cols[j]:
                    # Create a beautiful card for each entry
                    date_obj = datetime.datetime.fromisoformat(item["date"]).date()
                    
                    # Generate content for this mood entry
                    image_url = get_mood_image(item["mood"])
                    poem = generate_poem(item["mood"], item["time_slot"])
                    affirmation = get_mood_affirmation(item["mood"])
                    
                    time_emoji = {"morning": "🌅", "afternoon": "☀️", "night": "🌙"}
                    mood_emoji = {
                        "happy": "😊", "sad": "😢", "anxious": "😰", 
                        "tired": "😴", "inspired": "✨", "overwhelmed": "😵‍💫",
                        "grateful": "🙏", "lonely": "🥺"
                    }
                    
                    st.markdown(f"""
                    <div class="mood-card" style="padding: 1.5rem; border-radius: 15px; margin: 1rem 0; text-align: center;">
                        <h4>{date_obj.strftime('%b %d')} - {time_emoji.get(item['time_slot'], '💭')} {item['time_slot'].title()}</h4>
                        <p style="font-size: 1.2rem; margin: 1rem 0;">{mood_emoji.get(item['mood'], '💭')} {item['mood'].title()}</p>
                        {f'<p style="font-style: italic; color: #666; margin-bottom: 1rem;">"{item["note"]}"</p>' if item['note'] else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Image
                    st.image(image_url, width=250)
                    
                    # Expandable poem and affirmation
                    with st.expander("View Generated Content"):
                        st.markdown("**📜 Your Poem:**")
                        st.markdown(f"*{poem}*")
                        st.markdown("**💕 Affirmation:**")
                        st.markdown(affirmation)

def main():
    """Main function to run the app"""
    if not st.session_state.logged_in:
        login_screen()
    else:
        # Logout button in sidebar
        with st.sidebar:
            st.markdown(f"### Welcome back, {st.session_state.nickname}! 🌸")
            st.markdown("---")
            
            # Some stats
            if st.session_state.mood_data:
                total_entries = sum(len(day_data) for day_data in st.session_state.mood_data.values())
                st.metric("Total Mood Entries", total_entries)
                
                # Most common mood
                all_moods = []
                for day_data in st.session_state.mood_data.values():
                    for mood_info in day_data.values():
                        all_moods.append(mood_info["mood"])
                
                if all_moods:
                    most_common_mood = max(set(all_moods), key=all_moods.count)
                    st.metric("Most Common Mood", most_common_mood.title())
            
            st.markdown("---")
            
            # Wellness tips
            st.markdown("### 🌱 Daily Wellness Tips")
            wellness_tips = [
                "Take 3 deep breaths right now 🫧",
                "Drink a glass of water 💧",
                "Step outside for 2 minutes 🌿",
                "Text someone you love 💕",
                "Write down one thing you're grateful for 🙏",
                "Stretch your arms above your head 🙆‍♀️",
                "Listen to your favorite song 🎵",
                "Look at something beautiful around you 👀"
            ]
            current_time = datetime.datetime.now()
            seed = hash(f"wellness_tip_{current_time.date()}")
            random.seed(seed)
            daily_tip = random.choice(wellness_tips)
            st.info(daily_tip)
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.nickname = ""
                st.rerun()
        
        main_app()

# Custom CSS for better styling
st.markdown("""
<style>
/* Custom fonts and animations */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

.stApp {
    font-family: 'Inter', sans-serif;
}

/* Smooth transitions */
.mood-card {
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.mood-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

/* Button styling */
.stButton > button {
    border-radius: 25px;
    border: none;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #ff6b9d 0%, #c471ed 100%);
}

/* Responsive design */
@media (max-width: 768px) {
    .mood-card {
        margin: 0.5rem 0;
        padding: 1rem;
    }
}

/* Animation for new entries */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.new-entry {
    animation: fadeInUp 0.5s ease-out;
}

/* Loading spinner */
.stSpinner {
    color: #ff9a9e !important;
}

/* Success messages */
.stSuccess {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    border: none;
    color: #2d3748;
}

/* Info messages */
.stInfo {
    background: linear-gradient(135deg, #ffeef8 0%, #f0f4ff 100%);
    border: none;
    color: #4a5568;
}
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()