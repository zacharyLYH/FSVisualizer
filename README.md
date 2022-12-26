# FSVisualizer
A file system visualizer implemented using p5pi, a creative coding library. 

# What does it do?
It provides an intuitive graphical way to navigate your directories. Under corrrect use, provide the FSVisualizer with a full directory and you will see your current (initial input) directory and its content as a tree. You may do operations like traversing your file system and pulling metadata about any particular file or folder. To traverse your file system, if the node you left click on is a directory, you will access that directory and update the UI. To pull metadata about any one node, right click the node and some metadata will pop up at the top left. 

# Limitations
There are many. Unfortunately with p5, there is no easy way to implement a "slide the screen" feature without making the project unacceptably latent and difficult to implement. So, in a fixed sized screen, we try to give you as much information as possible. However, it becomes unusable as soon as the number of folders and files it has to show is more than 30, and thus, in this implementation we put a hard cap of showing only 30 files and subfolders at any one directory. Another limitation is that you may only use a certain subset of characters during input. More on that 3 sections down. You cannot go up a directory from the input directory. That is because we're using a traversal algorithm that only traverses downward from where it currrently is in the file system tree.

# Set up
1) Make sure your system has these following requirements outlined in [the p5 installation docs](https://p5.readthedocs.io/en/latest/install.html#installing-p5) to get 
started.
2) On the command line, run `python3 main.py`

At this point you should see a screen that looks like this:
![image](https://user-images.githubusercontent.com/78431286/209570903-9546be81-04fc-470b-9d62-0216b8c7577c.png)
 
# To use
1) Type in a valid **full** directory path (Note there are some character restrictions, outlined in the next subsection). An invalid directory will print an error 
message on the command line.
1.1) Note that you have to type the input letter by letter, since the listener will be logging key strokes as plain text, without further interpretation. 
2) Hit enter when you're ready

## Character restrictions
In general, all characters are readable by this implementation. The only characters that cannot be read are those that require the **SHIFT** button to select.
The only **exceptions** to this rule are capital letters (**SHIFT** + a-z), and the colon key (**SHIFT** + ;). Despite the limitations, these should be enough for 
most directory paths.

## Example full directories
1) C:/Users/John Smith/Desktop/work/Backend/node_modules
2) D:/LongTermStorage/Diaries/2021/January
3) E:  

# How it was built
Without going into every single function, this is the high level design of this repository. 
After getting user input, assuming the input is a valid repository, we run BFS using the input directory as the root and pulling out subdirectories and files
storing them as an adjacency list of `Directory:[List of Subdirectories and Files]`. This is an expensive one time operation that we'll hope will amortize over the lifetime of this instance. Next, using some math, we figure out how to draw the node bubbles and edge lines based on the number of subfolders and files a directory we want to show has, then draw. The size of the bubbles and spaces between them were hardcoded to an extent. We won't go into any more detail on that here, since a repeating that here is merely a repetition of what you'll find in the code. A point to note is that we've modularized to the best of our ability the various input channels (keyboard and mouse), from the various drawing features (drawing a bubble, drawing edges), and the program state controllers like `landingPage()` and `getFS()`. 

# Performance and usability
In general, p5py performs badly on heavy workloads. In big files, the amount of data to calculate drawables, print them, and store are incredibly costly - you might even experience latency in the seconds range. The use case of this project is probably very limited. Due to various set up libraries and sofware you need, Dockerizing this application might be an idea, however since it requires OpenGL, an Ubuntu image is probably needed and thus even Dockerizing it becomes expensive. It's probably easier to discuss where you **want** this piece of software. If your project assumes the user has OpenGL and p5pi installed, isn't expecting to input directories with more than 30 items, and doesn't mind a less than perfect UI, then this application in its current stage of development could fit your bill. 

# Motivation behind this project
I was inspired by Daniel Shiffman, one of the more pronounced figures in the p5 community to try out p5. Daniel uses p5.js in his Youtube videos, but personally I'm not a big fan of Javascript, and thus went the Python route. Notably, had I used Javascript instead of Python, the performance would've probably been better. I knew I wanted to build something out of p5, but I didn't want to do something I know Daniel had already done and I wanted to build something "practical" rather than simulation type programs Daniel usually builds. I thought a file system visualizer would've been interesting, as it incorporates the knowledge of UNIX style file systems and a nice traversal algorithm, and so I did it. Initially I was going for something that could swipe, zoom in, and zoom out, but it quickly became clear that was either impossible in p5 or terribly difficult and bad performing anyway. I settled for less but it was the best I could do under time and performance constraints. 

# Contribute
I would love to know if folks wanted to contribute to this project. You could fork this repository and build it out yourself, or shoot me an email at leeyihong03@gmail.com and we could discuss any ideas you might have.

# Final words
At this point in time, I'm no longer working on this project on an active basis hence there will be no more new updates after this version from me. However, as mentioned, if you have any cool ideas shoot me an email and I'll be happy to collaborate!
