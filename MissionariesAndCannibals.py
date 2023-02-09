#Rajeshwor Niroula
#Roll NO 71
#3C 3M problem 
#statespace tree is generated within the program directory
from collections import deque
from anytree import RenderTree
import graphviz
from anytree.exporter import DotExporter

class State:
    _id = 0
    def __init__(self,missionaries,cannibals,shore):
        self.name = State._id
        State._id += 1
        self.children = []
        self.parents = []
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.shore = shore
    
    def add_child(self,child):
        child.parents.append(self)
        for p in self.parents:
            child.parents.append(p)
        self.children.append(child)

    def compute_child_nodes(self):
        if (self.shore == 1):
            sign = -1 #original shore then substract
        else:
            sign = 1 #second shore then add
        for mis in range(3):
            for can in range(3):
                if (mis+can >= 1 and mis+can<=2 ):#since the boat can carry either 1 or 2 passengers
                    newState = State(self.missionaries + sign * mis, self.cannibals + sign * can,self.shore + sign * 1)
                    if(newState.valid_permu()):
                        self.add_child(newState)     
                        
    def valid_permu(self):
        if (self.cannibals > 3 or self.missionaries > 3 or self.cannibals < 0 or self.missionaries < 0):#substracting from zero popultion or adding 1 to max population
            return False
        if (self.cannibals > self.missionaries and self.missionaries >= 1 ):#cannibals > in first shore
            return False
        if(self.cannibals < self.missionaries and self.missionaries <= 2 ):#cannibals > in second shore
            return False
        return True

    def solution(self):
        return (self.cannibals == 0 and self.missionaries == 0 and self.shore == 0)
    
    def state(self):
        return(self.missionaries,self.cannibals,self.shore)
  
def BFS(initial):
    queue = deque([initial])
    i=0
    while(queue):
        irrelevant = False
        i = i + 1
        node = queue.popleft()
        #print(node.state())
        if(node.solution()):
            print("solution found")
            return node
        else:
            #checking if the node is same as its parent appending iff its different
            for p in node.parents:
                if(node.state() == p.state()):
                    #print("redundent")
                    irrelevant = True
                    break
            if(not irrelevant):
                #print("revelent : " ,node.state())
                node.compute_child_nodes()
                queue.extend(node.children)
 
def nodeName(node):
    return ('id:%s state:%s' % (node.name, node.state()))

def main():
    initial = State(3,3,1)
    node = BFS(initial)
    solutionPath = []
    solutionPath.append(node.state())
    for p in node.parents:
        solutionPath.append(p.state())
    solutionPath.reverse()
    print(solutionPath)   
    DotExporter(initial,nodenamefunc = nodeName).to_picture("stateSpace.png")

    
if __name__ == "__main__":
   main()
