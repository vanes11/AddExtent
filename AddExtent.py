from collections import namedtuple
#from socket import gethostbyaddr
from unittest import result


Concept = namedtuple("Concept", ["extent", "intent"]) ## a concept definition


def GetMaximalConcept(extent, GeneratorConcept, L):
    """ Search in de lattice L the smallest concept that can generate the concept (extent,...) 
    i.e, the smallest concept in L containing the parameta extent in it extension""" 

    ChildIsMinimal = True
    while ChildIsMinimal:
        ChildIsMinimal = False
        Children = GetChildren(GeneratorConcept, L)

        for Child in Children :
            if extent.issubset(Child.extent):
                GeneratorConcept = Child
                ChildIsMinimal = True
                break
    return GeneratorConcept  



def GetChildren(GeneratorConcept, L):
    """ Search in the lattice L the children of the concept GeneratorConcept """

    Children = []
    CopyL = list.copy(L)
    for concept in L:
        test = True
      
        for candidateChil in CopyL :
            if candidateChil!=concept and candidateChil != concept and concept.extent < candidateChil.extent and candidateChil.extent < GeneratorConcept.extent:
                test = False
                break
        if concept.extent < GeneratorConcept.extent and test==True:
            Children.append(concept)
    return Children


def GetChildrenOfChil(AttributConcept,L,result, Children):
    """ return all the concepts below AttributConcept in the lattice L """

    cle = "".join(sorted(list(AttributConcept.extent)))
    result[cle] = Children

    for elt in Children:
        NewChildren = GetChildren(elt,L)
        if NewChildren!= []:
            GetChildrenOfChil(elt,L,result,NewChildren)
    
    return result




def GetParents(GeneratorConcept, L):
    """ Search in the lattice L the parents of the concept GeneratorConcept """

    Parents = []
    CopyL = list.copy(L)
    for concept in L:
        test = True
       
        for candidateChil in CopyL :
            if candidateChil!=concept and candidateChil != concept and concept.extent > candidateChil.extent and candidateChil.extent > GeneratorConcept.extent:
                test = False
                break
        if concept.extent >  GeneratorConcept.extent and test==True:
            Parents.append(concept)
    return Parents



def AddExtent(extent,GeneratorConcept,L,RelationList):
    """ Goal - Add the concept having for extension "extent" name NewConcept in the lattice L.
    1- find the generating concept of said concept,
    2- create or identify its children, create the new concept, 
    and set the different links between NewConcept and its children, 
    without forgetting the one between NewConcept and its generating concept."""

    GeneratorConcept = GetMaximalConcept(extent, GeneratorConcept, L)

    if GeneratorConcept.extent == extent: 
        return GeneratorConcept

    GeneratorChildren = GetChildren(GeneratorConcept, L)
   
    NewChildren = []# contain the list of the NewConcept children
    
    for Candidate in GeneratorChildren:
        if not(Candidate.extent.issubset(extent)) == True:
            #intersectionExtent = Candidate.extent.intersection(extent)
            Candidate= AddExtent(Candidate.extent.intersection(extent), Candidate, L,RelationList)

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
    L.append(NewConcept)
    

    for Child in NewChildren:
        relation = (Child.extent, GeneratorConcept.extent)
        if relation in  RelationList:
            RelationList.remove(relation) #RemoveLink (Child, GeneratorConcept, L)
        relation = (Child.extent, NewConcept.extent)#SetLink(Child, NewConcept, L)
        RelationList.append(relation)

    relation = (NewConcept.extent, GeneratorConcept.extent)#SetLink(NewConcept, GeneratorConcept, L)
    RelationList.append(relation)

    return NewConcept




def AddExtent2(extent,GeneratorConcept,L,RelationList):

    GeneratorConcept = GetMaximalConcept(extent, GeneratorConcept, L)

    if GeneratorConcept.extent == extent: 
        return GeneratorConcept

    GeneratorChildren = GetChildren(GeneratorConcept, L)
    NewChildren = []
    
    for Candidate in GeneratorChildren:
        if not(Candidate.extent.issubset(extent)) == True:
            Candidate= AddExtent2(Candidate.extent.intersection(extent), Candidate, L,RelationList)

        AddChild = True
        for Child  in NewChildren:
            if Candidate.extent.issubset(Child.extent):
                AddChild = False
                break
        
            elif Child.extent.issubset(Candidate.extent):
                NewChildren.remove(Child)

        if AddChild:
            NewChildren.append(Candidate)

    NewConcept = Concept(extent, set())
    L.append(NewConcept)


    for Child in NewChildren:
        relation = (Child.extent, GeneratorConcept.extent)
        if relation in  RelationList:
            RelationList.remove(relation) 
        relation = (Child.extent, NewConcept.extent)
        RelationList.append(relation)

    relation = (NewConcept.extent, GeneratorConcept.extent)
    RelationList.append(relation)

    return NewConcept


