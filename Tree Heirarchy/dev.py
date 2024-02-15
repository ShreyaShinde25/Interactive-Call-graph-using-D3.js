import argparse
import os
import shutil
import json
from pyvis.network import Network

class Node:
    _id_gen = 0
    def __init__(self, data, size):
        Node._id_gen += 1
        self._uid = Node._id_gen
        self._data = data
        self.children = dict()
        self._size = size
        

    def get_uid(self):
        return self._uid

    def get_depth(self):
        return self.depth

    def add_child(self, child):
        self.children[child.get_uid()] = child
    
    def remove_child_by_uid(self, uid: int):
        if uid in self.children:
            self.children.pop(uid)

    def remove_child(self, child):
        self.remove_child_by_uid(child.get_uid())

    def get_children(self):
        return self.children.values()
    
    def get_child(self, uid):
        if uid not in self.children:
            return None
        return self.children[uid]

    def get_id(self):
        return self._data['id']
    
    def get_label(self):
        label = f"{self._data['classPath'].split('.')[-1]}.{self._data['methodName']}"
        # label = str(self._data['id'])
        # label = self._data['classPath']
        return label

    def get_title(self):
        return f"{self._data['classPath']}.{self._data['methodName']}"
    
    def get_size(self):
        return self._size

def build_call_tree(curr, method_map, size_map):
    curr_node = Node(data=method_map[curr['id']], size=size_map[curr['id']])
    for child in curr['children']:
        curr_node.add_child(build_call_tree(child, method_map, size_map))
    return curr_node

def build_context_tree(curr, method_map, size_map):  
    # TODO: Fix recursion preprocessing bug
    # - occurs when recursion is not just a method calling itself
    #   but rather a method earlier in the exec path

    def process_recursions(curr_node, path):
        path[curr_node.get_id()] = curr_node
        delete_uids = list()
        add_targets = list()
        child_nodes = list(curr_node.get_children())
        for child_node in child_nodes:
            if child_node.get_id() in path and curr_node.get_child(child_node.get_uid()) is not None:
                # print(f'found recursion from {curr_node.get_label()} to {child_node.get_label()}')
                curr_node.remove_child(child_node)
                for grand_child_node in child_node.get_children():
                    path[child_node.get_id()].add_child(grand_child_node) 
                curr_node.add_child(path[child_node.get_id()])                
            else:
                process_recursions(child_node, path)
        # for uid in delete_uids:
        #     child_node = curr_node.get_child(uid)
        #     curr_node.remove_child_by_uid(uid)
        #     if child_node is None:
        #         continue
        #     for grand_child_node in child_node.get_children():
        #             path[child_node.get_id()].add_child(grand_child_node) 
        # for child in add_targets:
        #     curr_node.add_child(child)
        path.pop(curr_node.get_id())
    
    def prune_call_tree(curr_node, visited):
        if curr_node.get_uid() in visited:
            return
        visited.add(curr_node.get_uid())
        # print(f'pruning {curr_node.get_label()}...')
        dups = {}
        # collect duplicates
        for child_node in curr_node.get_children():
            if child_node.get_id() not in dups:
                dups[child_node.get_id()] = {'leaf': list(), 'nonleaf': list()}
            
            if len(child_node.children) == 0:
                dups[child_node.get_id()]['leaf'].append(child_node)
            else:
                dups[child_node.get_id()]['nonleaf'].append(child_node)

        # prune duplicates
        for k in dups:
            for i in range(1, len(dups[k]['leaf'])):
                # remove duplicate leaf
                curr_node.remove_child(dups[k]['leaf'][i])
                # print(f'remove: {child_node.get_label()} from {curr_node.get_label()}')
            if len(dups[k]['nonleaf']) == 0:
                continue
            first = dups[k]['nonleaf'][0]
            for i in range(1, len(dups[k]['nonleaf'])):
                sybling = dups[k]['nonleaf'][i]
                # absorb child from sybling
                for nephew_node in sybling.get_children():
                    first.add_child(nephew_node)
                    # print(f'absorb: {nephew_node.get_label()} from {sybling.get_label()} in {first.get_label()}')
                # remove sybling from parent
                curr_node.remove_child(sybling)
                # print(f'remove: {child_node.get_label()} from {curr_node.get_label()}')
        
        # prune lower level
        for child_node in curr_node.get_children():
            prune_call_tree(child_node, visited)
        return curr_node
    
    ct_root = build_call_tree(curr, method_map, size_map)
    ct_root = prune_call_tree(ct_root, set())
    process_recursions(ct_root, dict())
    return ct_root

