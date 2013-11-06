# Frank Chemotti fchemotti@gmail.com
# collect data about google keyboard's next word prediction

import json
from itertools import chain

def print_set(s):
    """Print a set of strings, sorted, on one line, space-delimited."""
    l = list(s)
    l.sort()
    print ' '.join(l)

def print_list(l):
    """Print a list of strings, on one line, space-delimited."""
    print ' '.join(l)

def read_file(fname):
    """Read and return JSON dictionary.

    Keys must be strings.
    Values must be lists of strings.
    Unicode will be encoded using UTF-8."""     
    f = open(fname, 'r')
    dgraph = json.loads(f.read())
    f.close()
    dgraph = {key.encode('utf-8') : [word.encode('utf-8') for word in words]
             for (key, words) in dgraph.items()}
    return dgraph

def input_words(dgraph):
    """Add nodes to and return the word network, with user input.

    dgraph is a dict where each key is a string,
    and each value is a list of 3 strings.
    Input should be a list of 4 words separated by spaces.
    The first word is the key (node), and the remaining 3 words
    are the words predicted to follow the key (outgoing links).
    To facilitate creation of a closed network,
    any words that appear in the network as outgoing links
    but do not yet have their own node
    are printed immediately before the prompt."""
    text = ''
    one = ''
    two = ''
    thr = ''
    while text is not 'q':
        keys = set(dgraph.keys())
        words = set(chain.from_iterable(dgraph.values()))
        notkeys = words - keys
        if one in notkeys: print one
        elif two in notkeys: print two
        elif thr in notkeys: print thr
        else: print_set(notkeys)

        text = raw_input('enter the four words, or q to quit: ')
        words = text.split()
        if len(words) == 4:
            current, one, two, thr = words
            if current in dgraph:
                print 'duplicate'
            else:
                dgraph[current] = [one, two, thr]
    return dgraph

def write_json(fname, dgraph):
    """Output the word network dgraph to file fname as a JSON dictionary."""
    f = open(fname, 'w')
    f.write(json.dumps(dgraph))
    f.close()

def write_graphml(fname, dgraph):
    """INCOMPLETE: Output a graphML object."""
    f = open(fname, 'w')
    pass
    f.close()
##example graphml
##<?xml version="1.0" encoding="UTF-8"?>
##<graphml xmlns="http://graphml.graphdrawing.org/xmlns"  
##    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
##    xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
##     http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
##  <graph id="G" edgedefault="directed">
##    <node id="n0"/>
##    <node id="n1"/>
##    <node id="n2"/>
##    <node id="n3"/>
##    <node id="n4"/>
##    <node id="n5"/>
##    <node id="n6"/>
##    <node id="n7"/>
##    <node id="n8"/>
##    <node id="n9"/>
##    <node id="n10"/>
##    <edge source="n0" target="n2"/>
##    <edge source="n1" target="n2"/>
##    <edge source="n2" target="n3"/>
##    <edge source="n3" target="n5"/>
##    <edge source="n3" target="n4"/>
##    <edge source="n4" target="n6"/>
##    <edge source="n6" target="n5"/>
##    <edge source="n5" target="n7"/>
##    <edge source="n6" target="n8"/>
##    <edge source="n8" target="n7"/>
##    <edge source="n8" target="n9"/>
##    <edge source="n8" target="n10"/>
##  </graph>
##</graphml>

def closure_of(dgraph, node):
    """Return the set of nodes that forms the closure of node in dgraph."""
    if node not in dgraph.keys():
        return None
    part_closure = set([node])
    while True:
        add_nodes = set()
        for key in part_closure:
            for next_node in dgraph[key]:
                add_nodes.add(next_node)
        if add_nodes <= part_closure:
            closure = part_closure
            break
        part_closure = part_closure | add_nodes
    return closure

def find_closed_subgraph(dgraph):
    """Return a proper closed subset of nodes, if one exists."""
    nodes = set(dgraph.keys())
    for node in nodes:
        c = closure_of(dgraph, node)
        if not c == nodes:
            return c
    return None

def find_orphans(dgraph):
    """Return a set of nodes that do not appear as outgoing links."""
    nodes = set(dgraph.keys())
    children = set(chain.from_iterable(dgraph.values()))
    return nodes - children

