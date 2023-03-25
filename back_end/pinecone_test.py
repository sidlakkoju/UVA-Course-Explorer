# from ChatGPT, need to modify significantly


import openai
import pandas as pd
import pinecone
from pinecone import QueryIndex

# Set up OpenAI API key
openai.api_key = "your_openai_api_key"

# Set up Pinecone API key
pinecone.deinit()  # Deinitialize Pinecone if already initialized
pinecone.init(api_key="your_pinecone_api_key")

# Load your DataFrame
# df = pd.read_csv("your_data.csv")

# Replace the DataFrame below with your actual DataFrame
data = {
    "acad_org": ["AO1", "AO2"],
    "catalog_nbr": ["CN1", "CN2"],
    "class_nbr": ["CNBR1", "CNBR2"],
    "subject": ["S1", "S2"],
    "subject_descr": ["SD1", "SD2"],
    "descr": ["D1", "D2"],
    "units": [4, 3],
    "description": [
        "This is the first course description.",
        "This is the second course description.",
    ],
}

df = pd.DataFrame(data)

# Create embeddings using OpenAI API
def create_embeddings(texts):
    model_engine = "text-davinci-002"
    embeddings = []

    for text in texts:
        prompt = f"Create an embedding for the following text: {text}"
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=30,
            n=1,
            stop=None,
            temperature=0.5,
        )

        embedding = response.choices[0].text.strip().split()
        embedding = [float(value) for value in embedding]
        embeddings.append(embedding)

    return embeddings

descriptions = df["description"].tolist()
embeddings = create_embeddings(descriptions)

# Create a Pinecone index
index_name = "course-embeddings"
pinecone.deinit()  # Deinitialize Pinecone if already initialized
pinecone.init(api_key="your_pinecone_api_key")
pinecone.create_index(index_name=index_name, metric="cosine", shards=1)

# Write embeddings to Pinecone index
pinecone_index = pinecone.Index(index_name=index_name, index_type=QueryIndex)

for class_nbr, embedding in zip(df["class_nbr"], embeddings):
    pinecone_index.upsert(upserts={class_nbr: embedding})

# Perform similarity search
def similarity_search(query, top_k=5):
    query_embedding = create_embeddings([query])[0]
    results = pinecone_index.fetch(ids=None, queries=[query_embedding], top_k=top_k)
    course_ids = results[0]

    # Get the course information
    course_info = df[df["class_nbr"].isin(course_ids)].to_dict(orient="records")

    return course_info

# Example search
query = "Find me courses similar to: Introduction to AI"
results = similarity_search(query)
print(results)

# Clean up
pinecone.deinit()  # Deinitialize Pinecone
pinecone.deinit(index_name)  # Delete the Pinecone index