from multiprocessing import Condition
import os
import concepts
from concepts import Context
from collections import namedtuple
import Lattice
#import graphvizTest



current_dir = os.getcwd()
context_path = str(current_dir)+'/context.csv'
context = Context.fromfile(context_path,frmat='csv')

#context_path2 = str(current_dir)+'/ContextExample'
#context_path3 = str(current_dir)+'/example_context.json'


""" if context_path.endswith(".csv"):
    context = concepts.load_csv(context_path)
    print("csv")
    print(context)
elif context_path.endswith(".cxt"):
    context = concepts.load_cxt(context_path)
    print("cxt")
    print(context)
else:
    context = concepts.load(context_path)
    print("other")
    print(context) """

#G = list(context.objects)
#M = list(context.properties)


Concept = namedtuple("Concept", ["extent", "intent"]) ## a concept definition
RelationList = [] # list of relations 
def CreateLatticeIncrementally (context):
    G = context.objects
    M = sorted(context.properties)
    L = [] #list Of   Concepts
    l = context.lattice
    T=l.supremum
    T= str(T)
    t = T.split("<->")
    tt = t[1].split("<=>")
    s = t[0].replace("{","")
    s = s.replace("}","")
    t = "".join(c for c in s if c.isalpha())
    ss = tt[0].replace("[","")
    ss = ss.replace("]","")
    tt = "".join(c for c in ss if c.isalpha())
   
    #print(t, tt)
    #Concept = namedtuple("Concept", ["extent", "intent"]) ## a concept definition
    TopConcept = Concept(set(list(t)),set(list(tt)))
    
    #TopConcept = Concept(set(G),set()) #?? le top concept est-il pareil toujours tout le temps?
    L.append(TopConcept) 
    AttributConceptList = [] 

    for m in M:
        ListOfConcepts = []
        extent = set(context.extension(m))
        AttributConceptExtent = []
        AttributConcept = AddExtent(extent, TopConcept, L)
        
        #Add m to the intent of propertyConcept and all concepts below
        #print("AttributConcept avant = ",AttributConcept)

        L.remove(AttributConcept)
        lastIntent = AttributConcept.intent
        AttributConcept = AttributConcept._replace(intent = lastIntent.union(set(m)))
        L.append(AttributConcept)
        AttributConceptList.append(AttributConcept)
        #AttributConceptChildren = GetChildren(AttributConcept,L)
        Children = [] # liste contenant les extensions des concepts enfants de Attributconcept
        for elt in RelationList:

            if elt[0] ==  AttributConcept.extent and elt[0].issuperset((elt[1])):
                Children.append(elt[1])
            elif elt[1]==AttributConcept.extent and elt[1].issuperset((elt[0])):
                 Children.append(elt[0])
            
        #print("relation children : = ", Children,"----",AttributConcept.extent )
        for concept in L:  
            check1 = concept.extent in (item for item in Children)
            if check1:
                lastIntent = concept.intent
                concept = concept._replace(intent = lastIntent.union(AttributConcept.intent))
                ListOfConcepts.append(concept)
            else:
                ListOfConcepts.append(concept)
        L = ListOfConcepts
    temp1 = [x for x in L if x not in (item for item in AttributConceptList)]
    temp = [x for x in temp1 if (x.extent != item.extent for item in AttributConceptList) and (x.extent != item.extent for item in AttributConceptList)]#list of concept not in relation with any attributconcept
        
    #print(len(temp), temp)
    for elt in temp:
        eltParents = GetParents(elt,L)
        lastIntent = elt.intent
        L.remove(elt)
        eltParentsIntent = [concept.intent for concept in eltParents]
        Intent = set()
        for intent in eltParentsIntent:
            Intent = Intent.union(intent)

        elt = elt._replace(intent = lastIntent.union(set(Intent)))
        L.append(elt)



        """ for concept in L:
            check = concept in (item for item in AttributConceptChildren)
            print(check)
            if check:
                print("ok")
                lastIntent = concept.intent
                print(lastIntent)
                concept = concept._replace(intent = lastIntent.union(set(m)))
                print(concept.intent)
                
                ListOfConcepts.append(concept)
            else:
                ListOfConcepts.append(concept)
        L = ListOfConcepts """
       
    return L, RelationList



