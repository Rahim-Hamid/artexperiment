Repository for code that generates some kind of art

p5proj folder is for projects made in p5.js - experimenting with trying to create repeated tesselations/patterns using the library - once the file is open in editor, right click the index.html file and run as live server

Strude REPL is a live music coding website based on a Javascript library, and the files in my folder are text files containing code that when run on the website will play music

The Pixelation project is able to take images and based on user input of block size produce varyingly pixelated images from an original image - the lower the block size, the greater the pixelation
Within this project, the mosaic.py file can take a target file and many other tile files and use the tile files to form "pixels" in an newly formed target image

The Live_Feed folder is for an art installation project and uses numerous python libraries to take an image at 30 second intervals through a dedicated camera and apply either a heavy CRT filter or a dithering effect on the image taken. It also supports live video feeds if the sleep function is removed, and also supports binary representation, block representation and ASCII character representation for live video feeds - may implement saving the photos taken at some point, concerns around storage

The Image Sequencer takes a folder of images as input and a list of random words as the label input and assigns the label to the images in the sequence (that are randomized), and then displays the images in fullscreen with the labels applied at 1 second intervals before moving to the next image-label pair - (for use the file path to the folder has to be modified, I did not include it since the way I got it to work was to create an absolute path in my own workspace)
