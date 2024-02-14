import argparse
import os
import shutil
import json
from pyvis.network import Network

class Node:
    _id_gen = 0
    def __init__(self, data):
        Node._id_gen += 1
        self._uid = Node._id_gen
        self._data = data
        self.children = dict()
    
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

def build_call_tree(curr):
    curr_node = Node(data=methods[curr['id']])
    for child in curr['children']:
        curr_node.add_child(build_call_tree(child))
    return curr_node

def build_context_tree(curr):  
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
    
    ct_root = build_call_tree(curr)
    ct_root = prune_call_tree(ct_root, set())
    process_recursions(ct_root, dict())
    return ct_root

def visualize(curr_node, name, max_depth=1000000000, max_edges=1000000000, show=False):
    visited = set()
    edge_count = 0
    def populate(curr_node, depth):
        nonlocal edge_count
        if curr_node.get_uid() in visited:
            return
        if depth > max_depth:
            return
        visited.add(curr_node.get_uid())
        color = 'blue'#'blue' if curr_node.get_id() == root['id'] else 'red'
        net.add_node(
            n_id=curr_node.get_uid(), 
            label=curr_node.get_label(), 
            color=color,
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

    options="""const options = {
                "physics": {
                    "repulsion": {
                    "centralGravity": 0.3,
                    "springLength": 100,
                    "springConstant": 0.15,
                    "nodeDistance": 140,
                    "damping": 0.15
                    },
                    "maxVelocity": 119,
                    "minVelocity": 0.69,
                    "solver": "repulsion",
                    "wind": {
                    "y": 5
                    }
                },
                "interaction": {"hover": true}
            }"""
    net.set_options(options)
    # net.show_buttons(filter_=['physics'])
    populate(curr_node, 0)
    net.save_graph(name)
    if show:
        net.show(name, notebook=False)
    
    
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
    parser.add_argument('--out', '-o', type=str, default='vis.html', help='output (.html) file containing call graph visualization.')    
    parser.add_argument('--ref', '-r', type=str, default='ref.html', help='reference (.html) file containing custom javascript to inject.')    
    parser.add_argument('--type', '-t', type=str, default='cct', help=f'type of visualization to generate, valid options: {VIS_TYPES}.')
    parser.add_argument('--maxDepth', '-D', type=int, default=1000000000, help=f'max depth in call graph data to visualize.')    
    parser.add_argument('--maxEdges', '-E', type=int, default=1000000000, help=f'max edges in call graph to visualize.')    

    args = parser.parse_args()
    out_dir = 'out'
    if os.path.isdir(out_dir) == False:
        os.mkdir(out_dir) 
    with open(f'{args.input}', 'r') as f:
        data = json.load(f)
    methods = {m['id']: m for m in data['methods']}
    paths = data['paths']
    root = paths[0]
    if args.type not in VIS_TYPES:
        print(f'Invalid visualization type: {args.type}')
    json_name = args.input.split('.json')[0]
    base_html = f'{out_dir}/{args.type}-base-{args.out}'
    out_html = f'{out_dir}/{args.type}-{args.out}'
    visualize(VIS_TYPES[args.type](root), base_html, args.maxDepth, args.maxEdges, show=False)
    # move lib/ directory to out/ folder
    p = os.path.dirname(os.path.abspath(__file__))
    if os.path.isdir(f'{out_dir}/lib'):
        shutil.rmtree(f'{out_dir}/lib')
    os.rename('lib', f'{out_dir}/lib')
    inject_custom_javascript(base_html, args.ref, out_html)
    print(f'base: {base_html}')
    print(f'out: {out_html}')
    