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
            system_message="Generate interview-style questions for the given topic. Ensure a mix of technical and conceptual questions. DO NOT include answers, just the questions.",
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

        self.mcq_agent = AssistantAgent(
    name="mcq_agent",
    system_message="Generate multiple-choice questions (MCQs) for the given topic. Follow this exact format for each question:\n\nQ1. [Question text]\nA) [Option A]\nB) [Option B]\nC) [Option C]\nD) [Option D]\n\nCorrect Answer: [Letter]\n\nEach question must be numbered with Q followed by the number. Each option must start with a capital letter followed by a parenthesis. DO NOT include explanations or additional text.",
    llm_config=self.llm_config,
    human_input_mode="NEVER",
    code_execution_config=False
)

        # MCQ Feedback Agent
        self.mcq_feedback_agent = AssistantAgent(
            name="mcq_feedback_agent",
            system_message="Evaluate the user's MCQ answers. Provide a score, explanations for correct/incorrect responses, and suggestions for improvement.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

    def generate_lesson(self, subject, topic):
        """Generates a structured lesson plan."""
        response = self.lesson_agent.generate_reply(
            messages=[{"role": "user", "content": f"Create a detailed lesson plan on {topic} for {subject}."}]
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
    
    def generate_mcqs(self, subject, topic, num_questions):
        """Generates multiple-choice questions (MCQs) with correct answers and explanations."""
        response = self.mcq_agent.generate_reply(
            messages=[{
                "role": "user",
                "content": f"Generate {num_questions} MCQs on {topic} in {subject}. Provide four answer choices for each question "
            }]
        )
        return response.get("content", "MCQ generation failed!") if isinstance(response, dict) else str(response)

    def evaluate_mcq_answers(self, user_answers):
        """Evaluates the user's MCQ answers and provides explanations and improvement scope."""
        response = self.mcq_feedback_agent.generate_reply(
            messages=[{"role": "user", "content": f"Evaluate these MCQ answers: {user_answers}"}]
        )
        return response.get("content", "Evaluation failed!") if isinstance(response, dict) else str(response)
