from initialization import FSVis
from p5 import *
f = None
path = ""
textBuffer = ""
isLanding = False
#Pointer to the node that makes the current root
localRoot = None
#Variable that tells you if viewing of a node is on or off. If viewing != None, then viewing == the node we're viewing
viewing = None
#Length of bubble, Spacing between bubbles
radiusAndDistanceOfBubble = {
    "root" : (60,840),
    3: (200,200),
    6: (100,100),
    9: (75,50),
    12: (60,30),
    15: (50,20),
    18: (40,20),
    21: (35,15),
    24: (30,15),
    27: (26,14),
    30: (25,10),
}

#Tuple of (x1,y1,x2,y2,node,root/child)
bubbleLocations = []

def setup():
    size(1800,1000)
    stroke(255)

#If esc is clicked, set path back to empty and call landingPage()
def draw():
    global path, isLanding, localRoot, radiusAndDistanceOfBubble, bubbleLocations, viewing
    background(0)
    if len(path) == 0:
        isLanding = True
        landingPage()
    else:
        isLanding = False
        if localRoot == None:
            getFS()
            if f:
                localRoot = f.root
            else:
                localRoot = None
        if localRoot:
            bubble(900, 120, 120, localRoot) #The localRoot is always at the same spot
            bubbleLocations.append((680, 0, 1020, 240, localRoot, "root"))
            #Loop through the subdirectory of localRoot, and call bubble
            radius_space = None
            if localRoot.numItems >= 30:
                radius_space = radiusAndDistanceOfBubble[30]
            else:
                subDirSize = localRoot.numItems
                while subDirSize % 3 != 0:
                    subDirSize += 1
                radius_space = radiusAndDistanceOfBubble[subDirSize]
            x = 0
            for items in f.adjList[localRoot]:
                bubbleLocations.append((x, 600-radius_space[0], x+radius_space[0]*2, 600+radius_space[0], items, "child"))
                bubble(x+radius_space[0], 600, radius_space[0], items)
                lines((900,240), (x+radius_space[0], 600-radius_space[0]))
                x += 2*radius_space[0] #This is 1 circle
                x += radius_space[1] #Add empty space
            if viewing != None:
                displayClickedBubble(viewing)

#Spawns another box and displays info on the clicked bubble. Maximum of 20 lines of text. 
#Dimentions of text box is 200x200 starting from (450,300)
#STILL NOT WORKING PROPERLY 
def displayClickedBubble(node):
    if node == None:
        return
    global f
    y = 0
    text("Exit by clicking RIGHT clicking", (500, y))
    y += 10
    text("Full path: " + node.path, (500, y))
    y += 10
    text("Shortened name: " + node.shortened, (500, y))
    y += 10
    if node.ptrToParent in f.adjList:
        text("Parent name: " + node.ptrToParent.shortened, (500, y))
        y += 10
    if node.type == "Directory":
        text("Number of items here: " + str(node.numItems), (500, y))
        y += 10
        text("Perms: " + ' '.join(node.perms), (500, y))
        y += 10
        text("It's a directory", (500, y))
        y += 10
    else:
        text("Size of file: " + str(node.size), (500, y))
        y += 10
        text("It's a file", (500, y))
        y += 10

#Does math to calcualte to bubble at specified location
def bubble(x, y, radius, node):
    fill('brown')
    ellipse(x, y, 2*radius, 2*radius)
    text_align("CENTER")
    fill(0)
    text(node.shortened,(x, y))

#Does math to calcualte to lines at specified coordinates
def lines(locRoot, locChild):
    stroke_weight(5)
    line(locRoot, locChild)

#Takes in x,y coordinates of the mouse and tries to find the node being clicked. 
#If found, returns the node, root/child identification, True
#If not found, returns None, None and False
def which_node_pressed(x, y):
    global bubbleLocations
    for b in bubbleLocations:
        if b[0] <= x and x <= b[2] and b[1] <= y and y <= b[3]:
            return b[4], b[5], True
    return None, None, False

#If left button is pressed, we will call getFS
#If right button is pressed, we will spawn a box to displays info on the clicked bubble
def mouse_pressed():
    global localRoot, bubbleLocations, viewing
    if f != None:
        """
        On left mouse button, update the localRoot to the clicked bubble. 
        Find out which bubble was clicked using the bubble array.
        """
        node,root_or_child, valid = which_node_pressed(mouse_x, mouse_y)
        if valid and mouse_button == "LEFT":
            if node in f.adjList: #Could be a file which wouldn't be in the adjList as a key
                if root_or_child == "child":
                    localRoot = node
                    bubbleLocations = []
                else:
                    localRoot = node.ptrToParent
                    bubbleLocations = []
            viewing = None
        elif valid and mouse_button == "RIGHT":
                viewing = node
        else:
            viewing = None

def getFS():
    global f, textBuffer, isLanding, path
    f = FSVis()
    if not f.getFilesAndFolders(f.processPath(path)):
        isLanding = True
        path = ""
        textBuffer = "" 
        f = None

#Landing page with a text field to give us the path
def landingPage():
    global path, textBuffer
    fill(120)
    ellipse(900,500,550,550)
    text_align("CENTER")
    fill(256)
    stroke_weight(1)
    text("Type a valid directory. When you're done hit ENTER", (900, 350))
    fill(0)
    if len(path) == 0:
        text(textBuffer, (900,500))
    else:
        text(path, (900,500))

#Any key strokes are logged here
def key_pressed():
    global isLanding, textBuffer, path, viewing, f, localRoot
    if key == "UP":
        path = ""
        isLanding = True
        textBuffer = ""
        f = None
        viewing = None
        localRoot = None
        return
    if isLanding:
        if key == "ENTER":
            path += textBuffer
            textBuffer = ""
        elif key == "BACKSPACE":
            textBuffer = textBuffer[:len(textBuffer)-1]
        elif key == "SHIFT":
            pass
        elif key == ":":
            textBuffer += str(":")
        else:
            textBuffer += str(key)

run()
    