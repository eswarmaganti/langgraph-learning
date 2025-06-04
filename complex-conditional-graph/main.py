
import os.path
from typing import TypedDict
from langgraph.graph import START, END, StateGraph


class AgentState(TypedDict):
    first_num: int
    second_num: int
    third_num: int
    first_opr: str
    final_opr: str
    first_result: int
    final_result: int


# defining the nodes

def first_addition_node(state: AgentState) -> AgentState:
    state['first_result'] = state['first_num'] + state['second_num']
    return  state

def first_subtraction_node(state: AgentState) -> AgentState:
    state['first_result'] = state['first_num'] - state['second_num']
    return state

def first_router(state: AgentState) -> str:

    if state['first_opr'] == '+':
        return "first_addition_opr"
    elif state['first_opr'] == '-':
        return "first_subtraction_opr"
    else:
        return None


def final_addition_node(state: AgentState) -> AgentState:
    state['final_result'] = state['first_result'] + state['third_num']
    return state


def final_subtraction_node(state: AgentState) -> AgentState:
    state['final_result'] = state['first_result'] - state['third_num']
    return state


def final_router(state: AgentState) -> str:
    if state['final_opr'] == '+':
        return "final_addition_opr"
    elif state['final_opr'] == '-':
        return "final_subtraction_opr"
    else:
        return None


# defining the graph, adding the nodes and edges
graph = StateGraph(AgentState)

graph.add_node("first_addition", first_addition_node)
graph.add_node("first_subtraction", first_subtraction_node)
graph.add_node("first_router", lambda state: state)
graph.add_node("final_addition", final_addition_node)
graph.add_node("final_subtraction", final_subtraction_node)
graph.add_node("final_router", lambda state: state)


graph.add_edge(START, "first_router")
graph.add_conditional_edges(
    source="first_router",
    path=first_router,
    path_map={
        # edge: node
        "first_addition_opr" :"first_addition",
        "first_subtraction_opr" : "first_subtraction"
    }
)

graph.add_edge("first_addition", "final_router")
graph.add_edge("first_subtraction", "final_router")

graph.add_conditional_edges(
    source="final_router",
    path=final_router,
    path_map={
        "final_addition_opr": "final_addition",
        "final_subtraction_opr": "final_subtraction",
    }
)

graph.add_edge("final_addition", END)
graph.add_edge("final_subtraction", END)


app = graph.compile()

if not os.path.exists("graph.png"):
    with open("graph.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
    print("Graph generated and saved successfully")

initial_state = AgentState(
    first_num = 10,
    second_num = 20,
    third_num = 30,
    first_opr = '+',
    final_opr='-'
)

result = app.invoke(initial_state)
