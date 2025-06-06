# ReAct Agent
## Objectives:
1. Learn how to create `Tools` in LangGraph
2. How to create a `ReAct Graph`
3. Work with different types of `Messages` such as `ToolMessages`
4. Test out robustness of our graph

`Main Goal: Create a robust ReAct Agent!`


### `add_messages` method in `langgraph.graph.messages`
- langgraph models workflows as graphs of nodes
- Nodes send messages to each other to pass data, trigger actions, or return results.
- The `add_messages` method is used to add one or more messages to a message queue or collection that the graph runtime processes.
### Typical purpose of `add_messages`
- Queueing messages for downstream nodes.
- Managing asynchronous or synchronous task results
- Updating the state of the graph execution with new information
- Ensuring data flows correctly through nodes by passing messages along edges.
- 