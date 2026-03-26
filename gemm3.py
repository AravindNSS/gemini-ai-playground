# pip install google-genai 
from google import genai
import json
import os

# =========================
# CONFIG
# =========================
API_KEY = ""
MODEL = "gemma-3-27b-it"

client = genai.Client(api_key=API_KEY)

# =========================
# MEMORY (Simple)
# =========================

MEMORY = [
    "User is a beginner student",
    "User prefers simple explanations"
]

# =========================
# KNOWLEDGE BASE (RAG-lite)
# =========================

KNOWLEDGE_DB = {
    "ai": "AI is the ability of machines to mimic human intelligence.",
    "ml": "Machine learning is a subset of AI that learns from data.",
    "dl": "Deep learning uses neural networks with many layers."
}

# =========================
# STEP 1: RETRIEVE CONTEXT
# =========================

def retrieve_knowledge(query):
    query_lower = query.lower()
    for key in KNOWLEDGE_DB:
        if f" {key} " in f" {query_lower} " or query_lower.startswith(key) or query_lower.endswith(key):
            return KNOWLEDGE_DB[key]
    return "General AI knowledge"

# =========================
# STEP 2: COMPRESS CONTEXT
# =========================

def compress_context(text):
    """
    Keep it simple: trim long text
    """
    return text[:150]

# =========================
# STEP 3: BUILD CONTEXT
# =========================

def build_context(query):
    print("\n--- QUERY ---\n", query)
    knowledge = retrieve_knowledge(query)
    print("\n--- RETRIEVED KNOWLEDGE ---\n", knowledge)
    compressed_knowledge = compress_context(knowledge)

    context = {
        "system": "You are a helpful AI tutor",
        
        "user": {
            "level": "beginner",
            "preference": "simple explanation"
        },

        "memory": MEMORY,

        "knowledge": compressed_knowledge,

        "task": {
            "instruction": "Explain clearly",
            "requirements": [
                "step-by-step",
                "simple words",
                "example"
            ]
        },

        "query": query
    }

    return context

# =========================
# STEP 4: CONTEXT → PROMPT
# =========================

def context_to_prompt(ctx):
    return f"""
### SYSTEM
{ctx['system']}

### USER
Level: {ctx['user']['level']}
Preference: {ctx['user']['preference']}

### MEMORY
{ctx['memory']}

### KNOWLEDGE
{ctx['knowledge']}

### TASK
{ctx['task']['instruction']}
Requirements: {ctx['task']['requirements']}

### QUESTION
{ctx['query']}

### OUTPUT (JSON ONLY)
{{
  "concept": "",
  "steps": [],
  "example": ""
}}
"""

# =========================
# STEP 5: EXECUTE
# =========================

def run(query):

    # Build context
    ctx = build_context(query)
    print("\n--- CONTEXT ---\n", json.dumps(ctx, indent=2))

    # Convert to prompt
    prompt = context_to_prompt(ctx)

    # Call model
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    print("\n--- RAW OUTPUT ---\n", response.text)

# =========================
# RUN
# =========================

if __name__ == "__main__":
    run("Explain how ml works")