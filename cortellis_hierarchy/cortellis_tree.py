import csv
import json

def parse_hierarchy(csv_file):
    hierarchy = {}
    current_level = hierarchy
    stack = [(0, current_level)]

    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=',')
    
        for line in reader:
            depth = int(line[0])
            text = line[1].strip()
            
            if depth < 0 or not text:
                continue
            
            while len(stack) > 1 and stack[-1][0] >= depth:
                stack.pop()
            
            new_node = {}
            stack[-1][1][text] = new_node   
            stack.append((depth, new_node))
    
    return hierarchy

# Loop over the range of files
for i in range(1, 34):
    csv_file = f"data/output_pair_{i}.csv"
    hierarchy = parse_hierarchy(csv_file)

    # Print the hierarchical structure
    print(f"Hierarchy for {csv_file}:")
    print(json.dumps(hierarchy, indent=2))
    
    # Save the hierarchical structure to a JSON file
    json_file = f"data/output_pair_{i}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(hierarchy, f, ensure_ascii=False, indent=4)
