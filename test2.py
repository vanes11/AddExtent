def add_intent(concept_lattice, intent):
    """
    Add a new intent to the concept lattice.

    concept_lattice: the concept lattice to update
    intent: the new intent to add
    """
    # Create a new concept with the given intent and empty extent
    new_concept = (intent, set())

    # Find the parents of the new concept
    parents = []
    for concept in concept_lattice:
        if concept[0].issubset(intent):
            parents.append(concept)

    # Add the new concept to the lattice and connect it to its parents
    concept_lattice.append(new_concept)
    for parent in parents:
        parent[1].add(new_concept)
    
    # Compute the extent of the new concept
    new_concept_extent = set()
    for object in concept_lattice[0][1]:
        if intent.issubset(object):
            new_concept_extent.add(object)
    new_concept[1] = new_concept_extent
    
    # Update the lower neighbors of the new concept
    lower_neighbors = [x for x in new_concept[1]]
    while lower_neighbors:
        current_object = lower_neighbors.pop()
        current_concept = get_concept_by_extent(concept_lattice, current_object)
        if current_concept not in parents:
            current_concept[0] = current_concept[0].union(intent)
            for child in current_concept[1]:
                if child not in lower_neighbors:
                    lower_neighbors.append(child)
                    
    # Update the upper neighbors of the new concept
    upper_neighbors = [new_concept]
    while upper_neighbors:
        current_concept = upper_neighbors.pop()
        for parent in [x for x in current_concept[1]]:
            parent_extent = parent[1]
            parent_intent = parent[0]
            if parent_intent.issubset(new_concept[0]):
                continue
            if parent_extent.issubset(new_concept[1]):
                parent[0] = parent[0].union(intent)
                if parent not in upper_neighbors:
                    upper_neighbors.append(parent)
                for grandchild in parent[1]:
                    if grandchild not in upper_neighbors:
                        upper_neighbors.append(grandchild)

