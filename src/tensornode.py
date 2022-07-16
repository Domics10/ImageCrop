class tensorNode:
    def __init__(self, tensor, id):
        self.id = id
        self.parent = None
        self.tensor = tensor
        self.childs = {id : []}
    
    def add_node(self, tensorNode, parent_id):
        if parent_id not in self.childs:
            self.childs[parent_id] = []
        tensorNode.add_parent(parent_id)
        self.childs[parent_id].append(tensorNode)

    def update_tensor(self, upt, n_id): #non modifica le foglie
        if n_id == 0:
            self.tensor = upt
        else:
            child = bfs(self, n_id)
            parent = child.get_parent(n_id)
            for child in self.childs[parent]:
                if child.get_id() == n_id:
                    child.tensor = upt               

    def get_childs(self):
        return self.childs[self.id]

    def get_tree(self):
        return self.childs

    def get_tensor(self):
        return self.tensor

    def add_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_id(self):
        return self.id
    
def bfs(tnd, n_id):
    visited = []
    queue = []

    visited.append(tnd.get_id())
    queue.append(tnd.get_id())
    if n_id == tnd.get_id():
       return tnd
    while queue:          
        id = queue.pop(0)
        if id in tnd.get_tree():
            for child in tnd.get_tree()[id]:
                if child.get_id() not in visited:
                    visited.append(child.get_id())
                    queue.append(child.get_id())              
                    if n_id == child.get_id():
                        return child