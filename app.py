import streamlit as st
import os
from dotenv import load_dotenv
from autogen import AssistantAgent
from dotenv import load_dotenv

load_dotenv()

# Creating Different Agents


class TutorAgents:
    def __init__(self, api_key):
        self.api_key = api_key
        self.llm_config = {'config_list': [
            {'model': 'llama-3.3-70b-versatile', 'api_key': self.api_key, 'api_type': "groq"}]}

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

        # MCQs Generator
        self.mcq_agent = AssistantAgent(
            name="mcq_agent",
            system_message="Generate multiple-choice questions (MCQs) for the given topic. Follow this exact format for each question:\n\nQ1. [Question text]\nA) [Option A]\nB) [Option B]\nC) [Option C]\nD) [Option D]\n\nCorrect Answer: [Letter]\n\nEach question must be numbered with Q followed by the number. Each option must start with a capital letter followed by a parenthesis. DO NOT include explanations or additional text.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        # MCQs Feedback Agent
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
            messages=[
                {"role": "user", "content": f"Create a detailed lesson plan on {topic} for {subject}."}]
        )
        return response.get("content", "Lesson generation failed!") if isinstance(response, dict) else str(response)

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
            messages=[
                {"role": "user", "content": f"Evaluate these MCQ answers: {user_answers}"}]
        )
        return response.get("content", "Evaluation failed!") if isinstance(response, dict) else str(response)

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
            messages=[
                {"role": "user", "content": f"Evaluate this answer: {user_answer}"}]
        )
        return response.get("content", "Evaluation failed!") if isinstance(response, dict) else str(response)


# Streamlit UI Title
st.title("🎓 Interview Preparation Coach")

st.subheader("📝 Preperation")

# Retrieving API key from environment variables
api_key = os.getenv("GROQ_API_KEY")

# Checking if API key is set
if not api_key:
    st.error("GROQ_API_KEY is missing. Please set it in your environment variables.")
    st.stop()

# Initializing AI Agents
agents = TutorAgents(api_key)

# User selects a subject
subject = st.text_input("**Enter the subject you want to practice:**")
topic = st.text_input("**Enter a specific topic:**")
# Initializing session state for interview questions and answers
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# Generating Lesson
if st.button("Generate Lesson"):
    if not subject.strip():
        st.error(
            "Please enter both a subject and a topic before generating a lesson.")
    else:
        with st.spinner("Generating structured lesson..."):
            lesson = agents.generate_lesson(subject, topic)
            if lesson:
                st.write(lesson)
            else:
                st.error("Failed to generate a lesson.")

st.subheader("📝 MCQ Practice")

num_mcqs = st.number_input(
    "Number of MCQs:", min_value=1, max_value=20, value=5, step=1)

# Generating MCQs
if st.button("Generate MCQs"):
    if not subject.strip():
        st.error("Please enter both a subject and a topic before generating MCQs.")
    else:
        with st.spinner("Generating multiple-choice questions..."):
            mcq_text = agents.generate_mcqs(subject, topic, num_mcqs)

            if mcq_text:
                st.session_state.raw_mcq_text = mcq_text  # Store the raw text
                st.subheader("📌 MCQs:")

                # Parsing the MCQs
                questions = []
                current_question = None

                lines = mcq_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    # Looking for a new question (starts with Q followed by a number)
                    if line.startswith('Q') and len(line) > 1 and line[1:].strip()[0].isdigit():
                        # Saving the previous question if it exists
                        if current_question and 'text' in current_question:
                            questions.append(current_question)

                        # Starting a new question
                        question_text = line
                        current_question = {
                            'text': question_text,
                            'options': [],
                            'correct': None
                        }

                    # Looking for options (starts with A), B), C), D))
                    elif line.startswith(('A)', 'B)', 'C)', 'D)')) and current_question:
                        current_question['options'].append(line)

                    # Looking for correct answer
                    elif line.startswith('Correct Answer:') and current_question:
                        current_question['correct'] = line.split(':')[
                            1].strip()

                # Adding the last question
                if current_question and 'text' in current_question and current_question['options']:
                    questions.append(current_question)

                # Storing in session state
                st.session_state.mcq_questions = questions
                st.session_state.mcq_answers = {
                    i: None for i in range(len(questions))}

# Displaying MCQs
if "mcq_questions" in st.session_state and st.session_state.mcq_questions:
    for i, q in enumerate(st.session_state.mcq_questions):
        st.markdown(f"### {q['text']}")

        for option in q['options']:
            st.markdown(option)

        # Don't show the correct answer to the user
        if 'correct' in q:
            # Store the correct answer in session state
            st.session_state.mcq_questions[i]['correct'] = q['correct']

        # Radio buttons for user selection
        user_choice = st.session_state.mcq_answers.get(i, None)
        
        user_choice = st.radio(
            "Your answer:",
            ["A", "B", "C", "D"],
            index=None if user_choice is None else ["A", "B", "C", "D"].index(user_choice),
            key=f"mcq_ans_{i}"
        )
        st.session_state.mcq_answers[i] = user_choice

        st.markdown("---")

