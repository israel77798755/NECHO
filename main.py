
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file!")


# ==========================================
# 2. INITIALIZE GEMINI MODEL
# ==========================================

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key,
    max_retries=2,
    timeout=60
)


# ==========================================
# 3. DEFINE CHATBOT NODE
# ==========================================

def chatbot(state: MessagesState):

    response = model.invoke(state["messages"])

    return {"messages": [response]}


# ==========================================
# 4. CREATE LANGGRAPH WORKFLOW
# ==========================================

workflow = StateGraph(MessagesState)

workflow.add_node("chatbot", chatbot)

workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)


# ==========================================
# 5. SET UP CONVERSATION MEMORY
# ==========================================

memory = MemorySaver()

app = workflow.compile(checkpointer=memory)


# ==========================================
# 6. CONFIGURE CONVERSATION THREAD
# ==========================================

config = {
    "configurable": {
        "thread_id": "necho_conversation_1"
    }
}


# ==========================================
# 7. START NECHO CHATBOT
# ==========================================

def main():

    print("\n" + "=" * 45)
    print("              WELCOME TO NECHO")
    print("=" * 45)

    print("NECHO is ready to chat!")
    print("Type 'exit' to end the conversation.\n")

    while True:

        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("\nNECHO: Goodbye! See you again.")
            break

        try:

            result = app.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=config
            )

            print("\nNECHO:", result["messages"][-1].text)
            print()

        except Exception as error:

            print("\nNECHO encountered an error:")
            print(error)
            print()


# ==========================================
# 8. RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    main()
