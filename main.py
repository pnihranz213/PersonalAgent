from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

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

    tools = [calculator, say_hello]
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
                    print(message.content, end="")

if __name__ == "__main__":
    print("Starting the calendar assistant...")
    main()