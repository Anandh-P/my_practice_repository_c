import streamlit as st
import fitz  # PyMuPDF
import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ========== 🔐 DeepSeek API Key ==========
DEEPSEEK_API_KEY = "API KEY"  # Replace with your actual API key
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# ========== Session State Initialization ==========
defaults = {
    "pdf_text": "",
    "mcqs": [],
    "answers": [],
    "qna_questions": [],
    "qna_answers": [],
    "summary": "",
    "report": ""
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ========== Reset Button ==========
if st.sidebar.button("🔄 Reset All"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ========== DeepSeek API Function ==========
def ask_deepseek(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful AI tutor."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        st.error(f"Error from DeepSeek API: {response.text}")
        return None

# ========== Email Sending Function ==========
def send_email(subject, body, to_email, from_email, app_password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, app_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Email sending failed: {e}")
        return False

# ========== PDF Text Extraction ==========
def extract_text(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ========== Sidebar ==========
st.sidebar.title("🎯 Choose a Task")
task = st.sidebar.radio("Select One", [
    "Prepare MCQs",
    "Prepare Questions and Answers",
    "Prepare Summary"
])

st.sidebar.markdown("📄 Upload PDF to extract content")
uploaded_file = st.sidebar.file_uploader("Upload Notes/Textbook", type="pdf")
if uploaded_file and st.session_state.pdf_text == "":
    with st.spinner("Extracting text from PDF..."):
        st.session_state.pdf_text = extract_text(uploaded_file)
    st.sidebar.success("✅ PDF processed!")

pdf_content = st.session_state.pdf_text

# ========== Task 1: Prepare MCQs ==========
if task == "Prepare MCQs":
    st.title("🧠 MCQ Generator & Evaluator")
    if st.session_state.pdf_text:
        num_mcqs = st.number_input("How many MCQs to generate?", min_value=1, max_value=20, value=5)

        if st.button("Generate MCQs"):
            st.session_state.mcqs = []
            prompt = (
                f"Generate {num_mcqs} multiple-choice questions from the following study material. "
                "Each question must have 4 options labeled A., B., C., and D. "
                "Do NOT provide the correct answer. Avoid LaTeX formatting.\n\n"
                f"{pdf_content}"
            )
            with st.spinner("Generating MCQs..."):
                response = ask_deepseek(prompt)
                if response:
                    mcqs = []
                    for q in response.split("\n\n"):
                        q = q.strip()
                        if all(opt in q for opt in ["A.", "B.", "C.", "D."]) and "Answer:" not in q:
                            if not q.lower().startswith("q1: here are") and "these questions cover" not in q.lower():
                                mcqs.append(q)
                    st.session_state.mcqs = mcqs
                    st.success("✅ MCQs generated!")

        if st.session_state.mcqs:
            st.subheader("Answer the MCQs")
            with st.form("mcq_form"):
                st.session_state.answers = []
                for i, q in enumerate(st.session_state.mcqs):
                    st.markdown(f"**Q{i+1}:** {q}")
                    answer = st.radio(f"Your Answer for Q{i+1}", ["A", "B", "C", "D"], key=f"mcq_{i}")
                    st.session_state.answers.append(answer)
                submit_mcqs = st.form_submit_button("Submit Answers")

            if submit_mcqs:
                with st.spinner("Evaluating your answers..."):
                    combined = ""
                    for i, (q, a) in enumerate(zip(st.session_state.mcqs, st.session_state.answers)):
                        combined += f"{q}\nStudent Answer: {a}\n\n"
                    eval_prompt = (
                        "Evaluate the following student answers to MCQs:\n\n"
                        f"{combined}"
                        "1. Mark each answer correct or incorrect.\n"
                        "2. Provide the correct answer if wrong.\n"
                        "3. Score the student out of total.\n"
                        "4. Identify strong and weak areas.\n"
                    )
                    st.session_state.report = ask_deepseek(eval_prompt)

                if st.session_state.report:
                    st.markdown("### 📊 Evaluation Report")
                    st.markdown(st.session_state.report, unsafe_allow_html=True)

# ========== Task 2: Prepare Q&A ==========
elif task == "Prepare Questions and Answers":
    st.title("✍️ Short Answer Practice")
    if st.session_state.pdf_text:
        num_qna = st.number_input("How many questions to generate?", min_value=1, max_value=10, value=3)

        if st.button("Generate Questions"):
            st.session_state.qna_questions = []
            prompt = (
                f"Generate {num_qna} short-answer questions from the study material below. "
                "Do not include the answers.\n\n"
                f"{pdf_content}"
            )
            with st.spinner("Generating Questions..."):
                response = ask_deepseek(prompt)
                if response:
                    st.session_state.qna_questions = [q.strip() for q in response.split("\n") if q.strip()]
                    st.success("✅ Questions generated!")

        if st.session_state.qna_questions:
            st.subheader("Your Answers")
            with st.form("qna_form"):
                st.session_state.qna_answers = []
                for i, q in enumerate(st.session_state.qna_questions):
                    st.markdown(f"**Q{i+1}:** {q}")
                    ans = st.text_area("Your Answer:", key=f"qna_{i}")
                    st.session_state.qna_answers.append(ans)
                submit_qna = st.form_submit_button("Submit Answers")

            if submit_qna:
                with st.spinner("Evaluating your answers..."):
                    full_qna = ""
                    for q, a in zip(st.session_state.qna_questions, st.session_state.qna_answers):
                        full_qna += f"Question: {q}\nStudent's Answer: {a}\n\n"
                    eval_prompt = (
                        "Evaluate the following short-answer responses:\n\n"
                        f"{full_qna}"
                        "1. Score each answer out of 5.\n"
                        "2. Suggest corrections.\n"
                        "3. Identify weak areas and strengths.\n"
                    )
                    st.session_state.report = ask_deepseek(eval_prompt)

                if st.session_state.report:
                    st.markdown("### 📝 Q&A Evaluation Report")
                    st.markdown(st.session_state.report, unsafe_allow_html=True)

# ========== Task 3: Summary ==========
elif task == "Prepare Summary":
    st.title("📚 Smart Summary for Full Marks")
    if st.session_state.pdf_text:
        if st.button("Generate Powerful Summary"):
            prompt = (
                "Give a clear, short, bullet-based summary of the following content. "
                "Make it highly effective for school exams. Use plain expressions, no LaTeX.\n\n"
                f"{pdf_content}"
            )
            with st.spinner("Generating summary..."):
                st.session_state.summary = ask_deepseek(prompt)

        if st.session_state.summary:
            st.markdown("### ✅ Exam-Ready Summary")
            st.markdown(st.session_state.summary, unsafe_allow_html=True)

# ========== Shared: Send Report via Email ==========

# ✅ Hardcoded sender email (your Gmail) and app password
SENDER_EMAIL = "E-MAIL"
APP_PASSWORD = "APP PASSWORD "  # Use App Password from Gmail

if st.session_state.report or st.session_state.summary:
    st.markdown("### 📬 Send Report via Email")
    with st.form("email_form"):
        recipient = st.text_input("Recipient Email", key="email_recipient")
        subject = st.text_input("Subject", value="Your MCQ/Q&A Report", key="email_subject")

        body = st.session_state.report or st.session_state.summary or "No report available."

        submit_email = st.form_submit_button("Send Email")
        if submit_email:
            if send_email(subject, body, recipient, SENDER_EMAIL, APP_PASSWORD):
                st.success(f"📧 Email sent to {recipient} successfully!")
