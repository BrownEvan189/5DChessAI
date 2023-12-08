import random
import copy
import os

class TreeNode:

    def __init__(self, parent, childrenNames, children, generation, state, name, value, parentName):
        self.parent = parent
        self.childrenNames = childrenNames
        self.generation = generation
        self.state = state
        self.name = name
        self.value = value
        self.parentName  = parentName
        self.children = children
rootParent = TreeNode(parent = None, childrenNames = 'root', children = [], generation = -1, state = None, name = 'rootParent', value = 0, parentName = None)
root = TreeNode(parent = rootParent, childrenNames = [], children = [], generation = 0, state = 1, name = 'root', value = -1000, parentName = 'None')
tree = [[root]]

global queue
queue = {tree[0][0].value:tree[0][0]}

#Print tree
def printTree():
    for i in tree:
        print(f'Generation {i[0].generation}:')
        for j in i:
            print(f'Name: {j.name}, Parent: {j.parentName}, Value: {j.value}, Children: {j.childrenNames}')

def getValue():
    return random.random()

#Naming System
usedNames = []
letters = 'abcdefghijklmnopqrstuvwxyz'
def assignName():
    name = ''
    while(1):
        for i in range(1,4):
            name += letters[random.randint(0, 25)]
        if name in usedNames:
            continue
        else:
            usedNames.append(name)
            break
    return name

#Select (Best first search)
def select(node):
    if node.children == []:
        return node
    else:
        for i in node.children:
            queue[i.value] = i
        return select(queue.pop(max(queue)))
    
#Expand:
def expand(node):
    if len(tree) == node.generation + 1:
        tree.append([])
    for k in range(2):
        child = TreeNode(
            parent = node, 
            parentName = node.name, 
            childrenNames = [], 
            children = [], 
            generation = node.generation + 1, 
            state = None, 
            name = assignName(), 
            value = None
            )
        tree[node.generation + 1].append(child)
        node.childrenNames.append(child.name)
        node.children.append(child)

#Simulate:
def simulate(node):
    for i in node.children:
        i.value = getValue()

#Backpropogate:
def backPropogate(node):
    k = -1
    for i in node.children:
        leaf = i
        p = leaf.value - 0.5
        for j in range(leaf.generation, 0, -1):
            leaf.parent.value += (p * k)
            leaf = leaf.parent
            k *= -1

#Tree search:
def treeSearch(num):
    global queue
    for i in range(0, num):
        node = tree[0][0]
        node = select(node)
        expand(node)
        simulate(node)
        backPropogate(node)
        queue = {tree[0][0].value:tree[0][0]}
      
treeSearch(10)
printTree()
