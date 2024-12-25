# RECIPE BOOK

Note: Completed Mar 22, 2021

#### Video Demo:  https://youtu.be/YTKjwifTwgI


## Project Description
RECIPE BOOK is a flask web application that uses the Python, HTML, and
CSS languages to create a personal recipe book for the user (me) to keep
recipes. It is designed to work on the CS50 IDE, and hence is dependent
on certain features of the IDE to run at the moment. It uses SQLite to
store information, and the sqlite3 Python module to interact with the
database. It also uses the os Python module to interact with files and
directories. Additionally, it borrows the apology() function from
the Finance problem as a simple way of indicating an error. It also
uses Bootstrap to help with styling.

#### Home page
The home page features a table with all the recipes a user has created
so far, as well as some information about each recipe. Additionally,
"edit" and "delete" buttons are provided. Clicking on text in a row
will redirect a user to the recipe page of that recipe, which will
provide the user with the recipe itself.

#### Recipe page
The recipe page can be navigated to by clicking on a recipe in one of
the many tables displaying recipes provided throughout the site. It
displays all the information of a recipe, including:
- Name of recipe
- An optional picture
- Country of origin
- Time required
- Portion size
- Difficulty
- Ingredients
- Instructions
Additionally, "edit" and "delete" buttons are provided near the top
right for users to edit and/or delete the recipe.

#### Create Recipe page
The create recipe page can be navigated to through the navigation bar
at the top of all pages on the web application. Here, the user has to
fill out a form which details all the information needed for a recipe.
Images are optional for recipes, while all other fields are required.
The user can then submit their recipe using the "Create Recipe"
button, while users who decide not to create a recipe can return to
the home page by clicking "Cancel". If a recipe is successfully
created, the user will be redirected to the newly created recipe
page after creating their recipe. Recipes are all stored inside the
recipe.db file, apart from images, which are stored as files within
an image directory in the static directory.

#### Search and Advanced Search pages
The search page allows the user to search for recipes. They can type
their search into the search bar. Clicking "Search" or enter will
then search whole recipes for the search query, and return any matching
results in a table below the search bar. Additionally, an advanced
search link is provided near the top for more detailed searches. This
page will allow users to search by category. Any number of fields in
the advanced search form can be filled out, and upon clicking "Search",
recipes will be searched by category, with results again being displayed
underneathe the search bars in a table.

#### Edit Recipe page
The edit recipe page can be navigated to through any of the "Edit"
buttons in the web application. It displays a form similar to the
create recipe page; however, the previous recipe information is
already filled in, but can be edited. Users can edit any of the
information in the form, and upon hitting "Save Changes", the user
will be redirected to the newly edited recipe page. It should be noted
that whenever a recipe is edited, the user must add in what image
they want displayed with the recipe again, even if the recipe page
originally had a image.

#### Delete Recipe page
The delete recipe page can be navigated to through any of the "Delete"
buttons in the web application. It displays a button that can be
clicked to delete a recipe, along with another button to go back home.
Additionally, it displays the recipe to be deleted beneathe. If the
"Delete" button is clicked, the recipe is then deleted from the
recipes.db database and its corresponding image is deleted from the
static directory.

## About Certain Design Choices
#### No Login Function
One design choice I made was to not include a login to my web app.
This is because I originally designed it to be used as a personal
recipe book for me. As a personal recipe book, having a login
function would simply waste a user's time. However, if I ever wanted
to have a way to create individual accounts to allow for sharing
of recipes and multiple users, having a login feature would definitely
be needed.
#### No JavaScript
Another design choice I made was to not include any JavaScript.
Admittedly, this is due to the fact that I am not very confident
in my coding skills yet, and wanted to keep my project simple to
minimize the potential of major bugs eating up a lot of time.
Additionally, I enjoy Python more than JavaScript.

#### Storing Text in the Database, While Storing Images Locally
I chose this method of file storage as I wanted to use a database for
storing information to reduce file clutter. However, I realized that
storing images in databases could be quite troublesome. Additionally,
images take up more storage space. I decided to compromise by storing
everything apart from images in the database, while storing images
locally. To link the two, I named my images after the recipe id they
were linked with, as well as storing the image file name in the
database.

## How to Run
1. Import the project directory and files inside into the CS50 IDE
2. Navigate to the project directory
3. Use the command "flask run" in the command line
4. Click on the link provided in the command line
(eg. Running on https://ide-5ef1666a74ae4314be15732d095e8fee-8080.cs50.ws/)

## Potential Improvements
#### Create a Login
This would absolutely be required if I ever wanted to expand the
userbase outside of just myself.

#### Use JavaScript
This would be helpful to make my website more user-friendly and
interactive. For example, I originally wanted to make my delete
button create a dialog box. However, that would require JavaScript.

#### Beautify the Website
The website at the moment admittedly is rather bland. Using more CSS,
the website could definitely be made to look more pretty.

## Thank You For Reading!
