# 🎓 Interview Preparation Coach

## 📝 Overview
The **Interview Preparation Coach** is a multi-agent AI-powered platform built using AutoGen and Groq's LLaMA-based models. It provides structured learning, interview questions, MCQs, and feedback to help users enhance their knowledge and practice for technical interviews.

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
pip install -r requirements.txt
```

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/vibhhav/AI-Interview-Coach.git
cd AI-Interview-Coach
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
-  Enter the subject and topic you want to practice.
- Generate structured lessons for in-depth understanding.
- Generate MCQs and answer them to test your knowledge.
- Submit MCQ answers and receive detailed evaluations.
- Generate interview questions based on difficulty level.
- Write answers and receive AI-driven feedback.

## 📸 Screenshots
![Image](https://github.com/user-attachments/assets/c7d91725-ed60-45e2-8add-ff66defdef4d)

![Image](https://github.com/user-attachments/assets/981c7393-99a9-4303-be54-6e1a7566665c)

![Image](https://github.com/user-attachments/assets/375a3968-4262-4a9b-b741-35a46063ffd7)

![Image](https://github.com/user-attachments/assets/f868566f-d0b4-4cc0-81a5-315337f9e0ae)

## 📌 Technologies Used
- **Python** (Backend logic)
- **Streamlit** (UI framework)
- **AutoGen** (AI agents management)
- **Groq API** (LLaMA-3.3-70B Model)

## 🏗️ Future Enhancements
-  Voice-based mock interviews using Whisper API
 - Resume-based question generation
 - Web Dashboard with user progress tracking



