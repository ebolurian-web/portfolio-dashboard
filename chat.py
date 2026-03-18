import os
import streamlit as st
import google.generativeai as genai
from datetime import date

_SYSTEM_PROMPT = """
You are a friendly portfolio analysis assistant. Your job is to collect exactly 6 pieces
of information from the user through natural conversation:

1. Stock tickers to analyze (e.g. AAPL, MSFT, BTC-USD)
2. Analysis start date
3. Analysis end date (if not given, use today)
4. Initial investment amount in dollars
5. Investment horizon in years (must be 1–10)
6. Target portfolio value in dollars

You can ask for multiple things at once if it feels natural. Be brief and friendly.
Once you have all 6, call the configure_portfolio function immediately — do not ask
for confirmation first.
""".strip()

_configure_portfolio_tool = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="configure_portfolio",
            description="Call this once all 6 portfolio parameters have been collected.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "tickers": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Comma-separated ticker symbols, e.g. AAPL, MSFT, BTC-USD",
                    ),
                    "start_date": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Analysis start date in YYYY-MM-DD format",
                    ),
                    "end_date": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Analysis end date in YYYY-MM-DD format",
                    ),
                    "investment": genai.protos.Schema(
                        type=genai.protos.Type.NUMBER,
                        description="Initial investment amount in dollars",
                    ),
                    "horizon_years": genai.protos.Schema(
                        type=genai.protos.Type.INTEGER,
                        description="Investment horizon in years (1–10)",
                    ),
                    "target_value": genai.protos.Schema(
                        type=genai.protos.Type.NUMBER,
                        description="Target portfolio value in dollars",
                    ),
                },
                required=["tickers", "start_date", "end_date", "investment",
                          "horizon_years", "target_value"],
            ),
        )
    ]
)


def _chat_init():
    """Idempotent — safe to call on every render."""
    api_key = os.environ.get("GOOGLE_API_KEY", "")

    if "chat_msgs" not in st.session_state:
        st.session_state.chat_msgs = [
            {"role": "assistant",
             "content": (
                 "Hi! I'll set up your portfolio analysis through a quick chat.\n\n"
                 "Which stocks would you like to analyze? "
                 "Enter tickers separated by commas — e.g. **AAPL, MSFT, GOOGL**. "
                 "Crypto works too (BTC-USD)."
             )}
        ]
        st.session_state.chat_done = False
        st.session_state.chat_vals = {}

        if not api_key:
            st.session_state.chat_msgs.append({
                "role": "assistant",
                "content": (
                    "⚠️ **GOOGLE_API_KEY not set.** "
                    "Get a free key at [aistudio.google.com](https://aistudio.google.com) "
                    "and run: `export GOOGLE_API_KEY=your_key_here`"
                ),
            })

    if "gemini_chat" not in st.session_state and api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=_SYSTEM_PROMPT,
            tools=[_configure_portfolio_tool],
        )
        st.session_state.gemini_chat = model.start_chat()


def _chat_respond(user_input):
    st.session_state.chat_msgs.append({"role": "user", "content": user_input})

    if "gemini_chat" not in st.session_state:
        st.session_state.chat_msgs.append({
            "role": "assistant",
            "content": "⚠️ AI unavailable — please set GOOGLE_API_KEY and restart.",
        })
        return

    try:
        response = st.session_state.gemini_chat.send_message(user_input)
        part = response.candidates[0].content.parts[0]

        if hasattr(part, "function_call") and part.function_call.name == "configure_portfolio":
            args = part.function_call.args
            st.session_state.chat_vals = {
                "tickers_str": args["tickers"],
                "start_date":  date.fromisoformat(args["start_date"]),
                "end_date":    date.fromisoformat(args["end_date"]),
                "investment":  int(args["investment"]),
                "horizon":     int(args["horizon_years"]),
                "goal":        int(args["target_value"]),
            }
            st.session_state.chat_done = True
            st.session_state.chat_msgs.append({
                "role": "assistant",
                "content": (
                    f"All set! Here's your configuration:\n\n"
                    f"**Tickers:** {args['tickers']}\n\n"
                    f"**Period:** {args['start_date']} → {args['end_date']}\n\n"
                    f"**Investment:** ${int(args['investment']):,}\n\n"
                    f"**Horizon:** {int(args['horizon_years'])} year"
                    f"{'s' if int(args['horizon_years']) != 1 else ''}\n\n"
                    f"**Goal:** ${int(args['target_value']):,}\n\n"
                    "Click **Run Analysis** below to begin."
                ),
            })
        else:
            st.session_state.chat_msgs.append({"role": "assistant", "content": part.text})

    except Exception as e:
        st.session_state.chat_msgs.append({
            "role": "assistant",
            "content": f"Something went wrong — please try again. ({e})",
        })