def GetMaximalConcept(extent, GeneratorConcept, L):
    #print(L,"juste apres")
    ChildIsMinimal = True
    while ChildIsMinimal:
        ChildIsMinimal = False
        Children = GetChildren(GeneratorConcept, L)
        #print(Children,"liste des enfants")

        for Child in Children :
            if extent.issubset(Child.extent):
                GeneratorConcept = Child
                ChildIsMinimal = True
                break
    #print(L,"apress")
    return GeneratorConcept  



def GetChildren(GeneratorConcept, L):
    
    Children = []
    CopyL = list.copy(L)
    
    for concept in L:
        test = True
        CopyL.remove(concept)
        
        for candidateChil in CopyL :
            if candidateChil!=concept and concept.extent < candidateChil.extent and candidateChil.extent < GeneratorConcept.extent:
                test = False
                break
        if concept.extent < GeneratorConcept.extent and test==True:
            Children.append(concept)
        #print(Children)
    return Children

def GetParents(GeneratorConcept, L):
    
    Parents = []
    CopyL = list.copy(L)
    
    for concept in L:
        test = True
        CopyL.remove(concept)
        
        for candidateChil in CopyL :
            if candidateChil!=concept and concept.extent > candidateChil.extent and candidateChil.extent > GeneratorConcept.extent:
                test = False
                break
        if concept.extent >  GeneratorConcept.extent and test==True:
            Parents.append(concept)
        #print(Children)
    return Parents


def AddExtent(extent,GeneratorConcept,L):
    GeneratorConcept = GetMaximalConcept(extent, GeneratorConcept, L)
    if GeneratorConcept.extent == extent: 
        return GeneratorConcept

    GeneratorChildren = GetChildren(GeneratorConcept, L)
    #print(GeneratorChildren)
    NewChildren = []

    for Candidate in GeneratorChildren:
        if not(Candidate.extent.issubset(extent)) == True:
            #intersectionExtent = Candidate.extent.intersection(extent)
            Candidate = AddExtent(Candidate.extent.intersection(extent), Candidate, L)

        AddChild = True
        for Child  in NewChildren:
            if Candidate.extent.issubset(Child.extent):
                AddChild = False
                break
        
            elif Child.extent.issubset(Candidate.extent):
                NewChildren.remove(Child)

        if AddChild:
            NewChildren.append(Candidate)

    NewConcept = Concept(extent, GeneratorConcept.intent)
    """ if NewConcept.extent == {'d'}:
        print(NewChildren) """
    #print(NewConcept,"******",L)
    L.append(NewConcept)
    #print("new children: = ", NewChildren)
    for Child in NewChildren:
        relation = (Child.extent, GeneratorConcept.extent)
        if relation in  RelationList:
        #RemoveLink (Child, GeneratorConcept, L)
        #SetLink(Child, NewConcept, L)
            RelationList.remove(relation)
        relation = (Child.extent, NewConcept.extent)
        RelationList.append(relation)

    #SetLink(NewConcept, GeneratorConcept, L)
    relation = (NewConcept.extent, GeneratorConcept.extent)
    RelationList.append(relation)

    return NewConcept



    

ListOfConcepts,RelationList = CreateLatticeIncrementally (context)
#print(ListOfConcepts)
#print(RelationList)
print("longueur de ListOfconcepts : nombre de noeuds = ", len(ListOfConcepts))
print("longuer de RelationList :  nombre de liaisons= ", len(RelationList))
RelationList.reverse()
ListOfConcepts.reverse()
Lattice.draw_lattice(ListOfConcepts,RelationList)
#graphvizTest.draw_lattice(ListOfConcepts)