import argparse
import os
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
        label = f"{self._data['classPath']}.{self._data['methodName']}"
        # label = str(self._data['id'])
        # label = self._data['classPath']
        return label


def build_call_tree(curr):
    curr_node = Node(data=methods[curr['id']])
    for child in curr['children']:
        curr_node.add_child(build_call_tree(child))
    return curr_node

def build_context_tree(curr):  
    # TODO: Fix recursion preprocessing bug
    # - occurs when recursion is not just a method calling itself
    #   but rather a method earlier in the exec path

    # def process_recursions(curr_node, path):
    #     if curr_node in path:
    #         print('rec found!')
    #         # 

    #     path[curr_node.get_id()] = curr_node
    #     for child_node in curr_node.get_children():
    #         process_recursions(child_node, path)
    #     path.pop(curr_node.get_id())
    
    def prune_call_tree(curr_node):
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
            if len(dups[k]['nonleaf']) == 0:
                continue
            first = dups[k]['nonleaf'][0]
            for i in range(1, len(dups[k]['nonleaf'])):
                sybling = dups[k]['nonleaf'][i]
                # absorb child from sybling
                for nephew_node in sybling.get_children():
                    first.add_child(nephew_node)
                # remove sybling from parent
                curr_node.remove_child(sybling)
        return curr_node
    
    ct_root = build_call_tree(curr)
    # process_recursions(ct_root, dict())
    return prune_call_tree(ct_root)

def visualize(curr_node, name, show=False):
    def populate(curr_node):
        color = 'blue' if curr_node.get_id() == root['id'] else 'red'
        net.add_node(
            n_id=curr_node.get_uid(), 
            label=curr_node.get_label(), 
            color=color,
            physics=False)
        for child_node in curr_node.get_children():
            populate(child_node)
            net.add_edge(curr_node.get_uid(), child_node.get_uid(), color='black', physics=False)
    net = Network(height="1000px", width="100%", directed=True)
    options = """options = {
        "physics": {
            "enabled": false,
            "minVelocity": 0.75
        }
    }"""
    net.set_options(options)
    populate(curr_node)
    # net.show_buttons(filter_=['physics'])
    if show:
        net.show(name, notebook=False)
    else:
        net.save_graph(name)


def inject_custom_javascript(base_html, ref_html, out_html, START_TOKEN='CUSTOM START ###', END_TOKEN='CUSTOM END ###'):
    ref_html_content = None
    target_html_content = None
    # extract custom javascript from ref_html based on START_TOKEN and END_TOKEN
    with open(ref_html,'r') as f:
        ref_html_content = f.readlines()
    i = 0
    start_index = 0
    ref_inject_ref = i
    # find start of custom javascript
    while i < len(ref_html_content) and START_TOKEN not in ref_html_content[i]: 
        if len(ref_html_content[i].strip()) > 0:
            ref_inject_ref = i
        i+=1
    start_index = i
    # find end of custom javascript
    while i < len(ref_html_content) and END_TOKEN not in ref_html_content[i]: 
        i+=1
    if start_index >= i:
        print(f'Error: could not find {START_TOKEN} and {END_TOKEN} in {ref_html}!')
        return
    custom_javascript = ref_html_content[start_index:i+1]
    # locate proper insert position in target_html
    with open(base_html, 'r') as f:
        base_html_content = f.readlines()
        inject_ref = -1
        for i in range(len(base_html_content)):
            if base_html_content[i].strip() == ref_html_content[ref_inject_ref].strip():
                inject_ref = i
                break
        if inject_ref == -1:
            print(f'Error: could not locate injection reference point: \n {ref_html_content[ref_inject_ref].strip()}')
            return 
        base_html_content = base_html_content[:inject_ref+1] + custom_javascript + base_html_content[inject_ref+1:]
    with open(out_html, 'w') as f:
        f.writelines(base_html_content)
    


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
    visualize(VIS_TYPES[args.type](root), base_html)
    inject_custom_javascript(base_html, args.ref, out_html)