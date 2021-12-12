from typing import TextIO, List, Dict, Tuple
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

def already_double_visited_small_node(visited:Dict[Node, int]):
    ret = sum([1 for node, visit_count in visited.items() if not node.is_big and visit_count>1])
    return ret>1

def go(adjacency_list: Dict[Node, List[Node]], path_to_here: List[Node], end: Node, paths: List[List[Node]], visited:Dict[Node, int]):
    current_node = path_to_here[-1]
    adjacents = adjacency_list[current_node]
    for node in adjacents:
        next_visited = visited.copy()
        next_visited[node] += 1
        next_path = list(path_to_here)
        next_path.append(node)

        if node == start:
            continue

        if node == end:
            paths.append(next_path)
        
        elif node.is_big:
            # Can always visit big nodes
            go(adj, next_path, end, paths, next_visited)

        elif visited[node] == 0:
            # Can always visit small nodes if they haven't been visited before
            go(adj, next_path, end, paths, next_visited)
        
        elif not already_double_visited_small_node(visited):
            go(adj, next_path, end, paths, next_visited)

adj, start, end = read_input(sys.stdin)
paths = []
visited = defaultdict(lambda:0)
visited[start] = 2
go(adj, [start], end, paths, visited)
print(len(paths))
# print_paths(paths)
