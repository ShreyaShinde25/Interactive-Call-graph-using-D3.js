import argparse
import os
import shutil
import json
from collections import defaultdict
from pyvis.network import Network

class Node:
    _id_gen = 0
    MAX_LABEL_SIZE = 15
    def __init__(self, data, size):
        Node._id_gen += 1
        self._uid = Node._id_gen
        self._data = data
        self.children = dict()
        self._size = size
        self._metrics = {}
        for entry in self._data['metrics']:
            self._metrics[entry['key']] = float(entry['value']) if entry['value'] else None
        

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
        label = f"{self._data['className'].split('.')[-1]}.{self._data['methodName']}"
        # label = str(self._data['id'])
        # label = self._data['className']
        if len(label) > Node.MAX_LABEL_SIZE:
            label = label[:min(Node.MAX_LABEL_SIZE, len(label))]
            label += '..' if label[-1] == '.' else '...'
        return label

    def get_title(self):
        return "\n".join([
            f"signature: {self._data['className']}.{self._data['methodName']}{self._data['methodDescriptor']}",
            f"callees: {len(self.children)}",
            f"methodSize: {self._metrics['methodSize']} bytecode size"
        ])
        
    def get_size(self):
        return self._size

def build_call_tree(curr, method_map, size_map):
    curr_node = Node(data=method_map[curr['id']], size=size_map[curr['id']])
    for child in curr['children']:
        curr_node.add_child(build_call_tree(child, method_map, size_map))
    return curr_node

def build_call_graph(curr, method_map, size_map, existing_nodes={}):
    curr_node = None
    if curr['id'] in existing_nodes:
        curr_node = existing_nodes[curr['id']]
    else:
        curr_node = Node(data=method_map[curr['id']], size=size_map[curr['id']])
        existing_nodes[curr['id']] = curr_node 

    for child in curr['children']:
        child_node = build_call_graph(child, method_map, size_map, existing_nodes)
        curr_node.add_child(child_node)
    return curr_node


def build_context_tree(curr, method_map, size_map):  
    # NOTE: based on the paper https://dl.acm.org/doi/pdf/10.1145/258916.258924
    # two nodes v and w in a call tree are equivalent iff:
    # - v and w represent the same procedure
    # - if any of the following are true:
    #   (1) the tree parent of v is equivalent to the tree parent of w,
    #   (2) v === w (this case is trivial; i.e. no need to handle?)
    #   (3) there is a vertex u such that u represents the same procedure 
    #       as v and w, and u is an ancestor of both v and w (here, a vertex 
    #       is an ancestor of itself)
    def prune_call_tree(curr_node, prev_node, path: dict, visited: set):
        if curr_node.get_id() in path:  
            ancestor_node = path[curr_node.get_id()]
            if ancestor_node:
                # handle case (3) above
                # have ancestor node adopt all of current node's children
                for child_node in curr_node.get_children():
                    ancestor_node.add_child(child_node)
                if prev_node:
                    # remove edge from previous node to current node
                    prev_node.remove_child(curr_node)
                    # add back edge between prev_node and ancestor node
                    prev_node.add_child(ancestor_node)
            return 1
        prune_count = 0
        # add uid to visited so that we don't visit the same node repeated
        visited.add(curr_node.get_uid())
        # register current node in path; in case we run into an equivalent node later
        path[curr_node.get_id()] = curr_node
        # print(f'pruning {curr_node.get_label()}...')
        dups = defaultdict(list)
        # collect duplicates
        for child_node in curr_node.get_children():
            if child_node.get_uid() in visited:
                continue # skip since we already added a back edge this child node
            dups[child_node.get_id()].append(child_node)
        # handle case (1) above
        for method_id in dups:
            first = dups[method_id][0]
            for i in range(1, len(dups[method_id])):
                sybling = dups[method_id][i]
                # adopt children from equivalent sybling
                for nephew_node in sybling.get_children():
                    first.add_child(nephew_node)
                    # print(f'adopt: {nephew_node.get_label()} from {sybling.get_label()} in {first.get_label()}')
                # remove sybling from parent
                curr_node.remove_child(sybling)
                # print(f'pruned: {child_node.get_label()} from {curr_node.get_label()}')
                prune_count += 1
            prune_count += prune_call_tree(first, curr_node, path, visited)
        # unregister current node from path
        path.pop(curr_node.get_id())
        return prune_count
    # build call tree first
    ct_root = build_call_tree(curr, method_map, size_map)
    # repeatedly prune call tree until there is only 1 copy of each equivalent node from the call tree
    while prune_call_tree(ct_root, None, dict(), set()) > 0:
        pass
    return ct_root


