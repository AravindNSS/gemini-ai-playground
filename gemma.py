from google import genai

client = genai.Client(api_key="")

response = client.models.generate_content(
    model="gemma-3-27b-it",
    contents="Roses are red, answer in short",
)

print(response.text)