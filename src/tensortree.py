import numpy as np
import tensorflow as tf
from functools import reduce
from .tensornode import tensorNode, bfs

def buildTree(tensor, leafs):

    l0 = tensorNode([], 0)
    l1 = list()
    
    nleaf=len(leafs)
    if 0 in leafs:
        nleaf-=1

    for i in range(nleaf):
        l1.append(tensorNode([], 1+i))

    l20 = list()
    for i in range(leafs[0]):
        l20.append(tensorNode(tensor[i], len(l1)+1+i))
        
    l21 = list()
    for i in range(leafs[0],leafs[1]+leafs[0]):
        l21.append(tensorNode(tensor[i], len(l1)+1+i))

    l22 = list()
    for i in range(leafs[0]+leafs[1],leafs[0]+leafs[1]+leafs[2]):
        l22.append(tensorNode(tensor[i], len(l1)+1+i))
    
    #add branches
    for layer in l1:
        l0.add_node(layer, l0.get_id())
        
    if l20:
        for layer in l20:
            l0.add_node(layer, l1[0].get_id())    
    if l21:
        for layer in l21:
            l0.add_node(layer, l1[1].get_id())
    if l22:
        for layer in l22:
            if len(l1)==3:
                l0.add_node(layer, l1[2].get_id())
            elif len(l1)==2:
                l0.add_node(layer, l1[1].get_id())

    return l0

def rebuildImg(tree, leafs):
    te = list()
    low = len(list(filter(lambda x:x!=0, leafs)))
    for i in range(low+1, low+1+np.sum(leafs)):
        te.append(bfs(tree, i))

    left = list(map(lambda x: x.get_tensor(), filter(lambda x:x.get_parent()==1, te)))
    middle = list(map(lambda x: x.get_tensor(), filter(lambda x:x.get_parent()==2, te)))
    right = list(map(lambda x: x.get_tensor(), filter(lambda x:x.get_parent()==3, te)))
    c = list()
    if left:
        c1 = reduce(lambda a,b: np.concatenate((a,b), axis=1), left)
        c.append(c1)
    if middle:
        c2 = reduce(lambda a,b: np.concatenate((a,b), axis=1), middle)
        c.append(c2)
    if right:
        c3 = reduce(lambda a,b: np.concatenate((a,b), axis=1), right)
        c.append(c3)

    reb = tf.constant(reduce(lambda a,b: np.concatenate((a, b), axis=2), c))
    return reb