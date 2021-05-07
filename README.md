# ImageProcessingApp
Python Image Processing Application For Color Detection and Photo/Dataset Detecton

Instructions when using OpenCV image detection (main.py):

The user is prompted with two directions allowing them to choose how many images they want to load to train the OpenCV application and how many images they want to load on the webpage to search through.

There is another option after the first two, that when "y" is inputted the user is allowed see the specific images they've selected, you may close out of this program when pressing "q" or may completely ignore this process by inputting any other key. 

When it comes to detecting the specific images the user has selected, the webpage must be in full view and loaded. The user can access the webpage from the link to his or her localhost in the terminal. After each image is in view pressing "p" allows the user to take a screenshot. After this step the user can then close the window. 

The application will use the screenshot as a template when detecting 1 to 1 identical images saving all other images the user wanted trained in the images folder for later use by the application. When the user stops the application a "detected.jpg" will appear allowing the user to see exactly the images that were detected by the openCV application. those images appear with a red rectangle highlighting them.

Bugs:

* Images and questions are prompted twice. This probably in most part has to do with Flask running in main.py and not on its own, I tried fixing this however, OpenCV was having trouble detecting anything on the webpage when it was outside of the main.py file.

* Only one image has the likeliness of being detected. There is a problem with the same image being saved twice and the application not being able to detect or recognize other photos due their duplication. A way to solve this was to iterate through each photo in the list however, due to the previous bug and lack of time I wasn't able to fix this. 
