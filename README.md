# AkamaiCare-chatbot

## lokahi hackathon solution

Running the FastAPI Server
Run the FastAPI Server: To run the FastAPI app, execute the following command from your project directory:

'''bash

uvicorn endpoint:app --reload
'''
API Documentation:

> Once the server is running, you can access the API documentation by visiting: http://127.0.0.1:8000/docs.
> Test the API: You can now test your chatbot API by sending a POST request to http://127.0.0.1:8000/chatbot with a JSON body:

'''json
{
"query": "Tell me about patient 2C85F5450905C91DC78DB09DE"
}
'''
