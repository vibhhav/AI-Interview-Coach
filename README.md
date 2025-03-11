# 🎓 Interview Preparation Coach

## 📝 Overview
The **Interview Preparation Coach** is a multi-agent AI-powered platform built using Streamlit and Groq's LLaMA-based models. It provides structured learning, interview questions, MCQs, and feedback to help users enhance their knowledge and practice for technical interviews.

## 🚀 Features
- **Lesson Generator:** Creates structured learning modules on any given topic.
- **Interview Question Generator:** Provides technical and conceptual interview questions.
- **MCQ Generator:** Generates multiple-choice questions with correct answers.
- **Feedback Agent:** Evaluates user answers and provides constructive feedback.
- **MCQ Feedback Agent:** Scores user MCQ responses and explains correct/incorrect answers.

## 🛠️ Setup Instructions

### 1️⃣ Prerequisites
Ensure you have Python installed on your system. You will also need the following dependencies:

```bash
pip install streamlit python-dotenv autogen
```

### 2️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### 3️⃣ Set Up Environment Variables
Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

### 4️⃣ Run the Application
```bash
streamlit run app.py
```

## 🎯 How It Works
1. Enter the subject and topic you want to practice.
2. Generate structured lessons for in-depth understanding.
3. Generate MCQs and answer them to test your knowledge.
4. Submit MCQ answers and receive detailed evaluations.
5. Generate interview questions based on difficulty level.
6. Write answers and receive AI-driven feedback.

## 📸 Screenshots
(Include relevant screenshots of the application UI here)

## 📌 Technologies Used
- **Python** (Backend logic)
- **Streamlit** (UI framework)
- **AutoGen** (AI agents management)
- **Groq API** (LLaMA-3.3-70B Model)

## 🏗️ Future Enhancements
- Add support for video-based explanations.
- Improve answer evaluation using advanced NLP techniques.
- Implement personalized learning paths based on user performance.

## 🤝 Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to submit a pull request.

## 📜 License
MIT License

---
⚡ Happy Learning & Best of Luck for Your Interviews! 🚀
