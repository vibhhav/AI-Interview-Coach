import streamlit as st
import os
from dotenv import load_dotenv
from agents import TutorAgents

# Load environment variables
load_dotenv()

# Streamlit UI Title
st.title("🎓 Interview Preparation Coach")

st.subheader("📝 Preperation")

# Retrieve API key from environment variables
api_key = os.getenv("GROQ_API_KEY")

# Check if API key is set
if not api_key:
    st.error("GROQ_API_KEY is missing. Please set it in your environment variables.")
    st.stop()

# Initialize AI Agents
agents = TutorAgents(api_key)

# User selects a subject
subject = st.text_input("**Enter the subject you want to practice:**")
topic = st.text_input("**Enter a specific topic:**")
# Initialize session state for interview questions and answers
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# Generate Lesson
if st.button("Generate Lesson"):
    if not subject.strip():
        st.error("Please enter both a subject and a topic before generating a lesson.")
    else:
        with st.spinner("Generating structured lesson..."):
            lesson = agents.generate_lesson(subject, topic)
            if lesson:
                st.write(lesson)
            else:
                st.error("Failed to generate a lesson.")

st.subheader("📝 MCQ Practice")

num_mcqs = st.number_input("Number of MCQs:", min_value=1, max_value=20, value=5, step=1)

if st.button("Generate MCQs"):
    if not subject.strip():
        st.error("Please enter both a subject and a topic before generating MCQs.")
    else:
        with st.spinner("Generating multiple-choice questions..."):
            mcq_text = agents.generate_mcqs(subject, topic, num_mcqs)

            if mcq_text:
                st.subheader("📌 MCQs:")
                questions = []
                current_question = {}
                question_count = 0

                for line in mcq_text.split("\n"):
                    line = line.strip()
                    if not line:
                        continue
        
                    if line.startswith("Q"):
                        # Save previous question if it exists
                        if current_question:
                            questions.append(current_question)
                            
                        # Start new question
                        question_count += 1
                        current_question = {
                            "question": line,
                            "options": [],
                            "answer_index": None
                        }
                    elif line.startswith(("A)", "B)", "C)", "D)")):
                        if current_question:
                            current_question["options"].append(line)
                    elif line.startswith("Correct Answer:") and current_question:
                        current_question["correct"] = line

            # Add the last question
                if current_question:
                    questions.append(current_question)

                # Store in session state
                st.session_state.mcq_questions = questions
                st.session_state.mcq_answers = {i: "" for i in range(len(questions))}

if "mcq_questions" in st.session_state and st.session_state.mcq_questions:
    
    for i, q in enumerate(st.session_state.mcq_questions):
        st.markdown(f"### {q['question']}")
        
        for option in q["options"]:
            st.markdown(option)
        
        st.session_state.mcq_answers[i] = st.radio(
            "Your answer:",
            ["A", "B", "C", "D"],
            key=f"mcq_ans_{i}"
        )
        
        st.markdown("---")


if st.button("Submit MCQ Answers"):
    if not st.session_state.mcq_questions:
        st.error("❌ Please generate MCQs first!")
    else:
        with st.spinner("⏳ Evaluating your answers..."):
            user_mcq_responses = {i: st.session_state.mcq_answers[i] for i in range(len(st.session_state.mcq_questions))}
            feedback_mcq = agents.evaluate_mcq_answers(user_mcq_responses)

            if feedback_mcq:
                st.subheader("MCQ Feedback")
                st.markdown(feedback_mcq, unsafe_allow_html=True)


st.subheader("📝 Interview Practice")

num_questions = st.number_input("Number of Questions:", min_value=1, max_value=20, value=5, step=1)

# User selects difficulty level
difficulty = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])

# Generate Interview Questions
if st.button("Start Interview Practice"):
    if not subject.strip():
        st.error("Please enter both a subject and a topic before starting the interview practice.")
    else:
        with st.spinner("Generating interview questions..."):
            interview_text = agents.generate_interview_questions(subject, topic, num_questions, difficulty)

            if interview_text:
                st.subheader("📌 Interview Questions:")
            
            # Split and filter out the introductory line
                lines = [q.strip() for q in interview_text.split("\n") if q.strip()]
                if "Here are" in lines[0]:  # Remove AI-generated intro if present
                    lines.pop(0)

            # Store properly formatted questions
                st.session_state.interview_questions = lines  
                st.session_state.user_answers = {i: "" for i in range(len(lines))}

# Display Interview Questions
if st.session_state.interview_questions:
    for i, q in enumerate(st.session_state.interview_questions):
        st.write(f"**Q{q}**")
        st.session_state.user_answers[i] = st.text_area(f"Your Answer {i+1}:", value=st.session_state.user_answers[i], key=f"ans_{i}")


# Submit Answers & Get Feedback
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
                        f"Q{i+1}: {question}\n\n"
                        f"**📝 Your Answer:**\n{user_answer}\n\n"
                        f"**✅ Feedback:**\n{feedback}\n"
                        
                    )
                else:
                    feedback_results.append(
                        f"Q{i+1}: {question}\n\n"
                        f"**📝 Your Answer:** _No answer provided._\n\n"
                        f"**Feedback:** _Please provide an answer for evaluation._\n"
                        
                    )

            st.subheader("Interview Feedback")
            for result in feedback_results:
                st.markdown(result, unsafe_allow_html=True)