def get_path(dgraph, init_node, edge_index_list):
    """Return a list of nodes for the specified path on dgraph.

    dgraph represents a closed directed graph.
    init_node is the starting node of the path.
    edge_index_list specifies which outgoing edge to follow from each node.
    """
    sequence = [init_node]
    for e in edge_index_list:
        sequence.append(dgraph[sequence[-1]][e])
    return sequence

def find_terminal_loop(dgraph, init_node, edge_index_loop):
    """Return the terminal cycle of nodes for the infinite path specified."""
    n = len(edge_index_loop)
    sequence = [init_node]
    while True:
        index = (len(sequence) - 1) % n
        next_node = dgraph[sequence[-1]][edge_index_loop[index]]
        if (next_node in sequence):
            index_of_match = sequence.index(next_node)
            next_index = len(sequence)
            if index_of_match % n == next_index % n:
                return sequence[index_of_match:]
        sequence.append(next_node)

def run_until_loop4(dgraph, init_node, edge_index_loop):
    """Return the path of nodes specified, ending after it repeats 4 times."""
    n = len(edge_index_loop)
    first_node = dgraph[init_node][edge_index_loop[0]]
    sequence = [first_node]
    while True:
        edge_index = len(sequence) % n
        next_node = dgraph[sequence[-1]][edge_index_loop[edge_index]]
        if next_node in sequence:
            next_index = len(sequence)
            index_of_match = sequence.index(next_node)
            while (index_of_match % n != next_index % n):
                try:
                    index_of_match = sequence.index(next_node, index_of_match + 1)
                except ValueError:
                    break
            if index_of_match % n == next_index % n:
                node_list = sequence[:index_of_match] + 4 * sequence[index_of_match:]
##                lead_in = ' '.join(sequence[:index_of_match])
##                loop = ' '.join(sequence[index_of_match:])
##                blank_lead = ' ' * len(lead_in)
##                print lead_in + ' &' + loop + '\\\\'
##                print ' &' + loop + '\\\\'
##                print ' &' + loop + '\\\\'
##                print ' &' + loop + '\\\\'
                return node_list
        sequence.append(next_node)

def cycle(loop):
    """Return cycled version of loop with a minimal element first."""
    # ideally would return lexicographically minimal cycle
    # but that's more difficult
    # would have to find all occurrences of min element
    # and determine which leads to lex'ly min cycle
    # could do by concatenation for strings, but not so good for other types
    index_of_least = loop.index(min(loop))
    return loop[index_of_least:] + loop[:index_of_least]

def all_loops(dgraph, edge_index_loop):
    """Return a complete list of distinct loops using edge_index_loop."""
    loops = []
    for init in dgraph.keys():
        loop = cycle(find_terminal_loop(dgraph, init, edge_index_loop))
        if loop not in loops:
            loops.append(loop)
    return loops

def loop_poem(dgraph, init, cycles):
    """Return a list of words using run_until_loop4 for all cycles."""
    poem = [init]
    for cycle in cycles:
        chunk = run_until_loop4(dgraph, poem[-1], cycle)
        poem = poem + chunk
    return poem
        
dgraph = read_file('base91.json')

##cycles = [[0], [1], [2],
##          [0,1], [0,2], [1,2],
##          [0,0,1], [0,0,2], [0,1,1], [0,1,2], [0,2,1], [0,2,2], [1,1,2], [1,2,2],
##          [0,0,0,1], [0,0,0,2], [0,0,1,1], [0,0,1,2], [0,0,2,1], [0,0,2,2],
##          [0,1,0,2], [0,1,1,1], [0,1,1,2], [0,1,2,1], [0,1,2,2], [0,2,1,1],
##          [0,2,1,2], [0,2,2,1], [0,2,2,2], [1,1,1,2], [1,1,2,2], [1,2,2,2]]

cycles = [[2], [1], [0],
          [2,1], [2,0], [1,0],
          [2,2,1], [2,2,0], [2,1,1], [2,1,0], [2,0,1], [2,0,0], [1,1,0], [1,0,0],
          [2,2,2,1], [2,2,2,0], [2,2,1,1], [2,2,1,0], [2,2,0,1], [2,2,0,0],
          [2,1,2,0], [2,1,1,1], [2,1,1,0], [2,1,0,1], [2,1,0,0], [2,0,1,1],
          [2,0,1,0], [2,0,0,1], [2,0,0,0], [1,1,1,0], [1,1,0,0], [1,0,0,0]]



    
