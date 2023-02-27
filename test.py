import networkx as nx
import matplotlib.pyplot as plt

def draw_lattice(concepts):
    """Draw a concept lattice using NetworkX."""
    # Create an empty directed graph
    G = nx.DiGraph()

    # Add the concepts as nodes in the graph
    for concept in concepts:
        #G.add_node(concept)
        G.add_nodes_from((set(concept),concepts[concept]))

    # Add edges between concepts based on the subsumption relationship
    for i, ci in enumerate(concepts):
        for j, cj in enumerate(concepts):
            
            if i != j and set(ci).issubset(set(cj))and set(ci).issuperset(set(cj)):
                G.add_edge(cj, ci)

    # Define the layout of the graph and draw it
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="white", edgecolors="black")
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")
    plt.axis("off")
    plt.show()



from collections import namedtuple

# Define some example concepts
Concept = namedtuple("Concept", ["intent", "extent"])
concept = []
""" c1 = Concept(set(["a", "b"]), set(["x", "y"]))
concept.append(c1)
c2 = Concept(set(["a"]), set(["x"]))
concept.append(c2)
c3 = Concept(set(["a", "b", "c"]), set(["x", "y", "z"]))
concept.append(c3)
c4 = Concept(set(["a", "b"]), set(["y", "z"]))
concept.append(c4) """


""" c1 = (1, {("a","b"): ("x","y")})
concept.append(c1)
c1 = (1, {("a"): ("x")})
concept.append(c1)
c3 =  (2, {("a", "b", "c"): ("x", "y", "z")})
concept.append(c3)
c4 = (3, {("a", "b"): ("y", "z")})
concept.append(c4) """


""" c1 =[{"a","b"},{"x","y"}]
concept.append(c1)
c1 = [{"a"},{"x"}]
concept.append(c1)
c3 = [{"a", "b", "c"},{"x", "y", "z"}]
concept.append(c3)
c4 = [{"a", "b"},{"y", "z"}]
concept.append(c4)
 """

""" c = {}
c[("a","b")] = {"x","y"}
c[("a")] = {"x"}
c[("a", "b", "c")] = {"x", "y", "z"}
c[("a", "c")]= {"y", "z"}
 """

c = []
c1 = "(a,b),(x,y)"
c.append(c1)
c2 = "(a),(x)"
c.append(c2)
c3 ="(a,b,c),(x,y,z)"
c.append(c3)
c4 = "(a,b),(y,z)"
c.append(c4)



for i,j in enumerate(c):
    print(type(j))
    t = j.split(")")
    print(set(t[0][1:]), t[0][1:],tuple(t[0][1:]))
exit()
#concepts = {c1, c2, c3, c4}

# Draw the concept lattice
draw_lattice(c)