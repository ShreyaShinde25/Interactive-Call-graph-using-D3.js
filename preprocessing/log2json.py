import re
import json
import argparse
import os
from collections import defaultdict
import util
import const

# can be tested at https://regexr.com/7snrp
PATTERN = r'(?P<ts>\d{2}\:\d{2}\:\d{2}\.\d+)(\*|\s)+(?P<thread>\w+)\s+(?P<tracepoint>(\w|\.)+)\s(.+)\[(?P<stack_pos>\d+)\]\s(?P<class_method_name>.+)(?P<input_params>\(\S*\))(?P<return_type>\S+)\s(\(Bytecode\sPC\:\s(?P<pc>\d+)\,\sLine\:\s(?P<line_no>\d+)\)\s)?(invkCD\:\s(?P<invoke_count_down>\d+)\,)?(?P<exec_type>\((Compiled Code|Native Method)\))?(\sstrtCnt\:\s(?P<start_sample_count>\d+)\,\sgblCnt\:\s(?P<global_sample_count>\d+)\,\scpu\:\s(?P<cpu>\d+\.\d+)\%\,)?\s(?P<method_size>\d+)\sbcsz'

class LogStackEntry:
    def __init__(self, data):
        self._data = data
        self._data["stack_pos"] = int(self._data["stack_pos"])
        self._data["class_name"], self._data["method_name"] = data["class_method_name"].rsplit(".", 1)
        self._data["method_descriptor"] = f'{data["input_params"]}{data["return_type"]}'

    def get_thread(self):
        return self.get_value('thread')    

    def get_call_site(self):
        return self.get_value('pc') # or 'line_no'

    def get_tracepoint(self):
        return self.get_value('tracepoint')
    
    def get_signature(self):
        return f'{self.get_value("class_name")}.{self.get_value("method_name")}{self.get_value("method_descriptor")}'

    def get_class_name(self):
        return self.get_value("class_name")

    def get_method_name(self):
        return self.get_value("method_name")
    
    def get_stack_pos(self):
        return self.get_value("stack_pos")

    def get_exec_type(self):
        t = self.get_value("exec_type")
        if t:
            t = t.lower().split(" ")[0].replace("(", "")
        return t if t else "interpreted"
    
    def get_value(self, key):
        return self._data[key] if key in self._data else None

def parse_line_for_data(line):
    try:
        match = re.search(PATTERN, line)
        if match:
            entry = LogStackEntry(match.groupdict())
            return entry
        else:
            print(f"No match found: {line}")
            return None
    except Exception as e:
        print(f"Error processing line: {line}\nError: {e}\n")
        # import sys; sys.exit(0)
        return None

def update_methods(json_methods, entry, method_map, next_method_id):
    key = entry.get_signature()
    if key not in method_map:
        method_map[key] = next_method_id
        json_methods.append({
            "id": next_method_id,
            "className": entry.get_class_name(),
            "methodName": entry.get_method_name(),
            "methodDescriptor": entry.get_value("method_descriptor"),
            "metrics": [
                {"key": "methodSize", "value": entry.get_value("method_size")},
                {"key": "cpu", "value": entry.get_value("cpu")}
            ]
        })
        next_method_id += 1
    else:
        #TODO: aggregate metrics here??
        pass
    return next_method_id

def update_paths(json_paths, call_stack, method_map):
    current_level = json_paths
    prev_entry = None
    i = len(call_stack)-1
    while i >= 0:
        current_entry = call_stack[i]
        current_id = method_map[current_entry.get_signature()]
        call_site = prev_entry.get_call_site() if prev_entry else current_entry.get_thread()
        exec_type = current_entry.get_exec_type()
        found = False
        for entry in current_level:
            # match criteria:
            # - same id (same method being called)
            # - called from same call-site (unless its at the bottom of stack)
            if entry["id"] == current_id and (call_site is None or entry["callSite"] == call_site):  
                found = True
                current_level = entry["children"]
                break
        if not found:
            # print(f'new entry: {current_entry.get_signature()}' )
            new_entry = {"id": current_id, "callSite": call_site, "execType": exec_type, "children": list()}
            current_level.append(new_entry)
            current_level = new_entry["children"]
        prev_entry = current_entry
        i -= 1

def process_call_stack(call_stack, method_map, next_method_id, json_methods, json_paths):
    # update methods
    for entry in call_stack:
        next_method_id = update_methods(json_methods, entry, method_map, next_method_id)
    # update paths
    update_paths(json_paths, call_stack, method_map)
    return next_method_id

def read_in_call_stacks(file, yield_tracepoint):
    call_stacks = defaultdict(list)
    for line in file:
        entry = parse_line_for_data(line)
        if entry is None:
            continue
        thread_id = entry.get_thread()
        if thread_id in call_stacks and entry.get_tracepoint() == yield_tracepoint:
            yield call_stacks[thread_id]
            call_stacks[thread_id].clear()
        call_stacks[thread_id].append(entry)

    # clean up
    for thread in call_stacks:
        if call_stacks[thread]:
            yield call_stacks[thread]

def main():
    parser = argparse.ArgumentParser(description='Script for converting JVM tracepoint output into JSON format which can be used for caller-callee visualizations.')
    parser.add_argument('--input', '-i', type=str, required=True, help='path to input (.log, .fmt) file to process with tracepoint output.') 
    parser.add_argument('--output', '-o', type=str, default='', help='output (.json) file name which will contain execution path information.')    
    args = parser.parse_args()
    util.mkdir(const.OUT_DIR) 
    method_map = {}
    next_method_id = 0
    json_methods = []
    json_paths = []

    with open(args.input, 'r') as file:
        for call_stack in read_in_call_stacks(file, "j9jit.93"):
            next_method_id = process_call_stack(call_stack, method_map, next_method_id, json_methods, json_paths)
    
    # structured based on outline in README
    json_output = {
        "methods": json_methods,
        "paths": json_paths
    }
    output_json = f"{const.OUT_DIR}/{args.output}"
    if args.output == '':
        log_name = util.get_file_name(args.input)
        output_json = f'{const.OUT_DIR}/{log_name}.json'
    with open(output_json, 'w') as json_file:
        json.dump(json_output, json_file, indent=4)

if __name__ == "__main__":
    main()
