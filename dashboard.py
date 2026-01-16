import streamlit as st
import pandas as pd
from scout import Scout
from brain import Brain
from copier import Copier
import config

# Page Config
st.set_page_config(page_title="AI Wallet Copy Trader", page_icon="🤖", layout="wide")

# Initialize Session State
if "copier" not in st.session_state:
    st.session_state.copier = Copier()
if "scout" not in st.session_state:
    st.session_state.scout = Scout()
if "brain" not in st.session_state:
    st.session_state.brain = Brain()

st.title("🤖 AI Wallet Copy Trader")

# Sidebar Status
with st.sidebar:
    st.header("System Status")

    # API Key Check
    if config.BITQUERY_API_KEY and "YOUR_KEY" not in config.BITQUERY_API_KEY:
        st.success("✅ BitQuery Connected")
    else:
        st.error("❌ BitQuery Key Missing")

    st.markdown("---")

    # Copier Status
    if st.session_state.copier.is_running:
        st.success("🟢 Copier Active")
        if st.button("Stop Copier"):
            st.session_state.copier.stop_listening()
            st.rerun()
    else:
        st.warning("🔴 Copier Idle")
        if st.button("Start Copier"):
            st.session_state.copier.start_listening()
            st.rerun()

# Tabs
tab1, tab2, tab3 = st.tabs(
    ["🔭 Scout (Discovery)", "🧠 Brain (Analysis)", "⚡ Copier (Live)"]
)

# --- TAB 1: SCOUT ---
with tab1:
    st.header("Market Discovery")
    st.write("Trending tokens found via GeckoTerminal.")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Scan Market Now"):
            with st.spinner("Scanning GeckoTerminal..."):
                tokens = st.session_state.scout.get_trending_tokens(limit=10)
                st.session_state.trending_tokens = tokens
                st.success(f"Found {len(tokens)} tokens.")

    if hasattr(st.session_state, "trending_tokens"):
        df = pd.DataFrame(st.session_state.trending_tokens)
        if not df.empty:
            # Format columns
            display_df = df[
                ["symbol", "address", "liquidity", "volume24h", "pool_address"]
            ]
            st.dataframe(
                display_df,
                column_config={
                    "address": "Token Address",
                    "pool_address": "Pool Address",
                    "liquidity": st.column_config.NumberColumn(
                        "Liquidity", format="$%d"
                    ),
                    "volume24h": st.column_config.NumberColumn("Vol 24h", format="$%d"),
                },
                use_container_width=True,
            )
        else:
            st.info("No tokens found matching criteria.")

# --- TAB 2: BRAIN ---
with tab2:
    st.header("Wallet Analysis")
    st.write("Analyze early buyers of a specific token.")

    token_input = st.text_input("Enter Token Address to Analyze:", placeholder="0x...")

    if st.button("Find Smart Money"):
        if token_input:
            with st.spinner("Querying BitQuery & Scoring Wallets..."):
                # 1. Find Early Buyers
                buyers = st.session_state.brain.find_early_buyers(token_input, limit=50)

                if buyers:
                    st.info(f"Found {len(buyers)} early buyers. Scoring them now...")

                    # 2. Score Wallets
                    scored_wallets = st.session_state.brain.score_wallets(buyers)

                    # Store in session for Copier
                    st.session_state.last_analysis = scored_wallets

                    # Display
                    st.subheader("🏆 Top Performing Wallets")

                    score_df = pd.DataFrame(scored_wallets)
                    st.dataframe(
                        score_df,
                        column_config={
                            "score": st.column_config.ProgressColumn(
                                "AI Score",
                                help="Win Rate Confidence",
                                format="%d",
                                min_value=0,
                                max_value=100,
                            ),
                        },
                        use_container_width=True,
                    )
                else:
                    st.warning("No buyers found or API error.")
        else:
            st.error("Please enter a token address.")

# --- TAB 3: COPIER ---
with tab3:
    st.header("Execution Control")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Active Watchlist")
        if st.session_state.copier.active_watchlist:
            st.table(st.session_state.copier.active_watchlist)
        else:
            st.info("Watchlist is empty. Analyze tokens in 'Brain' tab to populate.")

        if hasattr(st.session_state, "last_analysis"):
            if st.button("Add Top 5 Analysed Wallets to Watchlist"):
                top_5 = [w["address"] for w in st.session_state.last_analysis[:5]]
                st.session_state.copier.update_watchlist(top_5)
                st.success("Watchlist updated!")
                st.rerun()

    with col2:
        st.subheader("Live Logs")
        st.code("System initialized.\nWaiting for signals...", language="bash")
