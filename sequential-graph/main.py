# Imports
from langgraph.graph import StateGraph
from typing import TypedDict, Dict, List
# defining the graph state
class AgentState(TypedDict):
    name: str
    age: int
    skills: List[str]
    result: str
# defining the graphs nodes
def first_node(state: AgentState) -> AgentState:
    state['result'] = f'''{state['name']}, welcome to the system,'''
    return state
def second_node(state: AgentState) -> AgentState:
    state['result'] = f'''{state.get('result')} Your are {state.get('age')} years old!'''
    return  state
def third_node(state: AgentState) -> AgentState:
    state['result'] = f'''{state.get('result')} You have skills in {' '.join(state.get('skills'))}'''
    return state
# defining the graph and edges
graph = StateGraph(AgentState)
# Adding the nodes to the graph
graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)
# creating the edges between the graph nodes
graph.add_edge(start_key="first_node", end_key="second_node")
graph.add_edge(start_key="second_node", end_key="third_node")
graph.set_entry_point("first_node")
graph.set_finish_point("third_node")
app = graph.compile()
# save the graph png to local
graph_png = app.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(graph_png)
result = app.invoke({"name": "Sam Wilson", "age": "40", "skills": ["Python", "React", "GenAI"]})
print(result)
