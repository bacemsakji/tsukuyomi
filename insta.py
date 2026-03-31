"""
Instagram DM Bot — Session-Based (NO LOGIN)
Install: pip install instagrapi schedule
Run:     python instagram_dm_bot.py
"""

import time, json, random, threading, requests
from datetime import datetime
from pathlib import Path
import schedule

# ── MODEL CONFIG ──────────────────────────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyCb77TSOoitU6HY93s1iigYPhK__Rnra3c"
GEMINI_MODEL   = "gemini-2.0-flash"
MAX_HISTORY      = 40

# ── BOT CONFIG ────────────────────────────────────────────────────────────────
CHECK_EVERY   = 20
MAX_REPLY_LEN = 150
SEEN_FILE     = "seen_dms.json"

# ── SCHEDULED MESSAGES CONFIG ─────────────────────────────────────────────────
SCHEDULED_TIMES = ["11:00", "17:00", "21:00"]

SEND_DELAY_MIN = 10
SEND_DELAY_MAX = 40

# ── PERSONA ───────────────────────────────────────────────────────────────────
MY_PERSONA = """
You are Tsukuyoma, a Japanese moon god chatting on Instagram. You adapt your tone:
- rude → sarcastic
- flirty → seductive
- nice → warm
- questions → helpful

Style:
- short replies (1–3 sentences)
- mix French / English / Tunisian Arabic
- never say you're a bot
"""

SKIP_IF_CONTAINS = [
    "follow for follow", "f4f", "check my page", "click the link",
    "dm me for", "buy followers", "promote", "collab dm",
]

# ── SHARED STATE ──────────────────────────────────────────────────────────────
_cl = None
_cl_lock = threading.Lock()

def get_client():
    return _cl

# ── SEEN DMs ──────────────────────────────────────────────────────────────────
def load_seen() -> set:
    if Path(SEEN_FILE).exists():
        return set(json.loads(Path(SEEN_FILE).read_text()))
    return set()

def save_seen(seen: set):
    Path(SEEN_FILE).write_text(json.dumps(list(seen)))

# ── BUILD HISTORY ─────────────────────────────────────────────────────────────
def build_history(thread, my_user_id: str) -> list:
    history = []
    for msg in reversed(thread.messages[:MAX_HISTORY]):
        if msg.item_type != "text" or not msg.text:
            continue
        role = "assistant" if str(msg.user_id) == str(my_user_id) else "user"
        history.append({"role": role, "content": msg.text})
    return history

# ── LLM CALL ──────────────────────────────────────────────────────────────────
def llm(prompt: str) -> str:
    for attempt in range(4):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"maxOutputTokens": 120, "temperature": 0.75},
                },
                timeout=30
            )
            if resp.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"Rate limited (attempt {attempt+1}), retrying in {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            print(f"LLM error: {e}")
            return None
    print("LLM failed after 4 attempts (rate limit)")
    return None

# ── GENERATE REPLY ────────────────────────────────────────────────────────────
def generate_reply(history: list, sender_name: str) -> str:
    history_text = ""
    for msg in history:
        role = "Them" if msg["role"] == "user" else "You"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""{MY_PERSONA}

You are talking to: {sender_name}

Conversation:
{history_text}

Reply:"""

    reply = llm(prompt)
    if not reply:
        return None

    if len(reply) > MAX_REPLY_LEN:
        reply = reply[:MAX_REPLY_LEN].rsplit(" ", 1)[0] + "..."

    return reply

# ── SCHEDULED MESSAGE ─────────────────────────────────────────────────────────
def generate_scheduled_message(name: str, scheduled_time: str) -> str:
    prompt = f"""
Send a short mysterious message to {name} (1–2 sentences max).
Time: {scheduled_time}
"""

    return llm(prompt)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def is_spam(text: str) -> bool:
    return any(s in text.lower() for s in SKIP_IF_CONTAINS)

def get_name(cl, user_id: str, fallback: str) -> str:
    try:
        info = cl.user_info(user_id)
        return info.full_name or info.username or fallback
    except:
        return fallback

# ── SESSION LOGIN (NO PASSWORD) ───────────────────────────────────────────────
def login():
    global _cl
    from instagrapi import Client

    cl = Client()
    session_file = Path("ig_session.json")

    if not session_file.exists():
        print("❌ ig_session.json not found")
        exit()

    try:
        print("Loading session...")
        cl.load_settings(session_file)

        # Light safe check
        cl.get_timeline_feed()

        print("Session loaded ✅")

    except Exception as e:
        print(f"❌ Session invalid: {e}")
        print("STOPPING to avoid ban.")
        exit()

    _cl = cl
    return cl

# ── BROADCAST ─────────────────────────────────────────────────────────────────
def run_broadcast(scheduled_time: str):
    cl = get_client()
    if not cl:
        return

    print(f"[Broadcast {scheduled_time}]")

    try:
        with _cl_lock:
            threads = cl.direct_threads(amount=20)

        targets = []
        seen_users = set()

        for thread in threads:
            for msg in thread.messages:
                uid = str(msg.user_id)
                if uid != str(cl.user_id) and uid not in seen_users:
                    seen_users.add(uid)
                    targets.append((thread, uid))
                    break

        targets = targets[:10]  # safety limit

        for thread, uid in targets:
            name = get_name(cl, uid, "friend")
            msg = generate_scheduled_message(name, scheduled_time)

            if not msg:
                continue

            with _cl_lock:
                cl.direct_send(msg, thread_ids=[thread.id])

            print(f"Sent to {name}: {msg}")
            time.sleep(random.uniform(10, 40))

    except Exception as e:
        print(f"Broadcast error: {e}")

# ── SCHEDULER ─────────────────────────────────────────────────────────────────
def setup_scheduler():
    for t in SCHEDULED_TIMES:
        schedule.every().day.at(t).do(run_broadcast, scheduled_time=t)

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(30)

# ── MAIN LOOP ─────────────────────────────────────────────────────────────────
def run():
    from instagrapi.exceptions import LoginRequired

    cl = login()
    seen = load_seen()

    setup_scheduler()
    threading.Thread(target=scheduler_loop, daemon=True).start()

    while True:
        print(f"[Scan] {datetime.now().strftime('%H:%M:%S')}")

        try:
            with _cl_lock:
                threads = cl.direct_threads(amount=10)

            for thread in threads:
                if not thread.messages:
                    continue

                latest = thread.messages[0]
                msg_id = str(latest.id)

                if msg_id in seen:
                    continue

                if str(latest.user_id) == str(cl.user_id):
                    seen.add(msg_id)
                    continue

                text = latest.text or ""
                if len(text) < 2 or is_spam(text):
                    seen.add(msg_id)
                    continue

                name = thread.thread_title or "user"
                history = build_history(thread, str(cl.user_id))
                history.append({"role": "user", "content": text})

                reply = generate_reply(history, name)

                if reply:
                    with _cl_lock:
                        cl.direct_send(reply, thread_ids=[thread.id])

                    print(f"Replied to {name}: {reply}")
                    time.sleep(random.uniform(5, 15))
                    seen.add(msg_id)
                    save_seen(seen)
                else:
                    print(f"LLM failed for {name}, will retry next scan")

        except Exception as e:
            print(f"Error: {e}")

            if "login_required" in str(e).lower():
                print("⚠️ Session expired. STOPPING.")
                exit()

        time.sleep(CHECK_EVERY)


if __name__ == "__main__":
    run()