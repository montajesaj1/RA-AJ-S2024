- [Understanding Cortellis](#understanding-cortellis)

<!-- toc omit heading -->
# Algorithm & DS Design for Cortellis Hierarchy 

### Understanding Cortellis 

- Designed in a tree-like structure s.t. an index 0 will have children with
index 1.
- Following children belong to those immediately preceding them.

i.e. 
```
0	Andrology
1	Male contraception
1	Male genital system disease
2	Hematocele
2	Male genital tract inflammation
```

is equivalent to...

```
0           Andrology
              /   \
1            MC   MGSD
                   / \
2                 H  MGTI
```

### Building a Tree data structure
- Simply 

import csv
from treelib import Node, Tree

def build_tree_from_csv(csv_file):

    tree = Tree()

    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            if row
            tree.create_node(reader[0][1], 0)

build_tree_from_csv('test.csv')
