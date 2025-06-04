import random
from typing import TypedDict, Dict, List
from langgraph.graph import StateGraph, START, END
import os


# defining the graph state
class AgentState(TypedDict):
    player_name: str
    target_number: int
    guesses: List[int]
    attempts: int
    lower_bound: int
    upper_bound: int
    hint: str


# defining the graph nodes
def setup_node(state: AgentState) -> AgentState:
    """A node used to set up and initialize the application"""

    state["player_name"] = f"Welcome! {state['player_name']}"
    state['attempts'] = 0
    state['guesses'] = []
    state['lower_bound'] = 1
    state['upper_bound'] = 20
    state['target_number'] = random.randint(state['lower_bound'], state['upper_bound'])
    state['hint'] = "Guess a number between 1 to 20"
    return state


def guess_node(state: AgentState) -> AgentState:
    """Node to guess the random number in the lower and upper bound range"""
    state['guesses'].append(random.randint(state['lower_bound'], state['upper_bound']))

    state['attempts'] += 1
    return state



def hint_node(state: AgentState) -> AgentState:
    """Give hint and updates the lower and upper bounds accordingly"""
    last_guess = state['guesses'][-1]


    if last_guess > state['target_number']:
        state['hint'] = f'The number {last_guess} is too high, Try lower number'
        state['upper_bound'] = min(state['upper_bound'], last_guess-1)

        print(f"The Hint: {state['hint']}")
    elif last_guess < state['target_number']:
        state['hint'] = f'The number {last_guess} is too low, Try higher number'
        state['lower_bound'] = max(state['lower_bound'], last_guess + 1)

        print(f"The Hint: {state['hint']}")
    else:
        state['hint'] = f"Congrats!! you guessed the number {state['target_number']} in {state['attempts']} attempts"
    return state

def perform_next(state: AgentState) -> AgentState:
    """Node to validate the guess and performs next action"""

    last_guess = state['guesses'][-1]
    if  last_guess == state['target_number'] :
        print("Game Over!!! You found the number")
        return "exit"
    elif state['attempts'] == 7:
        print("Game Over!!! All your attempts are over")
        return "exit"
    else:
        return "continue"


graph = StateGraph(AgentState)

graph.add_node("setup_node", setup_node)
graph.add_node("guess_node", guess_node)
graph.add_node("hint_node", hint_node)

graph.add_edge("setup_node", "guess_node")
graph.add_edge("guess_node", "hint_node")

graph.add_conditional_edges(
    source="hint_node",
    path=perform_next,
    path_map={
        "exit": END,
        "continue": "guess_node"
    }
)

graph.set_entry_point("setup_node")


app = graph.compile()

# save the graph
if not os.path.exists("graph.png"):
    with open("graph.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())


result = app.invoke({
    "player_name": "Eswar",
    "guesses":[],
    "attempts":0,
    "lower_bound":1,
    "upper_bound":20
})

print(result)