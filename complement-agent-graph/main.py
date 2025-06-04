#!/usr/bin/env python
# coding: utf-8

# In[1]:


from langgraph.graph import StateGraph
from typing import Dict, TypedDict


# In[8]:


# defining the agent state

class AgentState(TypedDict):
    name: str
    message: str

# defining the node
def complement_node(state: AgentState) -> AgentState:
    '''Complement Node that generates a customized complement'''
    state['message'] = f"{state.get('name')}, You are doing a great job by learning LangGraph!!"
    return state


# In[9]:


# defining the graph
graph = StateGraph(AgentState)

# adding the node to the graph
graph.add_node("complement", complement_node)

# defining the start and end points
graph.set_entry_point("complement")
graph.set_finish_point("complement")

# compiling the graph
app = graph.compile()


# In[11]:


# invoking the graph with a user name
result = app.invoke({"name": "Eswar Maganti"})

print(result['message'])


# In[ ]:




