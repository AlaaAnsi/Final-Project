# WebsiteR
#### Video Demo:
#### Description:-


## Main goal:
My project seeks to fix a small problem. In Instagram, YouTube, or other similar apps, you might frequently see people suggesting excellent websites. If you find this information useful, you may save the video. But when this happens frequently, the saved URLs list becomes disorganized, making it impossible to find a specific website in your saved URLs. As a result, there should be a solution to this minor issue.

And this is what my project aims to do—make the top websites easier to access.

---

# Project files and folders
These make up my project:

**Front end:-**

*templates folder:* pages templates

*static folder:* containing the uploaded images and the "Done" page image

**Back end:-**

*app.py:* the main file

*requirements.txt:* contains the name of the libraries I used in app.py

*websiter.db:* SQLite database of the project

*README.md*

# SQLite tables
There are two tables in the project: "users" and "websites."

## users
Contains:

***ID:*** primary key


***user_name***

***password_hash:*** the user's password but hashed.
## websites

Contains:

***ID:*** primary key


***user_id:***  foreign key references users (id)


***imagesfn:***  The name of the file that contains the image.


***name:***  The name of the recommended website.


***link:***  The link to the recommended website

***desc:***  The recommended website description

***brief:***  The recommended website brief

***howto:***  The recommended website How-to use

***path:***  The path to the website interface image


# How the project works
I'll briefly go into more detail about app.py and the JavaScript I use below
## First, the normal functions:

***error():*** displays a page with an error message.

***allow_extension():*** checks the file extension of the uploaded image.

## Now, the routes' functitons:

***index():*** It has a small algorithm that it uses to handle the homepage functionality, which is randomizing the selection of websites' recommendation cards.

***register():*** This function manages the registration functionality, as the name would imply. It does this by verifying that the user provided a name and a password, then confirming that the name provided is unique, and finally remembering the user by storing his name and ID in the session variable. All of this occurs after the user clicks "Submit."

***login():*** Similar to how it works in the register function, after a user clicks the "Submit" button, the system checks to see if the user has entered a name and a password before confirming that the information is accurate. The code behind ultimately remembers the user by storing their name and ID in a session variable if the information provided is accurate.

***logout():*** merely clears the session variable to indicate that the user has logged out, making it the simplest function.

***add_website():*** This procedure manages the Add Website page operations. It checks to see if the user entered a name, a link, a brief, a description, a how-to, and an image. The entered data is then saved in variables for each.

The saving part follows that.

The program must first determine whether the image extension is permitted before storing the uploaded image.

If the user ID does not already exist, it is created after that, and a file with the name the user entered for the website recommendation is created inside the first file. The program then stores the image in static/uploads/[user id]/[website name] after all of that.

The text portion of the process is now complete; it simply creates a path string for the image for a future user and stores the path, the name, the brief, the description, how-to, and link in a sqlite table called "websites."

***done():*** renders the done.html template.

***error_t():*** shows the error message that was sent when the error function was used.

***view():*** displays the website recommendation requested. It accomplishes this by first obtaining the name of the requested website recommendation, then its image path, and finally performing a database query to obtain all the relevant data for the requested website recommendation. Finally, it sends the view.html template all of these details so that it can display them.

***search():*** It employs a straightforward search algorithm, obtains the keyword entered into the search box, and then compares the keyword with the database to find a similar word. If it finds one, the information is stored in a variable and transferred to search.html so that the result can be displayed.


# Finally, the Javascript I used

Javascript was only ever used once. and that is located in the file "add_website.html."

The idea behind using it is to create a character counter for the brief text box that displays the character counts and prevents users from entering more than 100 characters.

It functions as follows: it receives the elements "brief" and "char count," which stand in for the brief text box and the space beneath it, respectively, where the counter will be displayed. The code will then determine the length of what is typed whenever the key is up in the short text box. It will stop accepting keystrokes and stop the counter at 100 characters if the user types more than 100 characters.

This concludes my project.











    