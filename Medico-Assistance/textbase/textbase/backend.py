# textbase/backend.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from textbase.message import Message
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import sys
import logging
from typing import List
import importlib

logging.basicConfig(level=logging.INFO)

load_dotenv()

from .message import Message

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:4000",
    "http://localhost:5173",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    The `read_root` function reads and returns the contents of an HTML file specified by the path
    "textbase/frontend/index.html".
    :return: The content of the "index.html" file located in the "textbase/frontend" directory is being
    returned.
    """
    with open("textbase/frontend/dist/index.html") as f:
        return f.read()


def get_module_from_file_path(file_path: str):
    """
    The function `get_module_from_file_path` takes a file path as input, loads the module from the file,
    and returns the module.

    :param file_path: The file path is the path to the Python file that you want to import as a module.
    It should be a string representing the absolute or relative path to the file
    :type file_path: str
    :return: the module that is loaded from the given file path.
    """
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# textbase/backend.py

...

# textbase/backend.py

...

def handle_healthcare_question(message):
    """
    Function to handle questions about healthcare and mental health and provide the appropriate response.
    """
    question = message.lower().strip()
    if question == "what is healthcare":
        return "Healthcare involves preventing, diagnosing, and treating illnesses and injuries to improve overall well-being. It encompasses medical services provided by professionals and facilities, aiming to promote health and address health-related challenges. Through a combination of preventive measures and interventions, healthcare supports individuals in maintaining optimal physical and mental health."
    elif question == "hii":
        return "hello."
    elif question == "what is mental health":
        return "Mental health refers to a person's psychological, emotional, and social well-being; it influences what they feel and how they think, and behave. The state of cognitive and behavioural well-being is referred to as mental health. The term 'mental health' is also used to refer to the absence of mental disease."
    elif question == "how can i improve my mood":
        return "Engaging in regular physical activity and spending time outdoors can help improve mood by releasing endorphins and increasing exposure to natural light.."
    else:
        return None

@app.post("/chat", response_model=dict)
async def chat(messages: List[Message], state: dict = None):
    """
    Python API endpoint for processing user messages and generating bot responses.
    """
    try:
        file_path = os.environ.get("FILE_PATH")
        logging.info(f"File path: {file_path}")
        if not file_path:
            raise HTTPException(status_code=500, detail="FILE_PATH environment variable is not set.")
        
        module = get_module_from_file_path(file_path)

        logging.info("State: %s", state)

        # Check if the last message asks about the assistant's well-being
        if messages and messages[-1].content.lower() in ["how are you?", "how are you"]:
            return {"botResponse": {"content": "Hi! I'm doing fine, thank you for asking.", "role": "assistant"}}

        # Check if the last message asks about healthcare or mental health
        if messages and messages[-1].role.lower() == "user":
            additional_response = handle_healthcare_question(messages[-1].content)
            if additional_response:
                return {"botResponse": {"content": additional_response, "role": "assistant"}}

        # Call the on_message function from the dynamically loaded module
        response = module.on_message(messages, state)
        if isinstance(response, tuple):
            bot_response, new_state = response
            return {
                "botResponse": {"content": bot_response, "role": "assistant"},
                "newState": new_state,
            }
        elif isinstance(response, str):
            return {"botResponse": {"content": response, "role": "assistant"}}
        else:
            raise HTTPException(status_code=500, detail="Unexpected response type from module.")
    except Exception as e:
        logging.exception("Error during chat processing")
        raise HTTPException(status_code=500, detail=str(e))

# Mount the static directory (frontend files)
app.mount(
    "/assets",
    StaticFiles(directory="textbase/frontend/dist/assets", html=True),
    name="static",
)
