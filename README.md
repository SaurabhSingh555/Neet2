# 🧠 NEET Quiz Generator from Uploaded Chapters

This project is an **offline quiz generator** that creates **NEET-style multiple-choice questions (MCQs)** from uploaded chapters in PDF, DOCX, or TXT format. It uses **transformers (T5)** and **NLTK** to generate questions locally — **no API keys or internet access required** for inference!

---

## 🚀 Features

- ✅ Upload chapters in **PDF, DOCX, or TXT** format
- 🧪 Automatically generates **5 NEET-style MCQs**
- 💡 Uses a **T5 transformer model** for question generation
- 🔒 Works **100% offline** — no OpenAI or external APIs
- 📚 Ideal for NEET, JEE, and other subject-specific quizzes

---

## 📁 File Support

| File Type | Supported | Example |
|-----------|-----------|---------|
| PDF       | ✅        | `chapter1.pdf` |
| DOCX      | ✅        | `biology_notes.docx` |
| TXT       | ✅        | `physics_laws.txt` |

---

## 🧰 Tech Stack

- Python 🐍
- [Transformers (Hugging Face)](https://huggingface.co/valhalla/t5-small-qa-qg-hl)
- NLTK (Natural Language Toolkit)
- PyMuPDF (`fitz`) for PDF handling
- python-docx for DOCX reading
- Google Colab UI for file uploads

---

## 📦 Installation

Clone this repo and install the required packages:

```bash
git clone https://github.com/yourusername/neet-quiz-generator.git
cd neet-quiz-generator
pip install -r requirements.txt
