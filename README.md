# LangChain Tutorial Notebooks

Hands-on Jupyter notebooks for learning LangChain fundamentals, prompt engineering, multi-model workflows, chat memory, and structured output parsing.

## What is in this repo

- `00_lesson_2.ipynb`: Google Gemini API basics and generation parameters (`temperature`, `top_p`)
- `01_lesson_3.ipynb`: Prompt engineering patterns (role-playing, few-shot, chain-of-thought)
- `02_lesson_4.ipynb`: Multi-provider usage with LangChain (Google, OpenAI, Anthropic, Ollama)
- `03_lesson_5.ipynb`: Chat prompt templates and conversation memory with LangChain
- `04_lesson_6.ipynb`: Prompt templates and output parsers (list, structured, Pydantic)

## Requirements

Dependencies are listed in `requirements.txt` and include:

- `langchain`, `langchain-core`, `langchain-classic`, `langchain_community`
- `google-generativeai`, `langchain_google_genai`
- `langchain_openai`, `langchain_anthropic`
- `langchain-ollama`
- `python-dotenv`

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies.
3. Configure API keys.
4. Launch Jupyter and run notebooks in order.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install jupyter
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install jupyter
```

Start Jupyter:

```bash
jupyter notebook
```

Then open and run notebooks in this sequence:

1. `00_lesson_2.ipynb`
2. `01_lesson_3.ipynb`
3. `02_lesson_4.ipynb`
4. `03_lesson_5.ipynb`
5. `04_lesson_6.ipynb`

## Environment variables

Create a `.env` file in the project root (or export variables in your shell):

```env
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

Notes:

- You only need keys for the providers used in a given notebook cell.
- `python-dotenv` is included so notebooks can load values from `.env`.

## Optional: Run open-source models locally with Ollama

If you want to run local models used in some examples:

1. Install Ollama from the official website.
2. Pull a model (example):

```bash
ollama pull gemma:2b
```

3. Start the Ollama service:

```bash
ollama serve
```

LangChain typically connects to Ollama at `http://localhost:11434`.

## Learning path

- Start with model basics and parameters
- Move to prompt engineering techniques
- Compare providers with a unified LangChain interface
- Add memory for multi-turn conversations
- Finish with structured outputs and parsers

## Troubleshooting

- If imports fail, verify your active virtual environment and reinstall `requirements.txt`.
- If API calls fail, confirm your environment variables are loaded in the current kernel/session.
- If Ollama requests fail, make sure `ollama serve` is running.

## License

No license file is included in this repository yet.
