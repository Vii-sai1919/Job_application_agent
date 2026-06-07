from dotenv import load_dotenv
load_dotenv()

from src.job_application_agent.crew import run_crew

def run():
    company = "Google"
    role = "Software Engineer Intern"
    resume_path = "resume.pdf"

    print("\n🚀 Starting Job Application Agent...\n")
    
    result = run_crew(
        company=company,
        role=role,
        resume_path=resume_path
    )

    print("\n✅ Done!\n")
    print(result)

if __name__ == "__main__":
    run()