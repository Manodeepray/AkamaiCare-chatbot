import chatbot
from llama_index.core import PromptTemplate

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import os

# Initialize FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with a specific origin if needed, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize tools and agent
initial_tools = chatbot.create_tools()
combined_agent_tool = chatbot.combined_agent(initial_tools)
llm = chatbot.llm

# Define the FastAPI endpoint for GET requests
@app.get("/chatbot/")
async def chatbot_endpoint(query: str):
    """
    Endpoint to handle chatbot queries using GET request.
    """
    try:
        # Run the query through the chatbot
        context = combined_agent_tool.query(query)
        
        # Define the prompt template
        prompt_template = PromptTemplate("""
        You are a helpful and empathetic medical assistant working in a hospital. 
        Your job is to assist staff and hospital admin who have complete access to the data in context. Help with medical queries, provide 
        accurate information of patients, and guide them responsibly. 
        Always maintain a professional and caring tone.

        Here are some guidelines to follow:
        - If the query involves specific symptoms, suggest consulting a doctor for proper diagnosis.
        - If the query relates to medical terms, conditions, or medications, explain them in simple terms.
        - If the query relates to patients details, conditions, or medications, explain them in simple terms.
        - If unsure about a response, advise consulting a healthcare provider.
        - Always prioritize safety and professionalism.

        Query: {query}

        Context: "{context}"

        Provide a detailed, empathetic, and professional response to the above query.
        """)

        # Format the prompt
        prompt = prompt_template.format(query=query, context=context)

        # Generate the answer using the LLM
        answer = llm.complete(prompt)

        # Return the response
        return {"query": query, "response": answer}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the AkamaiCare API"}
