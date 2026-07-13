import streamlit as st
import requests
import json
from duckduckgo_search import DDGS
from models import ResearchReport

# Configure Streamlit
st.set_page_config(page_title="AI Agentic Researcher", page_icon="🔍", layout="centered")

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "granite4.1:3b"

def search_web(query: str) -> str:
    """Fetch search results using DuckDuckGo."""
    try:
        results = DDGS().text(query, max_results=3)
        context = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
        return context
    except Exception as e:
        return f"Error fetching web results: {e}"

def generate_report(topic: str, context: str) -> ResearchReport:
    """Generate structured JSON from Ollama using Pydantic V2 schema."""
    schema = ResearchReport.model_json_schema()
    
    prompt = f"""
    You are an expert AI researcher. I will provide a topic and some web search context.
    Analyze the context and write a report.
    
    Topic: {topic}
    Web Context: {context}
    
    You MUST output valid JSON only. Your JSON object must contain exactly the following keys:
    "title" (string), "executive_summary" (string), "key_findings" (list of strings), and "conclusion" (string).
    
    OUTPUT ONLY THE JSON OBJECT. Do not output the schema. Do not output any markdown formatting or extra text.
    """
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2
        }
    }
    
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    raw_json = response.json().get("response", "{}")
    
    # Use Pydantic V2 to validate and parse the JSON string
    report = ResearchReport.model_validate_json(raw_json)
    return report

def format_markdown(report: ResearchReport) -> str:
    """Format the Pydantic model into a Markdown string."""
    md = f"# {report.title}\n\n"
    md += f"## Executive Summary\n{report.executive_summary}\n\n"
    md += "## Key Findings\n"
    for finding in report.key_findings:
        md += f"- {finding}\n"
    md += f"\n## Conclusion\n{report.conclusion}\n"
    return md

st.title("🔍 Pydantic V2 Agentic Researcher")
st.markdown(f"**Powered by `{MODEL_NAME}`, Pydantic V2, and DuckDuckGo**")

topic = st.text_input("Enter a research topic (e.g., 'Latest Quantum Computing breakthroughs')")

if st.button("Generate Report"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        with st.spinner("1. Searching the web..."):
            context = search_web(topic)
            
        with st.spinner(f"2. Synthesizing data with {MODEL_NAME}..."):
            try:
                report = generate_report(topic, context)
                md_content = format_markdown(report)
                
                # Save to disk as per buildai rules
                with open("output.md", "w", encoding="utf-8") as f:
                    f.write(md_content)
                    
                st.success("Report Generated and Validated via Pydantic!")
                
                st.markdown("---")
                st.markdown(md_content)
                st.markdown("---")
                
                st.download_button(
                    label="📥 Download Report",
                    data=md_content,
                    file_name="output.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Failed to generate valid report: {e}")
