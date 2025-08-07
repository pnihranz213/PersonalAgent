from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_google_community import CalendarToolkit, calendar
from langchain_google_community.calendar.utils import (
    build_resource_service,
    get_google_credentials,
)

# Can review scopes here: https://developers.google.com/calendar/api/auth
# For instance, readonly scope is https://www.googleapis.com/auth/calendar.readonly
credentials = get_google_credentials(
    token_file="token.json",
    scopes=["https://www.googleapis.com/auth/calendar"],
    client_secrets_file="credentials.json",
)

api_resource = build_resource_service(credentials=credentials)
toolkit = CalendarToolkit(api_resource=api_resource)
cal_tools = toolkit.get_tools()

load_dotenv()

@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmeric calculations with numbers"""
    print("Tool has been called.")
    return f"The sum of {a} and {b} is {a + b}"
    
@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user"""
    print("Tool has been called.")
    return f"Hello {name}, I hope you are well today"

def main():

    llm = ChatOpenAI(temperature=0)

    tools = [calculator, say_hello] + cal_tools  # Combine your tools with calendar tools
    agent_executor = create_react_agent(llm, tools)

    print("Hello! How can I assist you today?")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        print(f"\nAgent: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    # Remove lines with "You can view the event" or links
                    lines = message.content.splitlines()
                    filtered_lines = [
                        line for line in lines
                        if "You can view the event" not in line and "http" not in line
                    ]
                    print("\n".join(filtered_lines), end="")

if __name__ == "__main__":
    print("Starting the calendar assistant...")
    main()