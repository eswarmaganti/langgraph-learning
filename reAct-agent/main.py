from typing import TypedDict, Annotated, Sequence

from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage, BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages



# defining the agent state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# defining the arithmetic tools for the application
@tool
def add(a: int, b: int)-> int:
    """This function takes two integer parameters as input, performs addition and returns the result"""

    return  a+b

@tool
def subtract(a: int, b: int) -> int:
    """This function takes two integer parameters as inputs, performs subtraction and returns the result"""

    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """This function takes two integer parameters as inputs, performs multiplication and returns the result"""

    return a * b

tools = [add, subtract, multiply]

# defining the llm model

model = ChatOllama(model='llama3.2').bind_tools(tools)


# defining the graph nodes
def model_call(state: AgentState) -> AgentState:
    prompt = [SystemMessage(
        content="You are an AI assistant, please answer my query to the best of your ability."
    )] + state['messages']

    response = model.invoke(prompt)

    return {'messages': response}

tool_node = ToolNode(tools=tools)

# check whether to continue the calls to tool node or end
def should_continue(state: AgentState) -> AgentState:
    messages = state.get('messages')
    last_message = messages[-1]

    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"


# defining the graph and its nodes
graph = StateGraph(AgentState)

graph.add_node("agent", model_call)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_edge( "tools", "agent")
graph.add_conditional_edges(
    source="agent",
    path=should_continue,
    path_map={
        "continue": "tools",
        "end": END
    }
)


agent = graph.compile()

# save the graph to local path
with open("graph.png", "wb+") as f:
    f.write(agent.get_graph().draw_mermaid_png())


# method to print the agent response

def print_stream(streams):
    for stream in streams:
        message = stream['messages'][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {"messages": [HumanMessage("what is the result of Add 5 + 2 and Multiply 10*11, tell me a joke?")]}

print_stream(agent.stream(inputs, stream_mode="values"))