def visualize(root_list, file_name, max_depth=1000000000, max_edges=1000000000, show=False):
    visited = set()
    edge_count = 0
    def populate(curr_node, depth):
        nonlocal edge_count
        if curr_node.get_uid() in visited:
            return
        if depth > max_depth:
            return
        visited.add(curr_node.get_uid())
        color = 'blue'
        net.add_node(
            n_id=curr_node.get_uid(), 
            label=curr_node.get_label(), 
            color=color,
            size=curr_node.get_size(),
            title=str(len(curr_node.get_children())))
            
        for child_node in curr_node.get_children():
            populate(child_node, depth+1)
            if child_node.get_uid() in visited:
                net.add_edge(curr_node.get_uid(), 
                             child_node.get_uid(), 
                             color='gray')
                edge_count += 1
                if edge_count >= max_edges:
                    return
    net = Network(height="1000px", width="100%", directed=True, filter_menu=True, select_menu=False)
    # options can be generated from: https://visjs.github.io/vis-network/examples/network/physics/physicsConfiguration.html
    options = """
        const options = {
            "layout": {
                "improvedLayout":true,
                "clusterThreshold": 150,
                "hierarchical": {
                    "enabled": true,
                    "levelSeparation": 150,
                    "nodeSpacing": 200,
                    "treeSpacing": 200,
                    "blockShifting": true,
                    "edgeMinimization": true,
                    "parentCentralization": true,
                    "direction": "UD",        
                    "sortMethod": "hubsize",  
                    "shakeTowards": "roots"  
                }
            },
            "edges": {
                "hoverWidth": 0,
                "selectionWidth": 0,
                "width": 1
            },
            "interaction": {"hover": true}
        }
    """
    net.set_options(options)
    # net.show_buttons(filter_=['physics'])
    for root_node in root_list:
        populate(root_node, 0)
    net.save_graph(file_name)
    if show:
        net.show(file_name, notebook=False)
    
    
def inject_custom_javascript(base_html, ref_html, out_html, START_TOKEN='CUSTOM START ###', END_TOKEN='CUSTOM END ###'):
    ref_html_content = None
    # extract custom javascript from ref_html based on START_TOKEN and END_TOKEN
    with open(ref_html,'r') as f:
        ref_html_content = f.readlines()
    with open(base_html, 'r') as f:
        base_html_content = f.readlines()
    right = 0
    left = 0
    ref_inject_ref = 0
    base_inject_ref = -1
    n = len(ref_html_content)
    while right < n:
        # find start of custom javascript
        while right < len(ref_html_content) and START_TOKEN not in ref_html_content[right]: 
            if len(ref_html_content[right].strip()) > 0:
                ref_inject_ref = right
            right+=1
        left = right
        # find end of custom javascript
        while right < len(ref_html_content) and END_TOKEN not in ref_html_content[right]: 
            right+=1
        if left >= right:
            # print(f'Error: could not find {START_TOKEN} and {END_TOKEN} in {ref_html}!')
            break
        custom_javascript = ref_html_content[left:right+1]
        # locate proper insert position in target_html
        for i in range(len(base_html_content)):
            if base_html_content[i].strip() == ref_html_content[ref_inject_ref].strip():
                base_inject_ref = i
                break
        if base_inject_ref == -1:
            # print(f'Error: could not locate injection reference point: \n {ref_html_content[ref_inject_ref].strip()}')
            break
        base_html_content = base_html_content[:base_inject_ref+1] + custom_javascript + base_html_content[base_inject_ref+1:]
        right += 1  
    with open(out_html, 'w') as f:
        f.writelines(base_html_content)
    return 0 


