import os

class Node:
    def __init__(self, path, shortened):
        self.path = path
        self.shortened = shortened
        self.ptrToParent = None
        self.type = None

class Directory(Node):
    def __init__(self, path, shortened):
        Node.__init__(self,path,shortened)
        self.numItems = 0
        self.perms = []
    
    def processDirectory(self):
        if os.access(self.path, os.R_OK):
            self.perms.append("R")
        if os.access(self.path, os.W_OK):
            self.perms.append("W")
        if os.access(self.path, os.X_OK):
            self.perms.append("X")
        self.type = "Directory"

class File(Node):
    def __init__(self, path, shortened):
        Node.__init__(self,path,shortened)
        self.size = 0
    
    def processFile(self):
        data = os.stat(self.path)
        self.size = data.st_size
        self.type = "File"

class FSVis:
    def __init__(self):
        self.adjList = {}
        self.root = None

    def processPath(self,path):
        newPath = ""
        for p in path:
            if p == "/":
                newPath += '\\\\'
            else:
                newPath += p
        return newPath
    
    def addToAdjList(self, key, value):
        if key not in self.adjList:
            self.adjList[key] = [value]
        else:
            self.adjList[key].append(value)

    #Using BFS, process every subdirectory given the root as path. 
    #If its a file, just add to adjList
    #If its a folder, add it to the explore queue
    def getFilesAndFolders(self, path):
        if not os.path.isdir(path):
            print("Please give a directory. " +path+ " is not a file")
            return False
        ptr = len(path)-1
        while path[ptr] != "\\":
            ptr -= 1
        rootDir = Directory(path, path[ptr+1:])
        rootDir.processDirectory()
        rootDir.ptrToParent = None
        self.root = rootDir
        q = [rootDir]
        while len(q) > 0:
            node = q.pop(0)
            node.numItems = len(os.listdir(node.path))
            for file in os.listdir(node.path):
                childFullPath = os.path.join(node.path, file)
                if os.path.isdir(childFullPath): 
                    newDir = Directory(childFullPath, file)
                    newDir.processDirectory()
                    newDir.ptrToParent = node
                    self.addToAdjList(node, newDir)
                    q.append(newDir)
                else:
                    newFile = File(childFullPath, file)
                    newFile.processFile()
                    newFile.ptrToParent = node
                    self.addToAdjList(node, newFile)
        return True
    
    def consoleExamination(self):
        q = [self.root]
        while len(q) > 0:
            node = q.pop(0)
            print(node.shortened + ": ")
            for nodes in self.adjList[node]:
                print(nodes.shortened + ", ")
                if os.path.isdir(nodes.path): 
                    q.append(nodes)