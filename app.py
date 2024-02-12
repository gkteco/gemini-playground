import sys
import os
from dotenv import load_dotenv
load_dotenv()

import vertexai
from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)

# tool dependencies
from function_def import (
    get_stock_price,
    list_files_in_drive
)
from function_decl import function_declarations

# Set up the Vertex AI client
vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("LOCATION"))

# Tool object to pass to GenerativeModel
tools = Tool(
    function_declarations = function_declarations
)

#gemini configuration
generation_config = GenerationConfig(
    temperature=0.5,
    top_p=0.9,
    top_k=40,
    candidate_count=100,
    max_output_tokens=8192
)

# Create a GenerativeModel object
model = GenerativeModel("gemini-pro",
                        tools=[tools])
#start chat
chat = model.start_chat()
prompt = "list my files in google drive"
response = chat.send_message(prompt)

#function dispatch
function_call = response.candidates[0].content.parts[0].function_call

#function lookup table
function_lookup = {
    "get_stock_price": get_stock_price,
    "list_files_in_drive": list_files_in_drive
}

#check if function call is initiated by the model
if function_call.name in function_lookup:
    f = function_lookup[function_call.name]
    args = {key: value for key, value in function_call.args.items()}
    #call the function
    function_call_return = f(args)
    #send the result back to the model
    response = chat.send_message(
        Part.from_function_response(
            name=function_call.name,
            response= {
                "content": function_call_return,
            }
        )
    )
    chat_response = response.candidates[0].content.parts[0].text
    print("Chat response: ", chat_response)

else:
    print("Chat response: ", response.text)