if __name__ == "__main__":
    VIS_TYPES = {
        'cct': build_context_tree, 
        'ct': build_call_tree, 
        'cg': None, #TODO: implement generating call graph
    }
    parser = argparse.ArgumentParser(description='Script for generating customizable call graph visualizations using pyvis.')
    parser.add_argument('--input', '-i', type=str, required=True, help='input (.json) file to process with call graph info.') 
    parser.add_argument('--out', '-o', type=str, default='', help='output (.html) file containing call graph visualization.')    
    parser.add_argument('--ref', '-r', type=str, default='ref.html', help='reference (.html) file containing custom javascript to inject.')    
    parser.add_argument('--type', '-t', type=str, default='cct', help=f'type of visualization to generate, valid options: {VIS_TYPES}.')
    parser.add_argument('--maxDepth', '-D', type=int, default=1000000000, help=f'max depth in call graph data to visualize.')    
    parser.add_argument('--maxEdges', '-E', type=int, default=1000000000, help=f'max edges in call graph to visualize.')    
    parser.add_argument('--sizeKey', '-k', type=str, default='methodSize', help=f'default key form metrics list to determine node size in visualization.')    

    args = parser.parse_args()
    if args.type not in VIS_TYPES:
        print(f'Invalid visualization type: {args.type}')
    out_dir = 'out'
    if os.path.isdir(out_dir) == False:
        os.mkdir(out_dir) 
    # load json data
    with open(f'{args.input}', 'r') as f:
        data = json.load(f)
    METHODS = {m['id']: m for m in data['methods']}
    PATHS = data['paths']
    # calculate the node size for each method based on args.sizeKey
    min_size = float('inf')
    max_size = -float('inf')
    NODE_SIZE = dict()
    for k in METHODS:
        for metric_entry in METHODS[k]['metrics']:
            if metric_entry['key'] == args.sizeKey:
                NODE_SIZE[k] = metric_entry['value']
                min_size = min(min_size, NODE_SIZE[k])
                max_size = max(max_size, NODE_SIZE[k])
                break

    # scale node sizes (node with smallest size should have 
    # the default display size)
    MAX_DISPLAY_SIZE = 50
    for k in NODE_SIZE:
        NODE_SIZE[k] = MAX_DISPLAY_SIZE * (NODE_SIZE[k])/max_size

    # configure file names    
    base_html = f'{out_dir}/{args.type}-base-{args.out}'
    out_html = f'{out_dir}/{args.type}-{args.out}'
    if args.out == '':
        json_name = args.input.split('/')[-1].split('.json')[0]
        base_html = f'{out_dir}/{args.type}-base-{json_name}.html'
        out_html = f'{out_dir}/{args.type}-{json_name}.html'
    print(f'parsing: {args.input}...')
    root_list = list()
    # build data strcture in python 
    for root in PATHS:
        # build for each starting method
        root_node = VIS_TYPES[args.type](root, METHODS, NODE_SIZE)
        root_list.append(root_node)
    print(f'generating: {base_html}...')
    # create vis.js output
    visualize(
        root_list=root_list, 
        file_name=base_html, 
        max_depth=args.maxDepth, 
        max_edges=args.maxEdges, 
        show=False)
    # move lib/ directory to out/ folder
    p = os.path.dirname(os.path.abspath(__file__))
    if os.path.isdir(f'{out_dir}/lib'):
        shutil.rmtree(f'{out_dir}/lib')
    os.rename('lib', f'{out_dir}/lib')
    # inject custom javascript from args.ref
    print(f'generating: {out_html}...')
    inject_custom_javascript(base_html, args.ref, out_html)
    print('generated:')
    print(f'- {base_html}')
    print(f'- {out_html}')
    