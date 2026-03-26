from google import genai
from google.genai import types
import json

# Initialize client
client = genai.Client(api_key="")
config = types.GenerateContentConfig(
    temperature=0.7,    # Lower (0.1-0.5) for facts/code; Higher (0.8-1.5) for creativity
    top_k=50,          # Limits to top K tokens, can reduce randomness
)
# =========================
# ADVANCED PROMPT TEMPLATE
# =========================
SYSTEM_PROMPT = """
You are an expert AI tutor specializing in explaining complex topics to students.

Your teaching style:
- Step-by-step explanation
- Use analogies
- Keep clarity over jargon
- Adapt for beginners

You MUST follow output format strictly.
"""

CONTEXT_BLOCK = """
Definitions:
- Token: smallest unit of text processed by LLM
- Logits: raw scores before probability
- Transformer: neural architecture used in LLMs

Constraints:
- Keep explanation under 200 words
- Must include 1 real-world analogy
- Must include 1 example
"""

FEW_SHOT_EXAMPLES = """
Example 1:
Question: What is a token?
Answer:
{
  "concept": "Token",
  "explanation": "A token is a small piece of text...",
  "analogy": "Like breaking a sentence into Lego blocks",
  "example": "Hello world -> [Hello, world]"
}

Example 2:
Question: What is a neural network?
Answer:
{
  "concept": "Neural Network",
  "explanation": "A system of layers...",
  "analogy": "Like interconnected roads",
  "example": "Image classification system"
}
"""

USER_QUERY = "Explain how AI works"

# =========================
# MULTI-STAGE PROMPTING
# =========================

def generate_answer():
    prompt = f"""
{SYSTEM_PROMPT}

{CONTEXT_BLOCK}

{FEW_SHOT_EXAMPLES}

Task:
Answer the following question in structured JSON.

Question: {USER_QUERY}

Output format:
{{
  "concept": "...",
  "explanation": "...",
  "analogy": "...",
  "example": "..."
}}
"""
    
    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=prompt,
        config=config
    )
    
    return response.text


def self_reflect(answer):
    reflection_prompt = f"""
You are a strict reviewer.

Evaluate the following answer:
{answer}

Check:
- Is it correct?
- Is it simple for beginners?
- Does it follow all constraints?

Return JSON:
{{
  "score": 1-10,
  "issues": ["..."],
  "improved_answer": "..."
}}
"""
    
    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=reflection_prompt,
        config=config
    )
    
    return response.text


# =========================
# PIPELINE EXECUTION
# =========================

if __name__ == "__main__":
    print("=== Generating Answer ===")
    answer = generate_answer()
    print(answer)

    print("\n=== Self Reflection ===")
    review = self_reflect(answer)
    print(review)