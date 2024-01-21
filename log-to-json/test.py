import re
import json

def parse_line_for_class_and_method(line):
    try:
        match = re.search(r'\[(\d+)\] ([\w\.<>]+) \(([\w\.]+:\d+)\)\|(\d+) bcsz\|', line)
        if match:
            pos_in_stack = int(match.group(1))
            class_method_info = match.group(2)
            method_size = int(match.group(4))
            if '.' in class_method_info:
                class_path, method_name = class_method_info.rsplit('.', 1)
                return pos_in_stack, class_path, method_name, method_size
            else:
                return pos_in_stack, None, None, None
        else:
            return None, None, None, None
    except Exception as e:
        print(f"Error processing line: {line}\nError: {e}")
        return None, None, None, None

def add_method(json_methods, class_path, method_name, method_size, method_map, next_method_id):
    key = f"{class_path}.{method_name}"
    if key not in method_map:
        method_map[key] = next_method_id
        json_methods.append({
            "id": next_method_id,
            "classPath": class_path,
            "methodName": method_name,
            "metrics": [{"key": "methodSize", "value": method_size}]
        })
        next_method_id += 1
    return next_method_id

def add_path(json_paths, call_stack):
    current_level = json_paths
    for method_id in call_stack:
        found = False
        for child in current_level:
            if child["id"] == method_id:
                current_level = child.get("children", [])
                found = True
                break
        if not found:
            new_child = {"id": method_id, "children": []}
            current_level.append(new_child)
            current_level = new_child["children"]

def process_batch(batch, method_map, next_method_id, json_methods, json_paths):
    call_stack = []

    for line in batch:
        pos_in_stack, class_path, method_name, method_size = parse_line_for_class_and_method(line.strip())

        if class_path is None or method_name is None:
            continue

        next_method_id = add_method(json_methods, class_path, method_name, method_size, method_map, next_method_id)

        method_id = method_map[f"{class_path}.{method_name}"]

        call_stack = call_stack[:pos_in_stack-1]
        call_stack.append(method_id)
        add_path(json_paths, call_stack)

    return method_map, next_method_id

def read_in_batches(file, batch_size):
    batch = []
    for line in file:
        batch.append(line)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

def main():
    BATCH_SIZE = 50
    method_map = {}
    next_method_id = 0
    json_methods = []
    json_paths = [{"id": 0, "children": []}]

    with open('temp.txt', 'r') as file:
        for batch in read_in_batches(file, BATCH_SIZE):
            method_map, next_method_id = process_batch(batch, method_map, next_method_id, json_methods, json_paths[0]["children"])

    json_output = {
        "methods": json_methods,
        "paths": json_paths
    }

    with open('output.json', 'w') as json_file:
        json.dump(json_output, json_file, indent=4)

if __name__ == "__main__":
    main()
