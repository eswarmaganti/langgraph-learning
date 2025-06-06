from  langgraph.graph import StateGraph, START, END
from  typing import TypedDict, List, Dict, Union
from langchain_core.messages import HumanMessage, AIMessage
from  langchain_ollama import ChatOllama



# defining the agent's state
class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatOllama(model="llama3.2")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    state['messages'].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")

    print(f'\n {state}')
    return state


graph = StateGraph(AgentState)

graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

conversation_history = []

user_input = input("Enter a message: ")

while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]
    user_input = input("Enter a message: ")


# save the conversation to the local file

with open("chat_history.txt", "a+") as f:
    f.write("Start of conversation")
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            f.write(f"You: {message.content}\n")
        if isinstance(message, AIMessage):
            f.write(f"AI: {message.content}\n")
    else:
        f.write("End of conversation")

