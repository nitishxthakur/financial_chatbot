import pdfplumber

with pdfplumber.open("Sample Financial Statement.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)

{
    "Revenue": {"Q1": 100000, "Q2": 120000},
    "Expenses": {"Q1": 80000, "Q2": 90000},
    "Net Profit": {"Q1": 20000, "Q2": 30000}
}

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(["What is the net profit for Q1?", "Revenue details for Q2"])

from pinecone import Pinecone

# Initialize Pinecone with your API key
pc = Pinecone(api_key="pcsk_3WjYhn_AQLcXLeh4cnQH4w3tG6qhiWGu9y6YzHD8Dmvh2L1rb2a9HXoWu47nEXc1yK6Wn4")

# List all indexes
index_names = pc.list_indexes().names()
print("Available Indexes:", index_names)

import os
from pinecone import Pinecone

# Initialize Pinecone with your API key
pc = Pinecone(api_key="pcsk_3WjYhn_AQLcXLeh4cnQH4w3tG6qhiWGu9y6YzHD8Dmvh2L1rb2a9HXoWu47nEXc1yK6Wn4")

# Specify the index name
index_name = "financial-data-new"

# Get the index configuration
index_config = pc.describe_index(index_name)

# Print the dimension of the index
print(f"Index Name: {index_config['name']}")
print(f"Dimension: {index_config['dimension']}")

import os
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone with your API key
pc = Pinecone(api_key="pcsk_3WjYhn_AQLcXLeh4cnQH4w3tG6qhiWGu9y6YzHD8Dmvh2L1rb2a9HXoWu47nEXc1yK6Wn4")

# Connect to the existing index
index_name = "financial-data-new"
index = pc.Index(index_name)

# Prepare 768-dimensional embeddings (example data)
embeddings = [
    [0.2172567993402481] * 768,  # Example embedding for doc1 (768 dimensions)
    [0.3000063211917877] * 768   # Example embedding for doc2 (768 dimensions)
]

# Upsert embeddings with error handling
try:
    vectors_to_upsert = [
        ("doc1", embeddings[0]),
        ("doc2", embeddings[1])
    ]

    index.upsert(vectors=vectors_to_upsert)
    print("Upsert successful!")
except Exception as e:
    print(f"Error during upsert: {str(e)}")

# Example of querying (ensure to provide only vector or ID)
query_vector = [0.2172567993402481] * 768  # Replace with your actual query vector

try:
    results = index.query(vector=query_vector, top_k=5)  # Retrieve top 5 similar vectors
    print("Query results:")
    for match in results['matches']:
        print(f"ID: {match['id']}, Score: {match['score']}")
except Exception as e:
    print(f"Error during query: {str(e)}")

import streamlit as st
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Initialize Pinecone with your API key
pc = Pinecone(api_key="pcsk_3WjYhn_AQLcXLeh4cnQH4w3tG6qhiWGu9y6YzHD8Dmvh2L1rb2a9HXoWu47nEXc1yK6Wn4")  # Replace with your actual API key

# Connect to the existing index
index_name = "financial-data-new"
index = pc.Index(index_name)

# Load your embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # Ensure this matches your index

# Streamlit app title
st.title("Financial Data Query Bot")

# User input for query with a unique key
user_query = st.text_input("Enter your query:", key="user_query_input")

# Unique key for the submit button
if st.button("Submit", key="submit_button"):
    if user_query:
        # Generate an embedding from user input
        query_vector = model.encode(user_query).tolist()  # Convert to list if necessary

        try:
            # Query the index using the generated embedding
            results = index.query(vector=query_vector, top_k=5)  # Retrieve top 5 similar vectors

            # Display results
            st.write("Query results:")
            for match in results['matches']:
                st.write(f"ID: {match['id']}, Score: {match['score']}")
        except Exception as e:
            st.write(f"Error during query: {str(e)}")
    else:
        st.write("Please enter a query.")

# Display results with more context
if results['matches']:
    st.write("Query results:")
    for match in results['matches']:
        st.write(f"**ID:** {match['id']}")
        st.write(f"**Score:** {match['score']}")
        # If you have additional metadata, display it here
        # For example: st.write(f"**Content:** {match['metadata']['text']}")
else:
    st.write("No matches found.")

import streamlit as st
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Initialize Pinecone with your API key
pc = Pinecone(api_key="pcsk_3WjYhn_AQLcXLeh4cnQH4w3tG6qhiWGu9y6YzHD8Dmvh2L1rb2a9HXoWu47nEXc1yK6Wn4")

# Connect to the existing index
index_name = "financial-data-new"
index = pc.Index(index_name)

# Load your embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Streamlit app title (only once)
st.title("Financial Data Query Bot")

# User input for query with a unique key
user_query = st.text_input("Enter your query:", key="user_query_input")

# Unique key for the submit button
if st.button("Submit", key="submit_button"):
    if user_query:
        # Generate an embedding from user input
        query_vector = model.encode(user_query).tolist()  # Convert to list if necessary

        try:
            # Query the index using the generated embedding
            results = index.query(vector=query_vector, top_k=5)  # Retrieve top 5 similar vectors

            # Display results
            st.write("Query results:")
            for match in results['matches']:
                st.write(f"ID: {match['id']}, Score: {match['score']}")
        except Exception as e:
            st.write(f"Error during query: {str(e)}")
    else:
        st.write("Please enter a query.")

@st.cache_data
def generate_embedding(query):
    return model.encode(query).tolist()

if st.button("Submit"):
    if user_query:
        # Generate an embedding from user input with caching
        query_vector = generate_embedding(user_query)

        try:
            # Query the index using the generated embedding
            results = index.query(vector=query_vector, top_k=5)  # Retrieve top 5 similar vectors

            # Display results with more context
            if results['matches']:
                st.write("Query results:")
                for match in results['matches']:
                    st.write(f"**ID:** {match['id']}")
                    st.write(f"**Score:** {match['score']}")
                    if 'metadata' in match:
                        st.write(f"**Content:** {match['metadata'].get('text', 'No content available')}")
            else:
                st.write("No matches found.")

        except Exception as e:
            st.write(f"Error during query: {str(e)}")
    else:
        st.write("Please enter a query.")

if st.button("Clear"):
    user_query = ""  # Reset the user query input
    st.session_state.results = None  # Clear previous results

if results['matches']:
    st.write("Query results:")
    for match in results['matches']:
        st.write(f"**ID:** {match['id']}")
        st.write(f"**Score:** {match['score']}")
        if 'metadata' in match:
            metadata = match['metadata']
            st.write(f"**Content:** {metadata.get('text', 'No content available')}")
            st.write(f"**Date:** {metadata.get('date', 'No date available')}")
            st.write(f"**Category:** {metadata.get('category', 'No category available')}")

if st.checkbox("Show Help"):
    st.subheader("How to Use This App")
    st.write("""
    - Enter your financial query in the text box.
    - Click "Submit" to see the most relevant documents.
    - Use the "Clear" button to reset your input and results.
    """)
