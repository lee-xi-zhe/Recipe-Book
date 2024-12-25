from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
import os
import sqlite3

# Configure application
app = Flask(__name__)

# Allowed extensions for pictures in recipes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Path to location of folder for images
UPLOAD_FOLDER = 'static/images'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Save files (pictures) to UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set maximum file size
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024



# Home page, displays all recipes alphabetically
@app.route("/")
def index():
    con = sqlite3.connect("recipes.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    recipes = cur.execute("SELECT * FROM recipes").fetchall()
    return render_template("index.html", recipes=recipes)


# Recipe page, finds a recipe from id given by URL and displays it
@app.route("/recipe/<id>")
def recipe(id):
    con = sqlite3.connect("recipes.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    recipe = (cur.execute("SELECT * FROM recipes WHERE id = ?", (id,)).fetchall())[0]
    con.close()
    return render_template("recipe.html", recipe=recipe)


# Page to allow user to create a new recipe
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":

        con = sqlite3.connect("recipes.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # Check that form is filled out
        if not request.form.get("input-name"):
            return apology("must provide recipe name", 400)
        if not request.form.get("input-country"):
            return apology("must provide country of origin", 400)
        if not request.form.get("input-time"):
            return apology("must provide cooking time", 400)
        size = {"Serves 1-2", "Serves 2-5", "Serves 5-8", "Serves 8+"}
        if request.form.get("input-size") not in size:
            return apology("must provide valid portion size", 400)
        if not request.form.get("input-difficulty"):
            return apology("must provide recipe difficulty", 400)
        difficulties = {"Easy", "Medium", "Hard"}
        if request.form.get("input-difficulty") not in difficulties:
            return apology("must proivde valid recipe difficulty", 400)
        if not request.form.get("input-ingredients"):
            return apology("must provide recipe ingredients", 400)
        if not request.form.get("input-difficulty"):
            return apology("must provide recipe instructions", 400)

        # Check if there is an appropriate image

        # Check if file part of form exists; then get the file from the form
        if 'input-image' not in request.files:
            return apology("no file part of form detected", 400)
        image = request.files['input-image']

        # Check if file has a name (no name means no file submitted)
        if image.filename != '':

            # Inspect the file's extension
            if not allowed_file(image.filename):
                return apology("submitted file not in a valid format", 400)

        # Save text information of created recipe
        name = request.form.get("input-name")
        country = request.form.get("input-country")
        time = request.form.get("input-time")
        size = request.form.get("input-size")
        difficulty = request.form.get("input-difficulty")
        ingredients = request.form.get("input-ingredients")
        instructions = request.form.get("input-instructions")
        recipe_data = (name, country, time, size, difficulty, ingredients, instructions)
        id = cur.execute("INSERT INTO recipes(name, country, time, size, difficulty, ingredients, instructions) \
                         VALUES (?, ?, ?, ?, ?, ?, ?)", recipe_data).lastrowid
        con.commit()

        # If there is a image, change its name and save the image
        if image.filename != '':
            extension = image.filename.rsplit('.', 1)[1].lower()
            filename = str(id) +"." + extension

            # Save the file
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(path)

            cur.execute("UPDATE recipes SET image_name = ? WHERE id = ?", (filename, id))
            con.commit()
            con.close()

        # Redirect user to the created recipe page
        return redirect("/recipe/" + str(id))
    else:
        return render_template("create.html")


# Search for recipes
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        con = sqlite3.connect("recipes.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        search = "%" + request.form.get("search") + "%"
        recipes = (cur.execute("SELECT * FROM recipes WHERE name LIKE ? \
                              OR country LIKE ? OR difficulty LIKE ? \
                              OR time LIKE ? OR size LIKE ? \
                              OR ingredients LIKE ? OR instructions LIKE ?",
                              (search, search, search, search, search, search, search)).fetchall())
        con.close()
        return render_template("search.html", recipes=recipes)
    else:
        return render_template("search.html")


@app.route("/adv-search", methods=["GET", "POST"])
def adv_search():
    if request.method == "POST":

        con = sqlite3.connect("recipes.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # Append the database query for each field filled out
        database_query = "SELECT * FROM recipes WHERE name LIKE ?"
        searches = ["%" + request.form.get("search-name") + "%"]

        if request.form.get("search-country"):
            database_query = database_query + " AND country LIKE ?"
            searches.append("%" + request.form.get("search-country") + "%")
        if request.form.get("search-difficulty") != "":
            database_query = database_query + " AND difficulty LIKE ?"
            searches.append("%" + request.form.get("search-difficulty") + "%")
        if request.form.get("search-time"):
            database_query = database_query + " AND time LIKE ?"
            searches.append("%" + request.form.get("search-time") + "%")
        if request.form.get("search-size") != "":
            database_query = database_query + " AND size LIKE ?"
            searches.append("%" + request.form.get("search-size") + "%")
        if request.form.get("search-ingredients"):
            database_query = database_query + " AND ingredients LIKE ?"
            searches.append("%" + request.form.get("search-ingredients") + "%")
        if request.form.get("search-instructions"):
            database_query = database_query + " AND instructions LIKE ?"
            searches.append("%" + request.form.get("search-instructions") + "%")

        recipes = (cur.execute(database_query, tuple(searches)).fetchall())
        con.close()

        return render_template("adv-search.html", recipes=recipes)
    else:
        return render_template("adv-search.html")


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":

        con = sqlite3.connect("recipes.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # Check that form is filled out
        if not request.form.get("input-name"):
            return apology("must provide recipe name", 400)
        if not request.form.get("input-country"):
            return apology("must provide country of origin", 400)
        if not request.form.get("input-time"):
            return apology("must provide cooking time", 400)
        size = {"Serves 1-2", "Serves 2-5", "Serves 5-8", "Serves 8+"}
        if request.form.get("input-size") not in size:
            return apology("must provide valid portion size", 400)
        if not request.form.get("input-difficulty"):
            return apology("must provide recipe difficulty", 400)
        difficulties = {"Easy", "Medium", "Hard"}
        if request.form.get("input-difficulty") not in difficulties:
            return apology("must proivde valid recipe difficulty", 400)
        if not request.form.get("input-ingredients"):
            return apology("must provide recipe ingredients", 400)
        if not request.form.get("input-difficulty"):
            return apology("must provide recipe instructions", 400)

        # Check if there is an appropriate image

        # Check if file part of form exists; then get the file from the form
        if 'input-image' not in request.files:
            return apology("no file part of form detected", 400)
        image = request.files['input-image']

        # Check if file has a name (no name means no file submitted)
        if image.filename != '':

            # Inspect the file's extension
            if not allowed_file(image.filename):
                return apology("submitted file not in a valid format", 400)

        # Delete the old image
        delete_image(id)

        # Save text information of created recipe
        name = request.form.get("input-name")
        country = request.form.get("input-country")
        time = request.form.get("input-time")
        size = request.form.get("input-size")
        difficulty = request.form.get("input-difficulty")
        ingredients = request.form.get("input-ingredients")
        instructions = request.form.get("input-instructions")
        recipe_data = (name, country, time, size, difficulty, ingredients, instructions, id)
        cur.execute("UPDATE recipes SET name = ?, country = ?, time = ?, size = ?, difficulty = ?, \
                    ingredients = ?, instructions = ? WHERE id = ?", recipe_data)
        con.commit()


        # If there is a image, change its name and save the image
        if image.filename != '':
            extension = image.filename.rsplit('.', 1)[1].lower()
            filename = id +"." + extension

            # Save the file
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(path)

            cur.execute("UPDATE recipes SET image_name = ? WHERE id = ?", (filename, id))
            con.commit()
            con.close()

        return redirect("/recipe/" + id)
    else:
        con = sqlite3.connect("recipes.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        recipe = (cur.execute("SELECT * FROM recipes WHERE id LIKE ?", (id,)).fetchall())[0]
        con.close()

        return render_template("edit.html", recipe=recipe)


@app.route("/delete/<id>", methods=["GET", "POST"])
def delete(id):
    if request.method == "POST":

        con = sqlite3.connect("recipes.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        delete_image(id)

        # Delete recipe from table
        cur.execute("DELETE FROM recipes WHERE id = ?", (id,))
        con.commit()
        con.close()

        return redirect("/")
    else:
        con = sqlite3.connect("recipes.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        recipe = (cur.execute("SELECT * FROM recipes WHERE id = ?", (id,)).fetchall())[0]
        con.close()
        return render_template("delete.html", recipe=recipe)


# Apology message borrowed from pset9 Finance
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


# Function to check whether a file has the right extension (adapted from https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/)
def allowed_file(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    if extension in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


# Function to delete image
def delete_image(id):
    con = sqlite3.connect("recipes.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Delete image
    recipe = (cur.execute("SELECT * FROM recipes WHERE id = ?", (id,)).fetchall())[0]
    if recipe["image_name"] is not None:
        old_image_path = recipe["image_name"]
        old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], old_image_path)
        try:
            os.remove(old_image_path)
        except OSError as error:
            return apology("file path cannot be removed", 400)
    # Remove image name from database
    cur.execute("UPDATE recipes SET image_name = NULL WHERE id = ?", (id,))
    print("hello")
    con.commit()
    con.close()
    return