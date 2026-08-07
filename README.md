# AI English Writing & Speaking Evaluator

AI-powered English evaluation dashboard built with **Streamlit** for practicing and evaluating English writing and speaking performance.

## ✨ Features

- ✍️ **Writing Evaluation** — feedback for Grammar, Vocabulary, and Coherence.
- 🎙️ **Speaking Evaluation** — record/upload audio and evaluate Fluency, Grammar, and Vocabulary.
- 💡 **Sample Latihan** — 5 sample writing texts and 5 sample audio samples.
- 🕒 **History & Export** — evaluation history and CSV export.
- 🔌 **API Status** — OpenRouter and Groq API availability indicators.
- 🌌 **Modern UI** — futuristic dark dashboard with custom HTML/CSS styling.

## 🛠️ Tech Stack

- Python
- Streamlit
- OpenRouter API — AI evaluation
- Groq API — Speech-to-Text
- HTML/CSS — custom Streamlit UI

## 📁 Project Structure

```text
english_ai_eva/
├── app.py
├── requirements.txt
├── README.md
├── pages/
│   └── ...
├── assets/
│   └── ...
└── .streamlit/
    └── secrets.toml
```

> Adjust the structure above to match the files in your repository.

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/USERNAME/english_ai_eva.git
cd english_ai_eva
```

Replace `USERNAME` with your GitHub username.

### 2. Create a virtual environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If your Mac uses `pip3`:

```bash
pip3 install -r requirements.txt
```

## 🔑 API Configuration

The application expects these environment variables:

```text
OPENROUTER_API_KEY
GROQ_API_KEY
```

### Local development

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
OPENROUTER_API_KEY = "sk-or-v1-xxxxxxxxxxxxxxxx"
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxx"
```

**Never commit real API keys to GitHub.**

Recommended `.gitignore`:

```gitignore
.streamlit/secrets.toml
.env
__pycache__/
*.pyc
.venv/
```

## ▶️ Run the Application

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit, normally:

```text
http://localhost:8501
```

## ☁️ Deploy to Streamlit Cloud

1. Push the project to GitHub.
2. Create a new Streamlit app.
3. Select the GitHub repository.
4. Select `app.py` as the main file.
5. Open **Settings → Secrets**.
6. Add:

```toml
OPENROUTER_API_KEY = "sk-or-v1-xxxxxxxxxxxxxxxx"
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxx"
```

7. Save and restart/redeploy the application.

When both keys are detected, the dashboard displays:

```text
OpenRouter API ✓   |   Groq API ✓
```

## 🔌 API Status Logic

The application checks API availability using:

```python
openrouter_ok = bool(os.environ.get("OPENROUTER_API_KEY"))
groq_ok = bool(os.environ.get("GROQ_API_KEY"))
```

If both keys are available, the app shows **"Aplikasi siap digunakan!"**.

If a key is missing, the app displays a warning and configuration instructions.

## 🎯 Use Cases

- English writing practice
- English speaking practice
- Grammar improvement
- Vocabulary improvement
- Fluency practice
- AI-assisted English learning
- English performance tracking

## 🔐 Security

Never expose API keys in:

- GitHub source code
- `README.md`
- screenshots
- public repositories
- client-side/frontend code

Use Streamlit Secrets or environment variables for API credentials.

## 📌 API Requirements

| Service | Environment Variable | Purpose |
|---|---|---|
| OpenRouter | `OPENROUTER_API_KEY` | AI evaluation |
| Groq | `GROQ_API_KEY` | Speech-to-Text |

The current dashboard UI also references **Gemini AI** and **Whisper STT** as platform capabilities.

## 🧪 Development

Check Python syntax before pushing:

```bash
python3 -m py_compile app.py
```

Run locally:

```bash
streamlit run app.py
```

## 📄 License

Add your preferred license, for example:

```text
MIT License
```

If the project is proprietary, replace this section with your appropriate licensing statement.

AI-powered English learning and evaluation project built with Streamlit.

---

⭐ If you find this project useful, consider giving the repository a star.
