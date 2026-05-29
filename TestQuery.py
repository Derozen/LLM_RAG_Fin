import os
from dotenv import load_dotenv
import psycopg2
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
from sentence_transformers import SentenceTransformer

query = "Will Federal Fund rate decrease after FOMC meeting in the following 3 months?"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")

embed = model.encode(query).tolist()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

cur.execute("""
SELECT
    content,
    embedding <=> %s::vector AS distance
FROM documents
ORDER BY distance
DESC LIMIT 5;
""", (embed,))

results = cur.fetchall()

for row in results:
    print(row)
    
context = "\n".join([r[0] for r in results])
prompt = f"""
According to the following information：

Context:
{context}

Question:
{query}
"""

from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2
)

answer = response.choices[0].message.content

print(answer)
with open("answe.txt", "w") as f:
    f.write(answer)

