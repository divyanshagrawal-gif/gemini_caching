from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.5,  
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# message = HumanMessage(content="Hello, how are you?")
# response = model.invoke([message])
# print(response.text)