import os
import concepts
from concepts import Context
from collections import namedtuple
import Lattice
import AddExtent as ae




current_dir = os.getcwd()
context_path = str(current_dir)+'/exemple.csv'


#context_path2 = str(current_dir)+'/ContextExampleC'
#context_path3 = str(current_dir)+'/example_context.json'


if context_path.endswith(".csv"):
    context = Context.fromfile(context_path,frmat='csv')
    
elif context_path.endswith(".cxt"):
    context = Context.fromfile(context_path,frmat='csv')
    
else:
    context = Context.fromfile(context_path,frmat='csv')
    

Concept = namedtuple("Concept", ["extent", "intent"]) ## a concept definition




def CreateLatticeIncrementally (context):
    G = context.objects
    M = sorted(context.properties)
    L = [] #list Of   Concepts
    RelationList = [] # list of relations     
    TopConcept = Concept(set(G),set()) 
    L.append(TopConcept) 

    for m in M:
        ListOfConcepts = []
        extent = set(context.extension(m))
        AttributConcept = ae.AddExtent(extent, TopConcept, L, RelationList) # is the children of attributConcept
         
        ######Add m to the intent of AttributConcept and all concepts below ######
        L.remove(AttributConcept)
        lastIntent = AttributConcept.intent
        AttributConcept = AttributConcept._replace(intent = lastIntent.union(set(m)))

        if AttributConcept.extent == TopConcept.extent: # mettre a jour le topConcept de depart,car il y'a aumoins un attribut qui est vrai pour chaque objet
            TopConcept=AttributConcept

        L.append(AttributConcept)
        
        ###### Get all the conceapts above the attribut concept
        Children = ae.GetChildren(AttributConcept,L)
        result = dict()
        results = ae.GetChildrenOfChil(AttributConcept, L, result, Children)
        temp = []
        ChilOfChildren = dict()
        for key, val in results.items():
            if val not in temp:
                temp.append(val)
                ChilOfChildren[key] = val# remove duplicates values in results
        Finalresults = [val for key, val in ChilOfChildren.items()]
        flat_list = [item for sublist in Finalresults for item in sublist]#concert a list of list to et flat list
        AttributConceptChildren = [elt.extent for elt in flat_list]

        for concept in L:  
            check = concept.extent in (item for item in AttributConceptChildren)
            if check:
                lastIntent = concept.intent
                concept = concept._replace(intent = lastIntent.union(set(m)))# lastIntent.union(set(m)))
                ListOfConcepts.append(concept)
            else:
                ListOfConcepts.append(concept)
        L = ListOfConcepts
        

    return L, RelationList







def SimplifiedLattice (context):
    """ Les attributs se transmettent par hierachie descendante et les objets par heritage ascendante """

    G = context.objects
    M = sorted(context.properties)
    LL = [] 
    RelationList = []  
    TopConcept = Concept(set(G),set()) 
    LL.append(TopConcept) 

    for m in M:
       
        extent = set(context.extension(m)) 
        AttributConcept = ae.AddExtent2(extent, TopConcept, LL, RelationList) 
        ######Add m to the intent of AttributConcept ######
        
        LL.remove(AttributConcept)
        lastIntent = AttributConcept.intent
        AttributConcept = AttributConcept._replace(intent = lastIntent.union(set(m)))
        LL.append(AttributConcept)

        if AttributConcept.extent == TopConcept.extent: 
            TopConcept=AttributConcept
  
    return LL, RelationList



#################### lattice construction #################

ListOfConcepts,RelationList = CreateLatticeIncrementally (context)
#LL, Relations = SimplifiedLattice (context)

""" print("longueur de ListOfconcepts : nombre de noeuds = ", len(LL))
print("longuer de RelationList :  nombre de liaisons= ", len(Relations)) """


print("longueur de ListOfconcepts : nombre de noeuds = ", len(ListOfConcepts))
print("longuer de RelationList :  nombre de liaisons= ", len(RelationList))
Lattice.draw_lattice1(ListOfConcepts,RelationList)

#Lattice.draw_lattice2(LL,Relations)

