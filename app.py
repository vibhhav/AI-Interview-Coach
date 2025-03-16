import streamlit as st
import os
from dotenv import load_dotenv
from autogen import AssistantAgent

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

        # MCQs Generator (now takes lesson content as input)
        self.mcq_agent = AssistantAgent(
            name="mcq_agent",
            system_message="Generate multiple-choice questions (MCQs) based on the provided lesson content. Follow this exact format for each question:\n\nQ1. [Question text]\nA) [Option A]\nB) [Option B]\nC) [Option C]\nD) [Option D]\n\nCorrect Answer: [Letter]\n\nEach question must be numbered with Q followed by the number. Each option must start with a capital letter followed by a parenthesis. DO NOT include explanations or additional text.",
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

        # Interview Question Generator (now with realistic questions)
        self.interview_agent = AssistantAgent(
            name="interview_agent",
            system_message="Generate a realistic interview question for the given topic, considering the specified difficulty level. Ask questions that are commonly asked in actual job interviews - focus on conceptual understanding, problem-solving approaches, past experiences, behavioral scenarios, or industry trends rather than coding exercises. If the user's previous performance is provided, adjust the difficulty accordingly.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        # Feedback Agent - update this system message
        self.feedback_agent = AssistantAgent(
            name="feedback_agent",
            system_message="Evaluate the user's answer as if it were given in a real interview setting. Consider communication skills, clarity, technical accuracy, and how well they demonstrate understanding of the subject. Provide constructive feedback that focuses on both strengths and areas for improvement, similar to what an interviewer would consider. Return a rating from 1-5, where 1 is poor and 5 is excellent. Format your response like this: 'Rating: X/5\n\nFeedback: [Your detailed feedback here]'",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        # Overall Performance Agent
        self.performance_agent = AssistantAgent(
            name="performance_agent",
            system_message="Analyze the user's overall performance across both MCQs and interview questions. Provide a comprehensive evaluation highlighting strengths, areas for improvement, and specific recommendations for further study. Include quantitative metrics where available.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

    def generate_lesson(self, subject, topic):
        """Generates a structured lesson plan."""
        # If topic is empty, create a lesson about the general subject
        content = f"Create a detailed lesson plan on {topic} for {subject}." if topic else f"Create a detailed lesson plan on {subject}."
        
        response = self.lesson_agent.generate_reply(
            messages=[{"role": "user", "content": content}]
        )
        return response.get("content", "Lesson generation failed!") if isinstance(response, dict) else str(response)

    def generate_mcqs_from_lesson(self, lesson_content, num_questions):
        """Generates MCQs based on the lesson content."""
        response = self.mcq_agent.generate_reply(
            messages=[{
                "role": "user",
                "content": f"Generate {num_questions} DIFFERENT MCQs based on the following lesson content. Ensure these questions are diverse and cover various aspects of the material:\n\n{lesson_content}"
            }]
        )
        return response.get("content", "MCQ generation failed!") if isinstance(response, dict) else str(response)

    def evaluate_mcq_answers(self, user_answers):
        """Evaluates the user's MCQ answers and provides explanations."""
        response = self.mcq_feedback_agent.generate_reply(
            messages=[
                {"role": "user", "content": f"Evaluate these MCQ answers: {user_answers}"}]
        )
        return response.get("content", "Evaluation failed!") if isinstance(response, dict) else str(response)

    def generate_next_interview_question(self, subject, topic, current_difficulty, previous_performance=None):
        """Generates the next interview question based on previous performance."""
        # If topic is empty, generate questions about the general subject
        content = f"Generate a single {current_difficulty} realistic interview question for {topic} in {subject}. Make sure this question is DIFFERENT from any previous questions." if topic else f"Generate a single {current_difficulty} realistic interview question about {subject}. Ensure this is a UNIQUE question that hasn't been asked before."
        
        if previous_performance:
            content += f"\n\nPrevious performance: {previous_performance}"
        
        # Add this line to track previous questions if you want to be extra sure
        if hasattr(self, 'previous_questions') and self.previous_questions:
            content += f"\n\nPrevious questions (DO NOT ask these again): {', '.join(self.previous_questions[-5:])}"
        
        response = self.interview_agent.generate_reply(
            messages=[{"role": "user", "content": content}]
        )
        
        # Store this question for future reference
        if not hasattr(self, 'previous_questions'):
            self.previous_questions = []
        
        question = response.get("content", "Question generation failed!") if isinstance(response, dict) else str(response)
        self.previous_questions.append(question)
        
        return question


    def evaluate_answer(self, question, user_answer):
        """Evaluates user's answer and provides feedback with a rating."""
        response = self.feedback_agent.generate_reply(
            messages=[
                {"role": "user", "content": f"Question: {question}\n\nUser's Answer: {user_answer}\n\nEvaluate this answer:"}]
        )
        return response.get("content", "Evaluation failed!") if isinstance(response, dict) else str(response)

    def get_overall_performance(self, mcq_results, interview_results):
        """Provides an overall assessment of the user's performance."""
        combined_results = f"MCQ Results:\n{mcq_results}\n\nInterview Results:\n{interview_results}"
        
        response = self.performance_agent.generate_reply(
            messages=[
                {"role": "user", "content": f"Analyze the user's overall performance based on these results:\n\n{combined_results}"}]
        )
        return response.get("content", "Performance analysis failed!") if isinstance(response, dict) else str(response)


# Streamlit UI
st.title("🎓Interview Preparation Coach")

# Retrieving API key from environment variables
api_key = os.getenv("GROQ_API_KEY")

# Checking if API key is set
if not api_key:
    st.error("GROQ_API_KEY is missing. Please set it in your environment variables.")
    st.stop()

# Initializing AI Agents
agents = TutorAgents(api_key)

# Initialize session state variables
if "lesson_content" not in st.session_state:
    st.session_state.lesson_content = ""
if "mcq_questions" not in st.session_state:
    st.session_state.mcq_questions = []
if "mcq_answers" not in st.session_state:
    st.session_state.mcq_answers = {}
if "mcq_feedback" not in st.session_state:
    st.session_state.mcq_feedback = ""
if "current_interview_question" not in st.session_state:
    st.session_state.current_interview_question = ""
if "interview_history" not in st.session_state:
    st.session_state.interview_history = []
if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = "Medium"
if "interview_in_progress" not in st.session_state:
    st.session_state.interview_in_progress = False
if "overall_performance" not in st.session_state:
    st.session_state.overall_performance = ""
if "current_answer" not in st.session_state:
    st.session_state.current_answer = ""

# Sidebar for user input
with st.sidebar:
    st.header("Setup")
    subject = st.text_input("**Enter the subject:**")
    topic = st.text_input("**Enter a specific topic:**")
    st.divider()
    st.header("Settings")
    num_mcqs = st.number_input("Number of MCQs:", min_value=1, max_value=20, value=5, step=1)
    initial_difficulty = st.selectbox("Initial Interview Difficulty:", ["Easy", "Medium", "Hard"], index=1)

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📚 Lesson", "📝 MCQ Practice", "🎯 Interview Practice", "📊 Overall Performance"])

# Tab 1: Lesson Generation
with tab1:
    st.header("📚 Lesson Generator")
    
    if st.button("Generate Lesson"):
        if not subject.strip():
            st.error("Please enter at least a subject before generating a lesson.")
        else:
            # If topic is empty, we'll just use the subject as the general area
            lesson_topic = topic if topic.strip() else subject
            with st.spinner("Generating structured lesson..."):
                lesson = agents.generate_lesson(subject, lesson_topic)
                if lesson:
                    st.session_state.lesson_content = lesson
                    st.write(lesson)
                else:
                    st.error("Failed to generate a lesson.")

# Tab 2: MCQ Practice
with tab2:
    st.header("📝 MCQ Practice")
    
    # Generate MCQs from lesson
    if st.button("Generate MCQs from Lesson"):
        if not st.session_state.lesson_content:
            st.error("Please generate a lesson first.")
        else:
            with st.spinner("Generating MCQs based on the lesson..."):
                mcq_text = agents.generate_mcqs_from_lesson(st.session_state.lesson_content, num_mcqs)
                
                if mcq_text:
                    st.session_state.raw_mcq_text = mcq_text
                    
                    # Parsing the MCQs
                    questions = []
                    current_question = None
                    
                    lines = mcq_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Looking for a new question
                        if line.startswith('Q') and len(line) > 1 and line[1:].strip()[0].isdigit():
                            # Saving the previous question
                            if current_question and 'text' in current_question:
                                questions.append(current_question)
                            
                            # Starting a new question
                            current_question = {
                                'text': line,
                                'options': [],
                                'correct': None
                            }
                        
                        # Looking for options
                        elif line.startswith(('A)', 'B)', 'C)', 'D)')) and current_question:
                            current_question['options'].append(line)
                        
                        # Looking for correct answer
                        elif line.startswith('Correct Answer:') and current_question:
                            current_question['correct'] = line.split(':')[1].strip()
                    
                    # Adding the last question
                    if current_question and 'text' in current_question and current_question['options']:
                        questions.append(current_question)
                    
                    # Storing in session state
                    st.session_state.mcq_questions = questions
                    st.session_state.mcq_answers = {i: None for i in range(len(questions))}
    
    # Display MCQs
    if st.session_state.mcq_questions:
        st.subheader("📌 MCQs:")
        for i, q in enumerate(st.session_state.mcq_questions):
            st.markdown(f"### {q['text']}")
            
            for option in q['options']:
                st.markdown(option)
            
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
        
        # Submit MCQ Answers
        if st.button("Submit MCQ Answers"):
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
                    st.session_state.mcq_feedback = feedback_mcq
                    st.subheader("📊 MCQ Feedback & Evaluation")
                    st.write(feedback_mcq)
                else:
                    st.error("Failed to evaluate your answers. Please try again.")

# Tab 3: Interview Practice
with tab3:
    st.header("🎯 Interview Practice")
    
    if not st.session_state.interview_in_progress:
        # Start interview button
        if st.button("Start Interview Practice"):
            if not subject.strip():
                st.error("Please enter at least a subject before starting the interview.")
            else:
                # If topic is empty, we'll just use the subject as the general area
                interview_topic = topic if topic.strip() else subject
                st.session_state.interview_in_progress = True
                st.session_state.current_difficulty = initial_difficulty
                st.session_state.interview_history = []
                st.session_state.current_answer = ""
                
                # Generate the first question
                with st.spinner("Generating first interview question..."):
                    question = agents.generate_next_interview_question(subject, interview_topic, st.session_state.current_difficulty)
                    st.session_state.current_interview_question = question
                st.rerun()
    else:
        # Display current question
        st.subheader("Current Question:")
        st.write(st.session_state.current_interview_question)
        
        # User answer
        # User answer - using session state to maintain/clear value appropriately
        user_answer = st.text_area("Your Answer:", value=st.session_state.current_answer, height=200, key="answer_input")
        
        # Submit answer
        if st.button("Submit Answer"):
            if not user_answer.strip():
                st.error("Please provide an answer before submitting.")
            else:
                with st.spinner("Evaluating your answer..."):
                    feedback = agents.evaluate_answer(st.session_state.current_interview_question, user_answer)
                    
                    # Extract rating from feedback
                    rating = 3  # Default rating
                    if "Rating:" in feedback:
                        try:
                            rating_text = feedback.split("Rating:")[1].split("\n")[0].strip()
                            rating = int(rating_text.split("/")[0].strip())
                        except:
                            pass
                    
                    # Store the Q&A in history
                    st.session_state.interview_history.append({
                        "question": st.session_state.current_interview_question,
                        "answer": user_answer,
                        "feedback": feedback,
                        "rating": rating,
                        "difficulty": st.session_state.current_difficulty
                    })
                    
                    # Clear user answer
                    st.session_state.current_answer = ""  # Ensure answer is cleared

                    # Display feedback
                    st.subheader("Feedback:")
                    st.write(feedback)
                    
                    # Adjust difficulty based on rating
                    difficulties = ["Easy", "Medium", "Hard"]
                    current_index = difficulties.index(st.session_state.current_difficulty)
                    
                    if rating >= 4 and current_index < 2:
                        st.session_state.current_difficulty = difficulties[current_index + 1]
                    elif rating <= 2 and current_index > 0:
                        st.session_state.current_difficulty = difficulties[current_index - 1]
                    
                    # Generate the next interview question
                    with st.spinner("Generating next interview question..."):
                        next_question = agents.generate_next_interview_question(subject, topic, st.session_state.current_difficulty)
                        st.session_state.current_interview_question = next_question

                    # Force re-run to refresh the text area
                    st.rerun()

        
        # Option to end interview
        if st.button("End Interview"):
            st.session_state.interview_in_progress = False
            st.success("Interview completed. Check the Overall Performance tab for your results.")
            st.rerun()
        
        # Display interview history
        if st.session_state.interview_history:
            st.subheader("Interview History")
            for i, qa in enumerate(st.session_state.interview_history):
                with st.expander(f"Question {i+1} ({qa['difficulty']})"):
                    st.write(f"**Question:** {qa['question']}")
                    st.write(f"**Your Answer:** {qa['answer']}")
                    st.write(f"**Feedback:** {qa['feedback']}")

# Tab 4: Overall Performance
with tab4:
    st.header("📊 Overall Performance")
    
    if st.button("Generate Overall Performance Report"):
        if not st.session_state.mcq_feedback and not st.session_state.interview_history:
            st.error("Complete at least one MCQ test or interview question before generating a report.")
        else:
            with st.spinner("Analyzing your overall performance..."):
                # Prepare MCQ results
                mcq_results = st.session_state.mcq_feedback if st.session_state.mcq_feedback else "No MCQ data available."
                
                # Prepare interview results
                interview_results = "No interview data available."
                if st.session_state.interview_history:
                    interview_results = "Interview Questions Summary:\n\n"
                    for i, qa in enumerate(st.session_state.interview_history):
                        interview_results += f"Question {i+1} ({qa['difficulty']}):\n"
                        interview_results += f"Question: {qa['question']}\n"
                        interview_results += f"Rating: {qa['rating']}/5\n\n"
                
                # Generate overall performance report
                overall_report = agents.get_overall_performance(mcq_results, interview_results)
                st.session_state.overall_performance = overall_report
                
                # Display report
                st.subheader("📑 Overall Performance Report")
                st.write(overall_report)
    
    # Display existing report if available
    elif st.session_state.overall_performance:
        st.subheader("📑 Overall Performance Report")
        st.write(st.session_state.overall_performance)
    else:
        st.info("Complete MCQ tests and interview questions, then generate a report to see your overall performance.")