# Submitting MCQ Answers
if st.button("Submit MCQ Answers"):
    if "mcq_questions" not in st.session_state or not st.session_state.mcq_questions:
        st.error("❌ Please generate MCQs first!")
    else:
        with st.spinner("⏳ Evaluating your answers..."):
            # Preparing detailed information for evaluation
            evaluation_text = "Here are the MCQs and the user's answers:\n\n"

            for i, q in enumerate(st.session_state.mcq_questions):
                evaluation_text += f"{q['text']}\n"
                for option in q['options']:
                    evaluation_text += f"{option}\n"

                if 'correct' in q and q['correct']:
                    evaluation_text += f"Correct Answer: {q['correct']}\n\n"

                user_ans = st.session_state.mcq_answers[i]
                evaluation_text += f"User's Answer: {user_ans}\n\n"

            # Sending for evaluation
            feedback_mcq = agents.evaluate_mcq_answers(evaluation_text)

            if feedback_mcq:
                st.subheader("📊 MCQ Feedback & Evaluation")

                # Extract score information
                

                # Explanation Breakdown
                st.markdown("---")
                st.markdown("### 📖 Question-Wise Explanation:")

                lines = feedback_mcq.split("\n")
                for line in lines:
                    line = line.strip()

                    if line.startswith("Q"):  # Question
                        st.markdown(f"**❓ {line}**")

                    elif "User's Answer:" in line:  # User's Answer
                        if "Incorrect" in line:
                            st.markdown(f"🚫 {line}")  # Red Cross for Incorrect
                        else:
                            st.markdown(f"✅ {line}")  # Green Tick for Correct

                    elif "Correct Answer:" in line:  # Correct Answer
                        st.markdown(f"**✔️ {line}**")

                    elif "Explanation:" in line:  # Explanation
                        st.markdown(f"📝 {line}")

                    elif "Suggestions for improvement:" in line:
                        st.markdown("---")
                        st.markdown("### 📈 Suggestions for Improvement:")

                    elif line:  # Regular Improvement Suggestions
                        st.markdown(f"{line}")

                st.markdown("---")
                st.success(
                    "🎯 Keep practicing, and you'll see great improvement!")

            else:
                st.error("Failed to evaluate your answers. Please try again.")


st.subheader("📝 Interview Practice")

num_questions = st.number_input(
    "Number of Questions:", min_value=1, max_value=20, value=5, step=1)

# User selects difficulty level
difficulty = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])

# Generating Interview Questions
if st.button("Start Interview Practice"):
    if not subject.strip():
        st.error(
            "Please enter both a subject and a topic before starting the interview practice.")
    else:
        with st.spinner("Generating interview questions..."):
            interview_text = agents.generate_interview_questions(
                subject, topic, num_questions, difficulty)

            if interview_text:
                st.subheader("📌 Interview Questions:")

            # Splitting and filtering out the introductory line
                lines = [q.strip()
                         for q in interview_text.split("\n") if q.strip()]
                if "Here are" in lines[0]:  # Remove AI-generated intro if present
                    lines.pop(0)

            # Storing properly formatted questions
                st.session_state.interview_questions = lines
                st.session_state.user_answers = {
                    i: "" for i in range(len(lines))}

# Displaying Interview Questions
if st.session_state.interview_questions:
    for i, q in enumerate(st.session_state.interview_questions):
        st.write(f"**Q{q}**")
        st.session_state.user_answers[i] = st.text_area(
            f"Your Answer {i+1}:", value=st.session_state.user_answers[i], key=f"ans_{i}")


# Submitting Answers & Getting Feedback
if st.button("Submit Answers"):
    if not st.session_state.interview_questions:
        st.error("❌ Please generate interview questions first!")
    else:
        with st.spinner("⏳ Evaluating your answers..."):
            feedback_results = []

            for i, question in enumerate(st.session_state.interview_questions):
                user_answer = st.session_state.user_answers[i].strip()
                feedback = agents.evaluate_answer(user_answer)

                if user_answer:
                    feedback_results.append(
                        f"Q{question}\n\n"
                        f"**📝 Your Answer:**\n{user_answer}\n\n"
                        f"**✅ Feedback:**\n{feedback}\n"

                    )
                else:
                    feedback_results.append(
                        f"Q{question}\n\n"
                        f"**📝 Your Answer:** _No answer provided._\n\n"
                        f"**Feedback:** _Please provide an answer for evaluation._\n"

                    )

            st.subheader("📊 Interview Feedback")
            for result in feedback_results:
                st.markdown(result, unsafe_allow_html=True)
            st.success(
                        "🎯 Keep practicing, and you'll see great improvement! 🚀")