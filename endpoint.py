
import chatbot






from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os

# Your existing imports and class definitions go here...

# Initialize FastAPI
app = FastAPI()

# Define a query model for input
class QueryRequest(BaseModel):
    query: str

# Initialize tools and agent
initial_tools = chatbot.create_tools()
combined_agent_tool = chatbot.combined_agent(initial_tools)
llm = chatbot.llm
# Define the FastAPI endpoint
@app.post("/chatbot/")
async def chatbot_endpoint(request: QueryRequest):
    try:
        # Get the query
        query = request.query

        # Run the query through the chatbot
        context = combined_agent_tool.query(query)
        
        # Define the prompt template
        prompt_template = prompt_template("""
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
