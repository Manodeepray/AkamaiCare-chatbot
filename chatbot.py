#combined
import os


from llama_index.llms.gemini import Gemini

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Document
from llama_index.core.tools.types import ToolMetadata

        
from PyPDF2 import PdfReader


from llama_index.core import PromptTemplate
from sklearn.impute import SimpleImputer

from llama_index.core.tools import QueryEngineTool

from llama_index.core.tools.types import ToolMetadata

import pandas as pd
import logging
import sys

import pandas as pd
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine

from llama_index.core.selectors.llm_selectors import     LLMSingleSelector
   




GOOGLE_API_KEY = "AIzaSyAQKESf1NzOewpZ8InR9emIxMyG8VF9bzs"  # add your GOOGLE API key here
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


llm = Gemini(
    model="models/gemini-1.5-flash",
    # api_key="some key",  # uses GOOGLE_API_KEY env var by default
)





class CSVQueryTool():
    def __init__(self, csv_file_path, name , description):
        self.dataframe = pd.read_csv(csv_file_path )
        self.name = name 
        self.description = description
        self.metadata = ToolMetadata(name= self.name, description=self.description)

        # Initialize the imputer to replace NaN with the column mean
                
        # Separate numeric and non-numeric columns
        numeric_columns = self.dataframe.select_dtypes(include=["number"]).columns
        non_numeric_columns = self.dataframe.select_dtypes(exclude=["number"]).columns

        # Impute numeric columns with the mean
        numeric_imputer = SimpleImputer(strategy="mean")
        self.dataframe[numeric_columns] = numeric_imputer.fit_transform(self.dataframe[numeric_columns])

        # Handle non-numeric columns (e.g., fill with the most frequent value or a placeholder)
        non_numeric_imputer = SimpleImputer(strategy="most_frequent")
        self.dataframe[non_numeric_columns] = non_numeric_imputer.fit_transform(self.dataframe[non_numeric_columns])

        
        self.query_engine = PandasQueryEngine(df=self.dataframe, verbose=True , llm=llm)
        self.response = None
        self.instruction_str = """\
            1. Convert the query to executable Python code using Pandas.
            2. The final line of code should be a Python expression that can be called with the `eval()` function.
            3. The code should represent a solution to the query.
            4. PRINT ONLY THE EXPRESSION.
            5. Do not quote the expression.
            """
        self.new_prompt = PromptTemplate("""\
                      You are working with a pandas dataframe in Python.
                      The name of the dataframe is `df`.
                      This is the result of `print(df.head())`:
                      {df_str}

                      Follow these instructions:
                      {instruction_str}
                      Query: {query_str}

                      Expression: """
                      ).partial_format(instruction_str=self.instruction_str)

        self.query_engine.update_prompts({"pandas_prompt":self.new_prompt}) 

        self.tool = QueryEngineTool.from_defaults(
              self.query_engine, name=str(self.name), description=str(self.description)
          )


    def query(self, prompt):
        self.response = self.query_engine.query(prompt)
        self.response = str(self.response)
        return self.response

    def return_tool(self):
      return self.tool




class PDFRetrievalTool():
    def __init__(self, pdf_file_path , name , description):
        self.model_name = "models/embedding-001"
        self.name = name 
        self. description = description
        self.metadata = ToolMetadata(name= self.name, description=self.description)
        # load documents
        print(os.path.exists(pdf_file_path))
        self.documents = None
        self.text = None

        if self.documents == None:
          try:
            reader = PdfReader(pdf_file_path)
            self.text = [page.extract_text() for page in reader.pages] 
          except Exception as e:
            print(f"Error loading document: {e}")
        if self.text != None:
         self.documents = [Document(text=t) for t in self.text]

        self.splitter = SentenceSplitter(chunk_size=1024)
        self.nodes = self.splitter.get_nodes_from_documents(self.documents)

        #embeddings


        self.embed_model = GeminiEmbedding(
            model_name=self.model_name, api_key=GOOGLE_API_KEY, title="this is a document"
        )


        self.vector_index = VectorStoreIndex(self.nodes , embed_model=self.embed_model)

        self.query_engine = self.vector_index.as_query_engine(similarity_top_k=2 , llm = llm)
        self.tool = QueryEngineTool.from_defaults(
              self.query_engine, name=str(self.name), description=str(self.description)
          )
        self.response = None


    def retrieve(self, query):
        # Simple keyword-based search
        self.response = self.query_engine.query(query)
        return self.response

    def tool(self):
      return self.tool




def create_tools():
    Claims_Enrollment_truncated_csv_tool = CSVQueryTool("./Claims_Enrollment_truncated.csv" , name = "Claims_Enrollment", description = "patient enrollment csv claim ")
    Claims_Member_truncated_csv_tool = CSVQueryTool("./Claims_Member_truncated.csv" , name = "Claims_Member" , description = "patient members csv relation")
    Claims_Provider_truncated_csv_tool = CSVQueryTool("./Claims_Provider_truncated.csv" , name = "Claims_Provider", description = "providers and supplier ")
    #Claims_Services_truncated_csv_tool = CSVQueryTool("./content/Claims_Services_truncated.csv" , name = "Claims_Service" , description = "")

    pdf_engine = PDFRetrievalTool("./pcna2007databook.pdf" ,name = "pdf retrieval tool " , description = "for hawaian medical facilities" ) 

    initial_tools=[Claims_Enrollment_truncated_csv_tool,Claims_Member_truncated_csv_tool,Claims_Provider_truncated_csv_tool, pdf_engine]

    return initial_tools
class combined_agent():
#initial_tools=[csv_tool1,csv_tool2,csv_tool3, pdf_tool]
  def __init__(self , initial_tools):


      # Define the router
      self.selector = LLMSingleSelector.from_defaults(llm=llm)
      self.router_query_engine = RouterQueryEngine(
          selector=self.selector,
          
              query_engine_tools=initial_tools,
              llm=llm
          )
    
  def query(self,query):
    self.response = self.router_query_engine.query(query)
    return self.response.response


initial_tools = create_tools()


    
combined_agent_tool = combined_agent(initial_tools)






def chatbot_run(query):
    context = combined_agent_tool.query(query)
    prompt_template = PromptTemplate("""
    You are a helpful and empathetic medical assistant working in a hospital. 
    Your job is to assist staff and hospital admin whos has complete acces to the data in context. help with medical queries, provide 
    accurate information of patients, and guide them responsibly. 
    Always maintain a professional and caring tone.

    Here are some guidelines to follow:
    - If the query involves specific symptoms, suggest consulting a doctor for proper diagnosis.
    - If the query relates to medical terms, conditions, or medications, explain them in simple terms.
    - If the query relates to patients details, conditions, or medications, explain them in simple terms.
    - If unsure about a response, advise consulting a healthcare provider.
    - Always prioritize safety and professionalism.


    Query: {query}

    context " {context}

    Provide a detailed, empathetic, and professional response to the above query.
    """)
  
    prompt = prompt_template.format(query=query , context=context  )

    answer = llm.complete(prompt)


    return answer


answer = chatbot_run("tell me about patient in csv 1  2C85F5450905C91DC78DB09DE")


