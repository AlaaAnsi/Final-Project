import os
import random

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from helpers import error
from werkzeug.security import check_password_hash, generate_password_hash

from flask_session import Session

UPLOADE_FOLDER = "C:\\Users\\Alaa-Ansi\\vscode\\final_project\\static\\uploads"
allowed_extensions = ['png', 'jpg', 'jpeg']

#app configration
app = Flask(__name__)

#ensure auto reloading for templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

#some configrations
app.config["SESSION_PREMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem" # Storing sessions here, the filesystem
Session(app) # configiring this python file to be a session app 

#configering cs50 SQL
db = SQL("sqlite:///websiter.db") 


# Error cause displaying function
def error(error_cause, error_code):
    # Store error massage and error code in session
    session["e_massage"] = error_cause
    session["e_code"] = error_code
    print(f"{session['e_massage']}\n{session['e_code']}")

    return redirect("/error")


@app.route("/", methods=["GET", "POST"])
def index():
    """ The website home page, container some interface """

    # Query the needed infos from the db
    data = db.execute("select * from users join websites on users.id = websites.user_id")
        

    """ I linked between the two loops (the paths one and the infos one) by indexing with the same list, random_nums """

    if len(data) < 3:
        random_nums = random.sample(range(0, len(data)), k=len(data))

        # This list is created to contain a random selected key and value from the data dict
        random_list = []
        
        print(f"The choosed nums are {random_nums}")

        for i in range(len(data)):
            x = data[random_nums[i]]
            print(f"x is {x}")
            # Add the choosed element to random_list
            random_list.append(x)
            print(f"random_list is {random_list}")

            # clear random_nums to generate new unique numbers when reloading the page
            random_nums.clear()

            return render_template("index.html", session=session, data=random_list)
    else:
        random_nums = random.sample(range(0, len(data)), k=3)

          # This list is created to contain a random selected key and value from the data dict
        random_list = []
        
        print(f"The choosed nums are {random_nums}")

        for i in range(len(data)):
            x = data[random_nums[i]]
            print(f"x is {x}")
            # Add the choosed element to random_list
            random_list.append(x)
            print(f"random_list is {random_list}")

            # clear random_nums to generate new unique numbers when reloading the page
            random_nums.clear()

            return render_template("index.html", session=session, data=random_list)    

    

    # This list is created to contain a random selected key and value from the data dict
    random_list = []
    print(f"The choosed nums are {random_nums}")
    for i in range(3):
        x = data[random_nums[i]]
        print(f"x is {x}")
        # Add the choosed element to random_list
        random_list.append(x)
    print(f"random_list is {random_list}")

    # clear random_nums to generate new unique numbers when reloading the page
    random_nums.clear()

    


@app.route("/Register", methods=["GET", "POST"])
def register():
    """ Registering the user """

    infos = db.execute("select user_name from users")

    #if the user submitted the for
    if request.method == "POST":

        #Ensure user has provided a name
        if not request.form.get("username"):
            return error("Must provide a name", 6)     
        #Ensure user has provided a password    
        elif not request.form.get("password"):
            return error("Must provide a password", 7)

        #check if the name is totally new to the data base
        for i in infos:
            if request.form.get("username") == i["user_name"]:
                return error("This name is used by another user", 8)

        #Storing user data that have been provided
        name = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        #Remember the user

        #but if there is actually someone in the session variabel
        if session:
            session.clear()
     

        #Querying to insert user data
        db.execute("insert into users(user_name, password_hash) values(?, ?)", name, password)

        #remembering the user
        session["user"] = name
        session["id"] = db.execute("select id from users where user_name like ?", name)[0]["id"]

        print(session)
        #redirect to homepage
        return redirect("/")

    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """

    #forget user for now
    session.clear()

    if request.method == "POST":

        #If user left on of the boxes, or both blank ------------ #
    
        #Ensure user has provided a name
        if not request.form.get("username"):
            return error("Must provide a name", 9)     
        #Ensure user has provided a password    
        elif not request.form.get("password"):
            return error("Must provide a password", 10)

        #Storing user data that have been provided
        name = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))    

        #If user's infos are incorrect--------------------------

        row = db.execute("select * from users where user_name like ?", name)
        if len(row) != 1:
            return error("the name or the password is wrong", 11)
        print(row)
        #Checking the name
        if row[0]["user_name"] != name:
            return error("The name you typed does not exist", 12)
        #Checking the password    
        elif not check_password_hash(row[0]["password_hash"], request.form.get("password")): #when using "check_password_hash" function, compare the hashed password with the password plain unhashed text you want                       
            return error("The password you typed is wrong", 13)

        #------------------------------------------------------------------#

        #If every thing went okay

        #Remember user
        session["user"] = name
        session["id"] = db.execute("select id from users where user_name like ?", name)[0]["id"]

        #Redirect him/her to the hamepage
        return redirect("/")


    else:
        return render_template("login.html")




@app.route("/logout")
def logout():
    """ If the user reached this page (via post or get), he/she will be imdaiteley loged-out """

    # Forget user
    print("before" + str(session))
    
    session.clear()

    print("after" + str(session))

    # Redirect to homepage
    return redirect("/login")

#+-----------------------------------------------------------------------+#

def allow_extension(filename):
    """ Allow only images formats [png, jpeg, jpg] """

    #checking first if it is a file 
    if not "." in filename:
        return False

    #now splitting the file name to merely get the extension
    ext = str(filename).rsplit("'")[1].lower().rsplit(".", 1)[1]

    # checking if it's a allowed image format
    if ext in  allowed_extensions:
        return True
    else:

        return False  

#+-----------------------------------------------------------------------+#

@app.route("/add_website", methods=["GET", "POST"])
def add_website():
    """ letting the user add websites pockets """

    if request.method == "POST":

        # before anything, check for possible errors, then store the information

        #check images
        if not request.files.get("image"):
            return error("You haven't provided any images", 1)
        #check brief
        elif not request.form.get("brief"):
                return error("You haven't provided any brief idea of the website", 404)
        #check description    
        elif not request.form.get("description"):
            return error("You haven't provided any description", 2)
        #check howto
        elif not request.form.get("HowToUse"):
            return error("How should the users use the recommanded website?", 3)
        #check name
        elif not request.form.get("name"):
            return error("You haven't provided any website name", 4)
        #check link
        elif not request.form.get("link"):
            return error("You haven't provided any website link", 5)

        #store informations
        image = request.files.get("image")
        brief = request.form.get("brief")
        description = request.form.get("description")
        howto = request.form.get("HowToUse")
        name = request.form.get("name").strip()
        link = request.form.get("link")                    


        # Images section ---------------------------------------------- #

        #storing the image filename
        filename = str(request.files["image"]) 
        print(image)
        if image:
            print(filename.rsplit("'")[1].lower().rsplit(".", 1)[1])


        #checking if it's a allowed image format
        if not allow_extension(str(image)):
            print("image format is not allowed, allowed formats is PNG, JPG, JPEG")
   

        # Save image -------- #

        # First create a new folder for the users if it's not already has been made
        if not os.path.exists(f"C:\\Users\\Alaa-Ansi\\vscode\\final_project\\static\\uploads\\{session['id']}"):
            os.makedirs(os.path.join(f"C:\\Users\\Alaa-Ansi\\vscode\\final_project\\static\\uploads\\{session['id']}"))
            print(f"made a new file called {session['id']}")

        # create a new directory with the added website name (for more capability)
        if not os.path.exists(f"C:\\Users\\Alaa-Ansi\\vscode\\final_project\\static\\uploads\\{session['id']}\\{name.strip()}"):
            os.makedirs(os.path.join(f"C:\\Users\\Alaa-Ansi\\vscode\\final_project\\static\\uploads\\{session['id']}\\{name.strip()}"))    

        # finally, save the image
        image.save(os.path.join(f"C:\\Users\\Alaa-Ansi\\vscode\\final_project\\static\\uploads\\{session['id']}\\{name.strip()}", image.filename.strip()))
        

        print("image format is allowed\nimage saved")

        #----------------------------------------------------------------------#    

        # Texts section --------------------------------------------#

        # Make a proper image path for the img tag
        path = "/static/uploads/{userID}/{websiteName}/{imageName}".format(userID=session["id"], websiteName=name.strip(), imageName=image.filename.strip())
        print("image path is {p}".format(p = path))
        
        #store information in the data base
        db.execute("insert into websites(user_id, brief, imagesfn, name, link, desc, howto, path) values(?, ?, ?, ?, ?, ?, ?, ?)",
            session["id"], brief, name.strip(), name.strip(), link, description, howto, path)


        return redirect("/done")

    else:
        return render_template("add_website.html")     

@app.route("/done")
def done():
    return render_template("done.html")

@app.route("/error")
def error_t():
    # Get the error massage and the error code 
    error_massage = session["e_massage"]
    error_code = session["e_code"]

    #clear error massage and its code from session
    session["e_massage"] = ""
    session["e_code"] = ""
    print(f"after: {session['e_massage']}\n{session['e_code']}")

    return render_template("error.html", error=error_massage, error_code=error_code)

@app.route("/view", methods=["GET", "POST"]) 
def view():
    """ View the requested website recommandation information """

    # If the user reached this site via POST
    if request.method == "POST":
        # Get the requested website name and its image path
        requested_website = request.form.get("input")
        requested_website_interface = request.form.get("image_name_input")

        print(f"the image_name_input is {requested_website_interface}")
        print(f"yeah, it is {requested_website}")

        # Query the db to get all the informations about the requested website recommandation
        website = db.execute("select * from users join websites on users.id = websites.user_id where name like ?", requested_website)

        print(f"The requested website infos are {website}")
        
        return render_template("view.html", website=website)

    # else if the user reached this page via GET
    else:
        return render_template("view.html")    
        

@app.route("/search", methods=["POST"])
def search():
    """ Do a simple search algorithm """

    # Get the searched keyword
    searched = request.form.get("search").strip()
    print(f"searched-->>{searched}")

    # Query the db with searched keyword
    search_results = db.execute("select * from users join websites on users.id = websites.user_id where name like ?", searched)
    print("and the results are {results}".format(results = search_results))

    return render_template("search.html", s_results=search_results)

@app.route("/what_is_this_website_for")
def what_is_this_website_for():
    return render_template("what_is_this_website_for.html")