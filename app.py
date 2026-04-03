import streamlit as st
import pandas as pd

from scraper import get_jobs
from utils import remove_duplicates, filter_jobs, sort_jobs, calculate_match
from auth import signup, login
from bookmark_utils import save_bookmark, load_user_bookmarks
from application_utils import track_application, get_user_applications

st.set_page_config(page_title="JobSync", layout="wide")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = 1

# ---------------- AUTH ----------------
st.sidebar.title("🔐 Account")

if st.session_state.user is None:
    mode = st.sidebar.radio("Choose", ["Login", "Signup"])

    username = st.sidebar.text_input("Username")
    show = st.sidebar.checkbox("Show Password")
    password = st.sidebar.text_input("Password", type="default" if show else "password")

    if mode == "Signup":
        if st.sidebar.button("Create Account"):
            ok, msg = signup(username, password)
            st.sidebar.success(msg) if ok else st.sidebar.error(msg)

    if mode == "Login":
        if st.sidebar.button("Login"):
            if login(username, password):
                st.session_state.user = username
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials")

else:
    st.sidebar.write(f"👤 {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

# ---------------- FILTERS ----------------
st.sidebar.title("🔍 Filters")

keyword = st.sidebar.text_input("Keyword")
location = st.sidebar.selectbox("Location", ["All", "Remote", "India"])
role = st.sidebar.selectbox("Role", ["All", "Intern", "Developer"])
sort_option = st.sidebar.selectbox("Sort By", ["Latest", "Relevance"])
skills = st.sidebar.text_area("Paste your skills")

# ---------------- LOAD JOBS ----------------
@st.cache_data
def load_jobs():
    return get_jobs()

jobs = load_jobs()
jobs = remove_duplicates(jobs)
jobs = filter_jobs(jobs, keyword, location, role)
jobs = sort_jobs(jobs, keyword, sort_option)

# ---------------- PAGINATION ----------------
ITEMS = 5
start = (st.session_state.page - 1) * ITEMS
end = start + ITEMS
jobs_page = jobs[start:end]

st.title("🚀 JobSync")

# ---------------- DISPLAY ----------------
for i, job in enumerate(jobs_page):
    st.markdown(f"""
    ### {job['title']}
    **{job['company']}** | {job['location']}  
    📌 Source: {job.get('source','Unknown')}  
    [Apply Here]({job['link']})
    """)

    # Skill Match
    if skills:
        score = calculate_match(skills, job["title"])
        st.progress(score / 100)
        st.write(f"🎯 Match: {score}%")

    col1, col2 = st.columns(2)

    # APPLY BUTTON (FIXED KEY)
    if col1.button("🚀 Apply", key=f"apply_{i}_{job['title']}"):
        if st.session_state.user:
            track_application(st.session_state.user, job)
            st.success("Application tracked!")

    # SAVE BUTTON (FIXED KEY)
    if col2.button("⭐ Save", key=f"save_{i}_{job['title']}"):
        if st.session_state.user:
            save_bookmark(st.session_state.user, job)
            st.success("Saved!")

    st.divider()

# ---------------- PAGINATION ----------------
col1, col2, col3 = st.columns(3)

if col1.button("⬅️ Prev") and st.session_state.page > 1:
    st.session_state.page -= 1
    st.rerun()

if col3.button("Next ➡️") and end < len(jobs):
    st.session_state.page += 1
    st.rerun()

col2.write(f"Page {st.session_state.page}")

# ---------------- DASHBOARD ----------------
if st.session_state.user:
    st.subheader("📊 Dashboard")

    apps = get_user_applications(st.session_state.user)
    saved = load_user_bookmarks(st.session_state.user)

    if apps:
        df = pd.DataFrame(apps)
        st.metric("Applications", len(df))

        st.write("📈 Applications Over Time")
        st.line_chart(df["applied_on"].value_counts().sort_index())

        st.write("🏢 Top Companies")
        st.bar_chart(df["company"].value_counts())

    st.metric("⭐ Saved Jobs", len(saved))
