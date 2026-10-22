import requests
import streamlit as st
from ddgs import DDGS

from models import ResearchReport

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "granite4.1:3b"
REQUEST_TIMEOUT_S = 300


class SearchError(RuntimeError):
    """Raised when the web search fails or returns nothing."""


def search_web(query: str, max_results: int = 3) -> str:
    """Fetch search results using DuckDuckGo (via the `ddgs` package)."""
    try:
        results = DDGS().text(query, max_results=max_results)
    except Exception as e:
        raise SearchError(f"Web search failed: {e}") from e
    if not results:
        raise SearchError("Web search returned no results.")
    return "\n".join(f"- {r.get('title', '')}: {r.get('body', '')}" for r in results)


def build_prompt(topic: str, context: str) -> str:
    return f"""
    You are an expert AI researcher. I will provide a topic and some web search context.
    Analyze the context and write a report.

    Topic: {topic}
    Web Context: {context}

    Respond with a JSON object containing "title", "executive_summary",
    "key_findings" (3 to 5 short strings) and "conclusion".
    """


def generate_report(topic: str, context: str) -> ResearchReport:
    """Generate a report from Ollama, constrained to the ResearchReport JSON schema."""
    payload = {
        "model": MODEL_NAME,
        "prompt": build_prompt(topic, context),
        "stream": False,
        # Structured outputs: Ollama constrains generation to this JSON schema.
        "format": ResearchReport.model_json_schema(),
        "options": {"temperature": 0.2},
    }

    response = requests.post(OLLAMA_API_URL, json=payload, timeout=REQUEST_TIMEOUT_S)
    response.raise_for_status()
    raw_json = response.json().get("response", "{}")

    # Pydantic V2 still validates the result (lengths, cleanup) after generation.
    return ResearchReport.model_validate_json(raw_json)


def format_markdown(report: ResearchReport) -> str:
    """Format the Pydantic model into a Markdown string."""
    md = f"# {report.title}\n\n"
    md += f"## Executive Summary\n{report.executive_summary}\n\n"
    md += "## Key Findings\n"
    for finding in report.key_findings:
        md += f"- {finding}\n"
    md += f"\n## Conclusion\n{report.conclusion}\n"
    return md


def main() -> None:
    st.set_page_config(page_title="AI Agentic Researcher", page_icon="🔍", layout="centered")
    st.title("🔍 Pydantic V2 Agentic Researcher")
    st.markdown(f"**Powered by `{MODEL_NAME}`, Pydantic V2, and DuckDuckGo**")

    topic = st.text_input("Enter a research topic (e.g., 'Latest Quantum Computing breakthroughs')")

    if not st.button("Generate Report"):
        return
    if not topic.strip():
        st.warning("Please enter a topic.")
        return

    with st.spinner("1. Searching the web..."):
        try:
            context = search_web(topic)
        except SearchError as e:
            st.error(str(e))
            return

    with st.spinner(f"2. Synthesizing data with {MODEL_NAME}..."):
        try:
            report = generate_report(topic, context)
        except Exception as e:
            st.error(f"Failed to generate valid report: {e}")
            return

    md_content = format_markdown(report)
    st.success("Report Generated and Validated via Pydantic!")
    st.markdown("---")
    st.markdown(md_content)
    st.markdown("---")
    st.download_button(
        label="📥 Download Report",
        data=md_content,
        file_name="output.md",
        mime="text/markdown",
    )


if __name__ == "__main__":
    # `streamlit run app.py` executes this file as __main__.
    main()
