<div align="center">
  <a href="https://youtu.be/9q2SS8ixnT4">
    <img src="https://img.youtube.com/vi/9q2SS8ixnT4/0.jpg" alt="Pydantic V2 Tutorial: 50x Faster AI Validation Pipelines">
  </a>
  <h3>📺 <a href="https://youtu.be/9q2SS8ixnT4">Watch the full tutorial on YouTube</a></h3>
  <h1>🔍 Pydantic V2 Agentic Researcher Workflow</h1>
  <p><i>A powerful, minimal AI researcher leveraging strict Pydantic V2 typing, DuckDuckGo Search, and Local Ollama Models.</i></p>
</div>

---

## ⚡ Overview

This project demonstrates the sheer power of **Pydantic V2** combined with an agentic web search workflow. By enforcing strict JSON schemas on the local `granite4.1:3b` model, we guarantee that the synthesized research reports are robust, perfectly structured, and ready to be downloaded via a stunning Streamlit UI.

## 🛠️ Tech Stack
- **Pydantic V2**: Strict schema definition, validation, and JSON generation.
- **Streamlit**: Beautiful, rapid web interface.
- **Ollama**: Local AI inference using `granite4.1:3b` (zero-cost, fast).
- **DuckDuckGo Search**: Real-time web context gathering.

### 📁 File Explanations
- `app.py`: The main Streamlit web application. It handles the UI, invokes DuckDuckGo for web searches, formats the prompt for Ollama, and displays the final Markdown report.
- `models.py`: Contains the `ResearchReport` Pydantic V2 schema. It enforces strict type validation and utilizes `@field_validator` to automatically clean up the LLM's text output.
- `requirements.txt`: Python package dependencies.
- `output.md` / `ideal_outputs.md`: Sample generated markdown reports produced by the tool.

---

## 🚀 Installation & Setup

Copy and paste these commands into your Windows AntiGravity PowerShell:

### 1. Start Ollama & Download Model
Ensure you have Ollama installed on your system. Run the following command to download the model and ensure the server is running:
```powershell
ollama run granite4.1:3b
```
*(You can exit the interactive prompt once it downloads by typing `/bye`. Ollama will continue running in the background).*

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Run the Application
```powershell
streamlit run app.py
```

---

## 🧪 Testing

To quickly test the Pydantic generation pipeline without the UI:
```powershell
python -c "from app import generate_report; print(generate_report('AI Agents', 'AI Agents are autonomous entities.').model_dump_json(indent=2))"
```

---

## 🎯 5 Use Cases

1. **Automated Market Research**: Instantly generate well-structured reports on competitors by typing their names.
2. **Academic Synthesis**: Summarize the latest breakthroughs on highly specific topics in seconds.
3. **News Aggregation**: Get the top 3 key findings of current world events strongly validated by Pydantic.
4. **Offline-First AI Tools**: Completely local analysis (aside from the search ping) ensuring zero data leakage to cloud LLM providers.
5. **Data Pipeline Prototyping**: Serve as a visual frontend before adapting the robust `models.py` for a backend production pipeline.

---

## 🔮 5 Future Features

1. **Multi-Step Agents**: Add a planning step where the LLM decides *what* to search before searching.
2. **Dynamic Model Switching**: A sidebar dropdown to switch between installed Ollama models dynamically.
3. **PDF Export**: Convert the generated markdown into a beautiful PDF file alongside the Markdown download.
4. **Pydantic TypeAdapter**: Implement `TypeAdapter` for batch validation of multiple concurrent research reports.
5. **Streaming Responses**: Stream the generated report chunks directly into the UI for a faster perceived experience.

---

## 📚 Resources & Blogs

- [**Pydantic V2 Get Started**](https://pydantic.dev/docs/validation/latest/get-started/): Official documentation to jump right into Pydantic V2 core concepts.
- [**Migration Code Transformation Tool**](https://pydantic.dev/docs/validation/latest/get-started/migration#code-transformation-tool): A helpful guide and tool (`bump-pydantic`) for migrating your Pydantic V1 code to V2 seamlessly.
- [**Pydantic V2 Article**](https://pydantic.dev/articles/pydantic-v2): An in-depth article discussing the vision, performance enhancements, and architectural shifts in Pydantic V2.

---

### Keywords
Pydantic V2, AI Agents, Local Ollama, Granite Model, Streamlit UI, DuckDuckGo Search, Python, AI Workflow.
