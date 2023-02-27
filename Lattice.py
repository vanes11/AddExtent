from graphviz import Graph

def draw_lattice(concepts, relations):
    dot = Graph()
    # Add the nodes to the graph
    for concept in concepts:
        dot.node(str(concept.extent), label="{"+ ",".join(sorted(concept.extent))+"}"+" ; "+"{"+",".join(sorted(concept.intent))+"}")

    # Add the edges to the graph    
    for relation in relations:
        parent, child = relation
        dot.edge(str(parent), str(child))

    
    
    
    

    """ for concept in concepts:
        dot.node(str(concept), label="("+ ",".join(sorted(concept.extent))+" ; "+",".join(sorted(concept.intent))+")") """

    # Set the layout of the graph and display it
    dot.attr(layout="dot")
    dot.render(filename='Treillis/lattice',format="svg")
    dot.render(filename='Treillis/lattice', format="png")
    dot.render(filename='Treillis/lattice',format="pdf")
    dot.render(filename='Treillis/lattice', format="dot")
