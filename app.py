"""
Provide the Streamlit interface for PDF resume analysis and job discovery.
Display resume summaries, skill gaps, and career roadmaps generated with
Groq, then retrieve LinkedIn and Indeed listings through Apify.
"""

import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_indeed_jobs, fetch_linkedin_jobs
st.write("✅ Streamlit is working")

st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("💼 AI Job Recommender")
st.markdown("Upload your resume and get personalized recommendations based on your skills and experience from LinkedIn and Indeed.")

file_upload = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])

if file_upload:
    with st.spinner("🔍 Extracting text from resume..."):
        resume_text = extract_text_from_pdf(file_upload)

    with st.spinner("🧠 Summarizing your resume..."):
        summary = ask_openai(
            f"Summarize this resume and highlight key skills, education, experiences, and features:\n\n{resume_text}",
            max_tokens=500
        )

    with st.spinner("📊 Finding skill gaps..."):
        gaps = ask_openai(
            f"Analyze this resume and highlight missing skill gaps, certifications, and experience needed for better jobs:\n\n{resume_text}",
            max_tokens=400
        )

    with st.spinner("🗺️ Creating future roadmap..."):
        roadmap = ask_openai(
            f"Based on this resume, suggest a future roadmap to improve the person's career. Mention skills, certifications needed, and industry exposure:\n\n{resume_text}",
            max_tokens=300
        )

    # Display results
    st.markdown("---")
    st.header("📄 Resume Summary")
    st.markdown(
        f"<div style='background-color:#1e1e1e; padding:15px; border-radius:10px; font-size:16px; color:white;'>{summary}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(
        f"<div style='background-color:#1e1e1e; padding:15px; border-radius:10px; font-size:16px; color:white;'>{gaps}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.header("🧭 Future Roadmap & Preparation Strategy")
    st.markdown(
        f"<div style='background-color:#1e1e1e; padding:15px; border-radius:10px; font-size:16px; color:white;'>{roadmap}</div>",
        unsafe_allow_html=True
    )

    st.success("✅ Analysis Completed Successfully!")

    if st.button("🔵 Get Job Recommendations"):
        with st.spinner("Fetching job recommendations..."):
            keywords = ask_openai(
                f"Based on this resume summary, suggest the best job titles and keywords for searching:\n\n{summary}",
                max_tokens=100
            )
            search_keywords_clean = keywords.replace("\n", "").strip()

        st.success(f"Extracted Job Keywords: \n{search_keywords_clean}")

        with st.spinner("Fetching jobs from LinkedIn and Indeed..."):
            try:
                linked_jobs = fetch_linkedin_jobs(search_keywords_clean, rows=80)
            except Exception as e:
                st.error(f"Failed to fetch LinkedIn jobs: {e}")
                linked_jobs = []

            try:
                indeed_jobs = fetch_indeed_jobs(search_keywords_clean, rows=60)
            except Exception as e:
                st.error(f"Failed to fetch Indeed jobs: {e}")
                indeed_jobs = []

        # LinkedIn Jobs
        st.markdown("---")
        st.header("💼 Top LinkedIn Jobs")

        if linked_jobs:
            for job in linked_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"📍 {job.get('location')}")
                st.markdown(f"🔗 [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No LinkedIn jobs found for the given keywords.")

        # Indeed Jobs
        st.markdown("---")
        st.header("🧳 Top Indeed Jobs")

        if indeed_jobs:
            for job in indeed_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"📍 {job.get('location')}")
                st.markdown(f"🔗 [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No Indeed jobs found for the given keywords.")
