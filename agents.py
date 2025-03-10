from autogen import AssistantAgent
from dotenv import load_dotenv

load_dotenv()

class TutorAgents:
    def __init__(self, api_key):
        self.api_key = api_key
        self.llm_config = {'config_list': [{'model': 'llama-3.3-70b-versatile', 'api_key': self.api_key, 'api_type': "groq"}]}

        # Lesson Generator
        self.lesson_agent = AssistantAgent(
            name="lesson_agent",
            system_message="Create detailed structured learning modules on the given topic. Ensure the lesson includes an introduction, key concepts, examples, and a summary. DO NOT include your thought process, just the lesson content.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        # Interview Question Generator
        self.interview_agent = AssistantAgent(
            name="interview_agent",
            system_message="Generate 5 interview-style questions for the given topic. Ensure a mix of technical and conceptual questions. DO NOT include answers, just the questions.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        # Feedback Agent
        self.feedback_agent = AssistantAgent(
            name="feedback_agent",
            system_message="Evaluate the user's answer based on clarity, accuracy, and depth. Provide constructive feedback with suggestions for improvement. DO NOT include your thought process, just the feedback.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

    def generate_lesson(self, subject, topic):
        """Generates a structured lesson plan."""
        response = self.lesson_agent.generate_reply(
            messages=[{"role": "user", "content": f"Create a lesson plan on {topic} for {subject}."}]
        )
        return response.get("content", "Lesson generation failed!") if isinstance(response, dict) else str(response)

    def generate_interview_questions(self, subject, topic, num_questions, difficulty):
        """Generates interview questions based on the selected count and difficulty."""
        response = self.interview_agent.generate_reply(
            messages=[{
            "role": "user",
            "content": f"Generate {num_questions} {difficulty} interview questions for {topic} in {subject}."
        }]
    )
        return response.get("content", "Interview question generation failed!") if isinstance(response, dict) else str(response)


    def evaluate_answer(self, user_answer):
        """Evaluates user's answer and provides feedback."""
        response = self.feedback_agent.generate_reply(
            messages=[{"role": "user", "content": f"Evaluate this answer: {user_answer}"}]
        )
        return response.get("content", "Evaluation failed!") if isinstance(response, dict) else str(response)
