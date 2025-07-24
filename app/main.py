import streamlit as st
import sys
import os
import openai

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.tools.github_reader import get_github_issue, get_readme
from agent.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

st.title("🧠 HyperCoder – AI Engineer-in-a-Box")

def summarize_text(text):
    if not text:
        return "No content to summarize."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Summarize this:\n\n{text}"}]
    )
    return response.choices[0].message["content"]

owner = st.text_input("GitHub Owner (e.g., 'openai')")
repo = st.text_input("Repo (e.g., 'gpt-2')")
issue_number = st.number_input("Issue Number", step=1)

if st.button("Read Issue"):
    issue = get_github_issue(owner, repo, issue_number)
    readme = get_readme(owner, repo)

    st.subheader("🪵 Issue Content")
    st.markdown(f"### 📝 Title: {issue.get('title', 'N/A')}")

    labels = issue.get("labels", [])
    if labels:
        label_names = [label['name'] for label in labels]
        st.markdown(f"🏷️ Labels: {', '.join(label_names)}")
    else:
        st.markdown("🏷️ Labels: None")

    st.write(issue.get("body", "Not found"))

    st.subheader("🧠 Summary of Issue")
    summary = summarize_text(issue.get("body", ""))
    st.write(summary)

    st.subheader("📘 README")
    st.code(readme)
