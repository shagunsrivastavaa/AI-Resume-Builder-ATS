import streamlit as st
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="AI Resume Builder", layout="centered")

st.title("🚀 AI Resume Builder with ATS Score")

# Inputs
name = st.text_input("👤 Enter your name")
skills = st.text_area("🛠 Enter your skills (comma separated)")
job_desc = st.text_area("📄 Paste Job Description")


# 🔹 Resume Generator + ATS
def generate_resume(name, skills, job_desc):
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]

    # Resume content
    resume = f"""
{name.upper()}

PROFESSIONAL SUMMARY
Detail-oriented candidate with strong skills in {', '.join(skill_list[:3])}.
Skilled in data analysis, visualization, and problem-solving.

TECHNICAL SKILLS
"""
    for skill in skill_list:
        resume += f"- {skill}\n"

    resume += """
PROJECTS
- AI Resume Builder (this project)
- Data Analysis using Python

EXPERIENCE
- Academic and project-based experience
"""

    # 🔥 SMART KEYWORD EXTRACTION
    job_words = set(re.findall(r'\b[a-zA-Z]+\b', job_desc.lower()))

    stopwords = {
        "and", "the", "with", "for", "are", "this", "that",
        "using", "perform", "analyze", "intern", "learning"
    }

    job_words = job_words - stopwords

    # 🔥 SMART MATCHING (not exact)
    matched = []
    for skill in skill_list:
        skill_words = skill.lower().split()
        if any(word in job_words for word in skill_words):
            matched.append(skill)

    # 🔥 REALISTIC SCORE
    score = int((len(matched) / (len(skill_list) + 1)) * 100)
    score = min(score, 95)

    # Missing keywords
    missing = []
    for word in job_words:
        if word not in [s.lower() for s in skill_list]:
            if len(word) > 4:
                missing.append(word)

    return resume, score, matched, missing


# 📄 PDF FUNCTION
def create_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []
    for line in text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))
        content.append(Spacer(1, 8))

    doc.build(content)
    buffer.seek(0)
    return buffer


# BUTTON
if st.button("✨ Generate Resume"):
    if name and skills and job_desc:

        resume, score, matched, missing = generate_resume(name, skills, job_desc)

        # 📊 SCORE
        st.subheader("📊 ATS Match Score")
        st.progress(score / 100)

        if score < 50:
            st.error(f"Score: {score}% (Needs Improvement)")
        elif score < 80:
            st.warning(f"Score: {score}% (Good, can improve)")
        else:
            st.success(f"Score: {score}% (Excellent 🔥)")

        # ✔ MATCHED
        st.subheader("✔ Matching Skills")
        st.write(", ".join(matched) if matched else "None")

        # ❌ MISSING
        st.subheader("❌ Missing Keywords")
        st.write(", ".join(missing[:5]) if missing else "None")

        # 💡 TIPS
        st.subheader("💡 Improvement Tips")
        if score < 50:
            st.write("- Add missing keywords from job description")
            st.write("- Improve skill alignment")
        elif score < 80:
            st.write("- Add more relevant keywords")
        else:
            st.write("- Your resume is well optimized")

        # 📄 RESUME
        st.subheader("📄 Generated Resume")
        st.text_area("", resume, height=400)

        # 📥 DOWNLOAD
        pdf = create_pdf(resume)

        st.download_button(
            label="📥 Download Resume as PDF",
            data=pdf,
            file_name="resume.pdf",
            mime="application/pdf"
        )

    else:
        st.warning("Please fill all fields!")
