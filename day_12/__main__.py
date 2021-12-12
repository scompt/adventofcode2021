from typing import TextIO, List, Dict, Tuple, Set
import sys
from collections import namedtuple, defaultdict

Point = namedtuple("Point", ['x', 'y'])
Node = namedtuple("Node", ['name', 'is_big'])

def make_node(nodes:Dict[str, Node], name: str) -> Node:
    if name in nodes:
        return nodes[name]

    node = Node(name=name, is_big=name.isupper())
    nodes[name] = node
    return node

def read_input(textio: TextIO) -> Tuple[Dict[Node, List[Node]], Node, Node]:
    nodes = dict()
    start = end = None
    adjacency_list = defaultdict(list)
    lines = textio.readlines()
    
    for line in lines:
        from_node, to_node = (make_node(nodes, name) for name in line.strip().split('-'))
        adjacency_list[from_node].append(to_node)
        adjacency_list[to_node].append(from_node)
        
        if from_node.name == 'start' and not start:
            start = from_node
        if to_node.name == 'end' and not end:
            end = to_node

    return adjacency_list, start, end

def print_paths(paths):
    for path in paths:
        print(','.join(node.name for node in path))
            
def go(adjacency_list: Dict[Node, List[Node]], path_to_here: List[Node], end: Node, paths, visited):
    current_node = path_to_here[-1]
    adjacents = adjacency_list[current_node]
    for node in adjacents:
        if not node.is_big and node in visited:
            continue
        
        next_visited = visited.copy()
        next_visited.add(node)
        next_path = list(path_to_here)
        next_path.append(node)

        if node == end:
            paths.append(next_path)
        else:
            go(adj, next_path, end, paths, next_visited)

adj, start, end = read_input(sys.stdin)
paths = []
go(adj, [start], end, paths, set([start]))
print(len(paths))
# print_paths(paths)
