class Node:
    def __init__(self,query):
        self.query = query
        self._children = []
        self._ctx = [query]
        self._urls = self._get_urls()

    def _get_urls(self):
        return [f"url_{i}_{self.query}" for i in range(5)]

class TreeOfThought:
    def __init__(self):
        self.root = None
        self._max_depth = 2

    def build(self,initial_query,max_depth=2):
        self.query = initial_query
        self.root = Node(initial_query)
        self._max_depth = max_depth
        self._expand_tree(self.root)

    def _generate_children(self,query,depth):
        return [Node(f"query_{depth+1}_{i}_{self.query}") for i in range(1, 6)]

    def _expand_tree(self,root,depth=0,max_depth=3):
        if depth < self._max_depth:
            children = self._generate_children(root.query,depth=depth)
            for child in children:
                root._children.append(child)
                self._expand_tree(child,depth=depth+1,
                                  max_depth=max_depth)


if __name__ == '__main__':
    tree = TreeOfThought()
    tree.build("what is machine learning")


    def print_tree(node, level=0):
        print("--" * level + f"└─ {node.query}")
        print("--" * level + f"   Context: {node._ctx}")
        for child in node._children:
            print_tree(child, level + 1)

    print_tree(tree.root)


