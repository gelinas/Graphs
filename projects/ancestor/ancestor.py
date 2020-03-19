
# 1. Translate the problem into graph terminology
'''
Directed acyclic graph
(parent, child)
depth first search from child -> parent -> parent and see which chain is longest
'''

# 2. Build your graph
'''
Graph is built when parent, child relationships put in as 'ancestors' arg
'''

# 3. Traverse your graph

def earliest_ancestor(ancestors, starting_node):
    '''
    Write a function that, given the dataset and the ID of an 
    individual in the dataset returns their earliest known ancestor – 
    the one at the farthest distance from the input individual. 
    
    If there is more than one ancestor tied for "earliest", return 
    the one with the lowest numeric ID.
    
    If the input individual has no parents, the function should return -1.
    '''
    # depth first searching from child to parent for longest path
    # create a STACK
    s = Stack()
    # push the tuple of the starting node and path length
    s.push((starting_node, 0))
    # create a list for storing (node, path_length) tuples
    visited_ancestors = []
    # while the stack is not empty...
    while s.size() > 0:
        # pop the first tuple
        temp = s.pop()
        # do the thing:
        # check if there are any parents to the last element
        for pair in ancestors:
            if pair[1] == temp[0]:
                # add tuple with parent and path length
                new_ancestor = pair[0]
                path_length = temp[1] + 1
                visited_ancestors.push((new_ancestor, path_length))
            # Add pat
            print(temp)
            visited.add(temp)
            # push all it's neighbors
            for neighbor in self.get_neighbors(temp):
                s.push(neighbor)
    return visited