# method to visualize call graph
def visualize_call_tree(methods, node_sizes, paths, file_name, max_depth=1000000000, max_edges=1000000000, show=False):
    visited = set()
    edge_count = 0

    def populate(net, curr_node, depth):
        nonlocal edge_count
        if curr_node['id'] in visited:
            return
        if depth > max_depth:
            return
        visited.add(curr_node['id'])
        net.add_node(
            n_id=curr_node['id'],
            title=f"{methods[curr_node['id']]['methodName']}\nSize: {node_sizes[curr_node['id']]}",
            size=node_sizes[curr_node['id']],
            label=methods[curr_node['id']]['methodName']
        )
        for child_node in curr_node.get('children', []):
            populate(net, child_node, depth + 1)
            if child_node['id'] in visited:
                net.add_edge(curr_node['id'], child_node['id'])
                edge_count += 1
                if edge_count >= max_edges:
                    return

    net = Network(height="1000px", width="100%", directed=True, filter_menu=False, select_menu=False)
    with open(args.option, 'r') as f:
        options_data = json.load(f)
    options = f'''const options = {json.dumps(options_data, indent=1)}''' 
    net.set_options(options)

    for root_node_data in paths:
        populate(net, root_node_data, 0)

    net.save_graph(file_name)

    if show:
        net.show(file_name, notebook=False)






def visualize(root_list, file_name, max_depth=1000000000, max_edges=1000000000, show=False):
    visited = set()
    edge_count = 0
    def populate(curr_node, depth):
        # print(curr_node.get_id())
        nonlocal edge_count
        if curr_node.get_uid() in visited:
            return
        if depth > max_depth:
            return
        visited.add(curr_node.get_uid())
        net.add_node(
            n_id=curr_node.get_uid(), 
            label=curr_node.get_label(), 
            size=curr_node.get_size(),
            title=curr_node.get_title())
        for child_node in curr_node.get_children():
            populate(child_node, depth+1)
            if child_node.get_uid() in visited:
                net.add_edge(curr_node.get_uid(), child_node.get_uid())
                edge_count += 1
                if edge_count >= max_edges:
                    return
    net = Network(height="1000px", width="100%", directed=True, filter_menu=False, select_menu=False)
    # options can be generated from: https://visjs.github.io/vis-network/examples/network/physics/physicsConfiguration.html
    # TODO: instead of hard-coding values, we should load these options
    #       automatically from some .json file and generate the 'options' 
    #       string below
    with open(args.option, 'r') as f:
        options_data = json.load(f)
    options = f'''const options = {json.dumps(options_data, indent=1)}''' 
    net.set_options(options)
    # net.show_buttons(filter_=['physics'])
    for root_node in root_list:
        populate(root_node, 0)
    net.save_graph(file_name)
    if show:
        net.show(file_name, notebook=False)
    
    
def inject_custom_code(base_html, ref_html, out_html, 
        START_TOKEN='CUSTOM START', END_TOKEN='CUSTOM END'):
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
        'cg':build_call_graph
    }
    parser = argparse.ArgumentParser(description='Script for generating customizable call graph visualizations using pyvis.')
    parser.add_argument('--input', '-i', type=str, required=True, help='input (.json) file to process with call graph info.') 
    parser.add_argument('--out', '-o', type=str, default='', help='output (.html) file containing call graph visualization.')    
    parser.add_argument('--ref', '-r', type=str, default='ref.html', help='reference (.html) file containing custom javascript to inject.')    
    parser.add_argument('--type', '-t', type=str, default='cct', help=f'type of visualization to generate, valid options: {VIS_TYPES}.')
    parser.add_argument('--maxDepth', '-D', type=int, default=1000000000, help=f'max depth in call graph data to visualize.')    
    parser.add_argument('--maxEdges', '-E', type=int, default=1000000000, help=f'max edges in call graph to visualize.')    
    parser.add_argument('--sizeKey', '-k', type=str, default='methodSize', help=f'default key form metrics list to determine node size in visualization.')
    parser.add_argument('--option', '-c',type=str, default='options.json', help=f'options file to make visualization configurations.')    
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
    visit=set()
    for k in METHODS:
        for metric_entry in METHODS[k]['metrics']:
            if metric_entry['key'] == args.sizeKey:
                NODE_SIZE[k] = float(metric_entry['value'])
                min_size = min(min_size, NODE_SIZE[k])
                max_size = max(max_size, NODE_SIZE[k])
                break

    # scale node sizes
    MAX_DISPLAY_SIZE = 50 # maximum size of a node during visualization
    MIN_DISPLAY_SIZE = 10 # minimum size of a node during visualization
    for k in NODE_SIZE:
        # calculate visualization size by mapping from size metric value to [MIN_DISPLAY_SIZE, MAX_DISPLAY_SIZE]
        NODE_SIZE[k] = (MAX_DISPLAY_SIZE-MIN_DISPLAY_SIZE) * (NODE_SIZE[k]-min_size)/(max_size-min_size) + MIN_DISPLAY_SIZE

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
    
    # if args.type == 'cg':
    #     visualize_call_tree( METHODS, NODE_SIZE, PATHS, file_name=base_html, max_depth=args.maxDepth, max_edges=args.maxEdges, show=False)
    # else:
    #     visualize(root_list=root_list, file_name=base_html, max_depth=args.maxDepth, max_edges=args.maxEdges, show=False)
    
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
    inject_custom_code(base_html, args.ref, out_html)
    print('generated:')
    print(f'- {base_html}')
    print(f'- {out_html}')
    