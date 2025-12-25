## We Have Food at Home

## Inspiration
Sometimes people forget that they have a certain food product at home, and by the time they do remember that it exists, it's already past the expiration date. This inspired me to create a grocery manager app that sorts food products in order from earliest to latest expiry date, which allows users to decrease the amount of food that they waste.

## What it does
The user can input the name, quantity (optional), purchase date, and expiry date (optional) of a product, as well as additional notes for their own needs, such as where they stored the product. The web app creates 2 lists based on whether or not an expiry date has been specified.

For the list of products with expiry dates, it is outputted in order from earliest expiry to latest. When the expiry date of a product is 5 or fewer days away, or has already passed, the app will output a warning. 

For the list of products without expiry dates, it is outputted in order from earliest purchase date to latest.

There is also an option at the bottom of the page to get recipes with selected food items. The recipes are from Spoonacular API.

## How I built it
- The front-end of the web app was built using HTML, CSS, and JavaScript.
- I built the back-end in Python using the Flask framework, which made it easier to redirect and route URLS, and handle input from HTML forms. Moreover, I used Flask-SQLAlchemy to create a database that stores the food products’ information. 
- The recipes were generated using Spoonacular API based on which ingredients the user wanted to include.

## Challenges I ran into
- This was my first time doing a solo hackathon project. Since I only had 24 hours to complete this web app, I could not incorporate many features that I had envisioned.
- This was only my second time building a web app using Flask and SQLite, so there were many times where I could not figure out how to implement an idea, or I could not understand why some parts were not working. As a result, I spent a lot of time researching how to use these tools to ensure that everything was created safely.
- Unfortunately, I do not have much experience in using CSS so I struggled with creating a visually appealing user interface. I used ChatGPT to modify the CSS and HTML code solely to make the web app look cleaner since I did not have enough time to learn how to create all the visuals that I was hoping to have.

## Accomplishments that I'm proud of
This was my first time creating a solo hackathon project, so I am glad that I was able to code a functional web app within 24 hours that executes the main task of listing inputted foods in order of expiry date. The Spoonacular recipe generator was an extension that I had wanted to include after finishing the primary functions, and I am happy that I was able to add that in as well.

## What I learned
- How to create a SQLite database using Flask's extension Flask-SQLAlchemy. This made it very easy to manage the database without needing to know SQL. Moreover, it helped me accomplish the main function of my program to sort elements based on a certain column’s values.
- How to use Jinja2 to incorporate Python loops and conditionals within the HTML templates to meet my needs of outputting the required data.
- How to use Spoonacular API to generate information about foods and recipes.

## What's next for this project
- Modify the user interface to be more welcoming, unique, and convenient for the user. 
- Include voice commands for accessibility for users with poor vision, and overall more convenience for all users.
- Include tags so that users can organize food lists according to their needs.
- Push reminders to notify the user about upcoming expiry dates.
