import os.path
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END, START
import random

class AgentState(TypedDict):
    name: str
    numbers: List[int]
    counter: int

def greeting_node(state: AgentState) -> AgentState:
    """A node which greets the user"""
    state['name'] = f"Hi there, {state['name']}"
    state['counter'] = 0

    return  state

def random_node(state: AgentState) -> AgentState:
    """A Node which generates a set of random number from 0 to 10"""
    state['numbers'].append(random.randint(0,10))
    state['counter'] += 1

    return state

def should_continue(state: AgentState) -> AgentState:
    """Function to decide what to do next"""

    if state['counter'] < 5:
        print("Entering loop", state['counter'])
        return "loop"
    else:
        return "exit"


# defining the graph

graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge("greeting", "random")

graph.add_conditional_edges(
    "random",
    path= should_continue,
    path_map={
        "loop": "random", # loop bck to the same node
        "exit": END # end the graph
    }
)

graph.set_entry_point("greeting")

app = graph.compile()

# save the graph
if not os.path.exists("graph.png"):
    with open("graph.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())


# invoking the graph
result = app.invoke({"name": "John", "numbers": [] })





