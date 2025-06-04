#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install langgraph Ipython


# In[3]:


from typing import Dict, TypedDict
from langgraph.graph import StateGraph
from IPython.display import Image, display
# StateGraph is a framework that helps us to design and manage the flow of tasks in your application using a graph


# In[11]:


# AgentState - shared data structure that keeps track of information as your application runs.
class AgentState(TypedDict): # a state schema
    message: str


# defining a node
# it takes the state as input and outputs the updated state
def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting message to the state"""

    state["message"] = f"Hey {state['message']} how is your day going?"

    return state



# In[13]:


# defining a graph
graph = StateGraph(AgentState)

# adding a node the graph
graph.add_node(node="greeter", action=greeting_node)

# defining the start and end points
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

# compiling the graph
app = graph.compile()

# displaying the graph structure using IPython
display(Image(app.get_graph().draw_mermaid_png()))


# In[20]:


result = app.invoke({"message": "Bob"})


# In[21]:


result["message"]


# In[ ]:




