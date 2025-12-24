from langgraph.graph import START, StateGraph

def build_graph(State, retrieve, generate):
    """Create and compile a state graph with retrieve and generate."""
    # Create the graph
    graph_builder = StateGraph(State)
    
    # Add nodes with their names
    graph_builder.add_node("retrieve_node", retrieve)
    graph_builder.add_node("generate_node", generate)
    
    # Add edges
    graph_builder.add_edge(START, "retrieve_node")
    graph_builder.add_edge("retrieve_node", "generate_node")
    
    return graph_builder.compile()
