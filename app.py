import streamlit as st
import os
from datetime import datetime

st.set_page_config(
    page_title="Job Application Agent",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

* { font-family: 'DM Sans', sans-serif; }
.main { background-color: #0f0f0f; }
.block-container { padding: 2rem 3rem; max-width: 1100px; }
.hero-title { font-family: 'DM Serif Display', serif; font-size: 3.2rem; color: #f5f0e8; line-height: 1.1; margin-bottom: 0.3rem; }
.hero-sub { font-size: 1rem; color: #888; margin-bottom: 2rem; letter-spacing: 0.02em; }
.section-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; color: #c8a96e; margin-bottom: 0.5rem; }
.status-box { background: #1a1a1a; border: 1px solid #2a2a2a; border-left: 3px solid #c8a96e; border-radius: 8px; padding: 1.2rem 1.5rem; margin: 1rem 0; color: #ccc; font-size: 0.9rem; }
.agent-badge { display: inline-block; background: #1e1e1e; border: 1px solid #333; border-radius: 20px; padding: 0.25rem 0.75rem; font-size: 0.75rem; color: #c8a96e; margin: 0.2rem; }
.result-header { font-family: 'DM Serif Display', serif; font-size: 1.6rem; color: #f5f0e8; margin-bottom: 1.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid #2a2a2a; }
.stButton > button { background: #c8a96e !important; color: #0f0f0f !important; border: none !important; border-radius: 6px !important; font-weight: 600 !important; font-size: 0.9rem !important; letter-spacing: 0.05em !important; padding: 0.6rem 1.5rem !important; transition: all 0.2s !important; }
.stButton > button:hover { background: #d4b97e !important; transform: translateY(-1px) !important; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea { background-color: #1a1a1a !important; border: 1px solid #2a2a2a !important; border-radius: 6px !important; color: #f5f0e8 !important; font-family: 'DM Sans', sans-serif !important; }
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: #c8a96e !important; box-shadow: 0 0 0 1px #c8a96e33 !important; }
.stFileUploader { background: #1a1a1a !important; border: 1px dashed #333 !important; border-radius: 6px !important; }
.stExpander { background: #1a1a1a !important; border: 1px solid #2a2a2a !important; border-radius: 8px !important; }
div[data-testid="stMarkdownContainer"] p { color: #ccc; line-height: 1.7; }
label { color: #aaa !important; font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "results_ready" not in st.session_state:
    st.session_state.results_ready = False
if "output_prefix" not in st.session_state:
    st.session_state.output_prefix = None
if "error" not in st.session_state:
    st.session_state.error = None

# --- HERO ---
st.markdown('<div class="hero-title">Job Application<br><i>Agent</i></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Powered by crewAI + Ollama &nbsp;·&nbsp; Runs entirely on your machine &nbsp;·&nbsp; 7 autonomous agents</div>', unsafe_allow_html=True)

agents = ["Job Researcher", "Company Analyst", "Hire Pattern Analyst", "Resume Tailor", "Cover Letter Writer", "Gap Analyst", "Email Drafter"]
badges = " ".join([f'<span class="agent-badge">{a}</span>' for a in agents])
st.markdown(badges, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# --- INPUTS ---
st.markdown('<div class="section-label">Target Role</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    company = st.text_input("Company", placeholder="e.g. Google", label_visibility="collapsed")
with col2:
    role = st.text_input("Role", placeholder="e.g. Software Engineer Intern", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Your Details</div>', unsafe_allow_html=True)
candidate_name = st.text_input("Full Name", placeholder="e.g. Moh Bhargava", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Your Resume</div>', unsafe_allow_html=True)
resume_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Recent Hire Profiles (Optional)</div>', unsafe_allow_html=True)
hire_profiles = st.text_area(
    "Profiles",
    placeholder="Paste LinkedIn profile text of recently hired people in this role...",
    height=80,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)
run = st.button("Run Agent Crew →", use_container_width=False)

# --- RUN ---
if run:
    if not company or not role:
        st.error("Please enter both company name and role.")
    elif resume_file is None:
        st.error("Please upload your resume PDF.")
    else:
        st.session_state.results_ready = False
        st.session_state.output_prefix = None
        st.session_state.error = None

        resume_path = f"temp_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        with open(resume_path, "wb") as f:
            f.write(resume_file.read())

        st.markdown(f"""
        <div class="status-box">
            ⏳ &nbsp; Running crew for <strong>{role}</strong> at <strong>{company}</strong><br>
            <span style="color:#666; font-size:0.8rem;">This takes 5–15 minutes. All 7 agents run sequentially.</span>
        </div>
        """, unsafe_allow_html=True)

        with st.status("Running agent crew...", expanded=True) as status:
            st.write("🔍 Job Researcher — finding the job posting...")
            try:
                from src.job_application_agent.crew import run_crew

                # We'll update status as crew runs
                status.update(label="🏢 Company Analyst — researching the company...")
                
                run_crew(
                    company=company,
                    role=role,
                    resume_path=resume_path,
                    hire_profiles=hire_profiles if hire_profiles else None,
                    candidate_name=candidate_name if candidate_name else "Candidate"
                )

                output_files = sorted([
                    f for f in os.listdir("outputs") if f.endswith(".txt")
                ], reverse=True)
                if output_files:
                    st.session_state.output_prefix = output_files[0][:15]
                    st.session_state.results_ready = True
                
                status.update(label="✅ All agents completed!", state="complete")

            except Exception as e:
                st.session_state.error = str(e)
                status.update(label="❌ Something went wrong", state="error")
            finally:
                if os.path.exists(resume_path):
                    os.remove(resume_path)

# --- ERRORS ---
if st.session_state.error:
    st.error(f"Something went wrong: {st.session_state.error}")

# --- RESULTS ---
if st.session_state.results_ready and st.session_state.output_prefix:
    st.success("✅ All 7 agents completed successfully")
    st.markdown("---")
    st.markdown('<div class="result-header">Your Application Package</div>', unsafe_allow_html=True)

    file_labels = {
        "tailored_resume": ("📝 Tailored Resume", True),
        "cover_letter": ("✉️ Cover Letter", True),
        "gap_report": ("📊 Gap Report & Interview Prep", True),
        "recruiter_email": ("📧 Recruiter Email", True),
        "job_research": ("🔍 Job Research", False),
        "company_research": ("🏢 Company Research", False),
        "hire_patterns": ("👥 Hire Patterns", False),
    }

    output_files = sorted([
        f for f in os.listdir("outputs") if f.endswith(".txt")
    ], reverse=True)
    latest = [f for f in output_files if st.session_state.output_prefix in f]

    for filename in latest:
        if "full_summary" in filename:
            continue
        for key, (label, expanded) in file_labels.items():
            if key in filename and filename.endswith(".txt"):
                with st.expander(label, expanded=expanded):
                    with open(f"outputs/{filename}", "r") as f:
                        content = f.read()
                    st.markdown(content)

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.download_button(
                            "⬇️ Download as text",
                            data=content,
                            file_name=filename,
                            mime="text/plain",
                            key=filename
                        )
                    with col_b:
                        pdf_filename = filename.replace(".txt", ".pdf")
                        if os.path.exists(f"outputs/{pdf_filename}"):
                            with open(f"outputs/{pdf_filename}", "rb") as f:
                                pdf_data = f.read()
                            st.download_button(
                                "⬇️ Download as PDF",
                                data=pdf_data,
                                file_name=pdf_filename,
                                mime="application/pdf",
                                key=pdf_filename
                            )