from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import requests

# Create the Flask app
app = Flask(__name__)
app.secret_key = "shhhsecret"
API_KEY = ""

# Initialize the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ih2025preethi.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

# Create a Product class
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.Integer(), default=1)
    purchaseDate = db.Column(db.Integer(), nullable=False)
    purchaseDateString = db.Column(db.String(), nullable=False)
    purchaseDateDate = db.Column(db.Date, nullable=False)
    expiryDate = db.Column(db.Integer())
    expiryDateString = db.Column(db.String())
    expiryDateDate = db.Column(db.Date)
    notes = db.Column(db.String())

# Homepage
@app.route("/", methods=["GET", "POST"])
def add():
    # If getting input from the form:
    if request.method == "POST":

        # Get input
        name = request.form["new-product"]
        quantity = request.form["new-product-quantity"]
        expiryDate = request.form["new-product-expiry-date"]
        purchaseDate = request.form["new-product-purchase-date"]
        notes = request.form["new-product-notes"]

        # Set expiryDateInteger to -1
        expiryDateInteger = -1

        expiryDateDate = date.today()

        # If an expiryDate was inputted, remove the "-" from the expiryDate String and turn it into an integer
        if expiryDate != "":
            expiryDateDate = datetime.strptime(expiryDate, "%Y-%m-%d")
            expiryDateInteger = int(expiryDate.replace("-", ""))

        purchaseDateDate = datetime.strptime(purchaseDate, "%Y-%m-%d")

        # Remove the "-" from the purchaseDate String and turn it into an integer
        purchaseDateInteger = int(purchaseDate.replace("-", ""))

        # Create a Product object and add it to the database
        product = Product(name=name, quantity=quantity, expiryDate=expiryDateInteger, purchaseDate=purchaseDateInteger, notes=notes, expiryDateString=expiryDate, purchaseDateString=purchaseDate, expiryDateDate=expiryDateDate, purchaseDateDate=purchaseDateDate)
        db.session.add(product)
        db.session.commit()

    # Create a list of all the products with expiry dates
    productsWithExpiry = Product.query.filter(Product.expiryDate.isnot(-1))

    # Sort the list of products with expiry dates with the soonest expiry date on the top
    productsWithExpiry = productsWithExpiry.order_by(Product.expiryDate.asc()).all()

    # Create a list of all the products without expiry dates
    productsWithoutExpiry = Product.query.filter(Product.expiryDate.is_(-1))

    # Sort the list of products without expiry dates with the soonest purchase date on the top
    productsWithoutExpiry = productsWithoutExpiry.order_by(Product.purchaseDate.asc()).all()

    # **Print products for debugging purposes** #
    print(productsWithExpiry)
    print(productsWithoutExpiry)

    return render_template("home.html", productsWithExpiry=productsWithExpiry, productsWithoutExpiry=productsWithoutExpiry, today=date.today())

# Edit menu for the selected product
@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit(product_id):

    # Get the product based on the ID
    product = Product.query.get_or_404(product_id)

    # If getting input from the form:
    if request.method == "POST":

        # Change the values in the database
        name = request.form["edit-product"]
        quantity = request.form["edit-product-quantity"]
        expiryDate = request.form["edit-product-expiry-date"]
        purchaseDate = request.form["edit-product-purchase-date"]
        notes = request.form["edit-product-notes"]

        expiryDateInteger = -1

        if expiryDate != "":
            expiryDateInteger = int(expiryDate.replace("-", ""))

        purchaseDateInteger = int(purchaseDate.replace("-", ""))

        product.name = name
        product.quantity = quantity
        product.expiryDate = expiryDateInteger
        product.expiryDateString = expiryDate
        product.expiryDateDate = datetime.strptime(expiryDate, "%Y-%m-%d")
        product.purchaseDate = purchaseDateInteger
        product.purchaseDateString = purchaseDate
        product.purchaseDateDate = datetime.strptime(purchaseDate, "%Y-%m-%d")
        product.notes = notes

        db.session.commit()

        # Output a message to say that changes were saved
        flash("Your changes were saved!")

        return render_template("home.html")

    return render_template("editProduct.html", product=product)

# Delete a product based on the ID
@app.route("/delete/<int:product_id>", methods=["GET", "POST"])
def delete(product_id):

    # Get the product from the database based on the ID then delete it
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect("/")

# Get recipes based on selected ingredients
@app.route("/findRecipes", methods=["POST"])
def findRecipes():
    # Get the list of the products' IDs from the selected checkboxes
    selected_ids = request.form.getlist("ingredient")

    # Output an error message if the user did not pick any options
    if not selected_ids:
        flash("You must select at least one ingredient!", "error")
        return redirect("/")

    # Get the list of products using the list of the products' IDs
    products = Product.query.filter(Product.id.in_(selected_ids)).all()

    # Build ingredient list from product names
    ingredients = ",".join([p.name for p in products])

    print(ingredients)

    # Use Spoonacular API to find 5 recipes based on the ingredients
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients,
        "number": 5,
        "apiKey": API_KEY,
    }
    response = requests.get(url, params=params)
    recipeList = response.json()

    return render_template("recipes.html", recipeList=recipeList, chosen=products)


if __name__ in "__main__":
    with app.app_context():
        #db.drop_all()
        #print("Database has been cleared.")
        db.create_all()


    app.run(debug=True)
