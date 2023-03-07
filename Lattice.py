from graphviz import Graph
from graphviz import Digraph

def draw_lattice1(concepts, relations):
    dot = Graph()
    # Add the nodes to the graph
    for concept in concepts:
        dot.node(str(concept.extent), label="{"+ ",".join(sorted(concept.extent))+"}"+" ; "+"{"+",".join(sorted(concept.intent))+"}")

    # Add the edges to the graph    
    for relation in relations:
        child,parent = relation
        dot.edge(str(parent), str(child))


    # Set the layout of the graph and display it
    dot.attr(layout="dot")
    dot.render(filename='Treillis/lattice',format="svg")
    dot.render(filename='Treillis/lattice', format="png")
    dot.render(filename='Treillis/lattice',format="pdf")
    dot.render(filename='Treillis/lattice', format="dot")


def draw_lattice2(concepts, relations):
    dot = Digraph()
    for concept in concepts:
        dot.node(str(concept.extent), label="{"+ ",".join(sorted(concept.extent))+"}"+" ; "+"{"+",".join(sorted(concept.intent))+"}")

    
    for relation in relations:
        child,parent = relation
        dot.edge(str(parent), str(child))


    dot.attr(layout="dot")
    dot.render(filename='Treillis/lattice1',format="svg")
    dot.render(filename='Treillis/lattice1', format="png")
    dot.render(filename='Treillis/lattice1',format="pdf")
    dot.render(filename='Treillis/lattice1', format="dot")

