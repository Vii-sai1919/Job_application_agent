from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.job_application_agent.tools.custom_tool import resume_read_tool, search_tool
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

@CrewBase
class JobApplicationCrew():
    """Job Application Agent Crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def job_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['job_researcher'],
            tools=[search_tool],
            verbose=True
        )

    @agent
    def company_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['company_analyst'],
            tools=[search_tool],
            verbose=True
        )

    @agent
    def hire_pattern_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['hire_pattern_analyst'],
            tools=[search_tool],
            verbose=True
        )

    @agent
    def resume_tailor(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_tailor'],
            tools=[resume_read_tool],
            verbose=True
        )

    @agent
    def cover_letter_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['cover_letter_writer'],
            verbose=True
        )

    @agent
    def gap_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['gap_analyst'],
            verbose=True
        )

    @agent
    def email_drafter(self) -> Agent:
        return Agent(
            config=self.agents_config['email_drafter'],
            verbose=True
        )

    @task
    def job_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_research_task'],
            agent=self.job_researcher()
        )

    @task
    def company_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['company_research_task'],
            agent=self.company_analyst()
        )

    @task
    def hire_pattern_task(self) -> Task:
        return Task(
            config=self.tasks_config['hire_pattern_task'],
            agent=self.hire_pattern_analyst()
        )

    @task
    def resume_tailor_task(self) -> Task:
        return Task(
            config=self.tasks_config['resume_tailor_task'],
            agent=self.resume_tailor()
        )

    @task
    def cover_letter_task(self) -> Task:
        return Task(
            config=self.tasks_config['cover_letter_task'],
            agent=self.cover_letter_writer()
        )

    @task
    def gap_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['gap_analysis_task'],
            agent=self.gap_analyst()
        )

    @task
    def email_draft_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_draft_task'],
            agent=self.email_drafter()
        )
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )


def save_outputs(crew_instance):
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    task_names = [
        "job_research", "company_research", "hire_patterns",
        "tailored_resume", "cover_letter", "gap_report", "recruiter_email"
    ]
    
    for i, task in enumerate(crew_instance.tasks):
        if task.output:
            filename = f"outputs/{timestamp}_{task_names[i]}.txt"
            with open(filename, "w") as f:
                f.write(str(task.output.raw))
            print(f"✅ Saved: {filename}")


def run_crew(company, role, resume_path, hire_profiles=None):
    inputs = {
        "company": company,
        "role": role,
        "resume_path": resume_path,
        "hire_profiles": hire_profiles or ""
    }
    
    job_crew = JobApplicationCrew()
    result = job_crew.crew().kickoff(inputs=inputs)
    save_outputs(job_crew)
    return result