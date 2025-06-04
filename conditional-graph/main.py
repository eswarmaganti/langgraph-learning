import os.path
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    num1: int
    num2: int
    operation: str
    result: int


def adder(state: AgentState) -> AgentState:
    """This node adds two numbers"""
    state['result'] = state['num1'] + state['num2']

    return state
def subtractor(state: AgentState) -> AgentState:
    """This node subtracts the two numbers"""
    state['result'] = state['num1'] - state['num2']

    return state

def decide_next_node(state: AgentState) -> str:
    """This node decides the selection of next node based on operation in state"""

    if state['operation'] == '+':
        return "addition_opr"
    elif state['operation'] == '-':
        return "subtraction_opr"

    return None


# defining the state

graph = StateGraph(AgentState)

graph.add_node("addition_node", adder)
graph.add_node("subtraction_node", subtractor)
graph.add_node("router", lambda state:state)

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        # format "edge":"node"
        "addition_opr": "addition_node",
        "subtraction_opr": "subtraction_node"
    }
)

graph.add_edge("addition_node", END)
graph.add_edge("subtraction_node", END)

app = graph.compile()

# save the graph
if not os.path.exists("graph.png"):
    with open("graph.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())

    print("Graph image created successfully")

initial_state = AgentState(num1=10, num2=2, operation="+")
result = app.invoke(initial_state)
print(result)