import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent

load_dotenv()

def get_agent(model_name: str, system_prompt: str, allow_search: bool):
    llm = ChatGroq(model=model_name, temperature=0)
    tools = [TavilySearchResults(max_results=2)] if allow_search else []
    
    # Version-proof fix: We remove the modifier here entirely!
    agent = create_react_agent(llm, tools)
    return agent