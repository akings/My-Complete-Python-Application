from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_bcrypt import check_password_hash, generate_password_hash
from databases import Users
from databases import Products

app = Flask(__name__)
app.secret_key = "kihohohuohohgff"


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form["x"]
        email = request.form["y"]
        password = request.form["z"]
        password = generate_password_hash(password)
        try:
            Users.create(name=name, email=email, password=password)
            flash("Account created successfully")
        except Exception:
            flash("That email is already used")
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["x"]
        password = request.form["y"]

        try:
            user = Users.get(Users.email == email)
            hashed_password = user.password
            if check_password_hash(hashed_password, password):
                flash("Login Successful")
                session["name"] = user.name
                session["email"] = user.email
                session["id"] = user.id
                session["logged_in"] = True
                return redirect(url_for("home_page"))
        except Users.DoesNotExist:
            flash("Wrong username or password")
    return render_template("login.html")


@app.route('/home')
def home_page():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route('/logout')
def logout():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route('/view_users')
def view_users():
    users = Users.select()
    return render_template("users.html", users=users)


@app.route('/delete_users/<int:id>')
def delete_user(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    Users.delete().where(Users.id == id).execute()
    flash("User Deleted Successfully")
    return redirect(url_for("view_users"))

@app.route('/update_user/<int:id>', methods=['GET','POST'])
def update_user(id):
    user = Users.get(Users.id == id)
    if request.method == 'POST':
        updated_name = request.form["x"]
        updated_email = request.form["y"]
        updated_password = request.form["z"]
        hashed_password = generate_password_hash(updated_password)
        user.name = updated_name
        user.email = updated_email
        user.password = hashed_password
        user.save()
        flash("User Updated Successfully")
        return redirect(url_for("view_users"))
    return render_template("update_User.html", user = user)

@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
    if request.method == "POST":
        product_name = request.form["jina"]
        product_quantity = request.form["wingi"]
        product_price = request.form["bei"]
        try:
            Products.create(name=product_name, quantity=product_quantity, price=product_price)
            flash("Product Added successfully")
        except Exception:
            flash("Adding product Failed")
    return render_template('add_products.html')

@app.route('/view_product')
def view_product():
    view_product = Products.select()
    return render_template("view_product.html", products=view_product)

@app.route('/delete_product/<int:id>')
def delete_product(id):
    if not session.get("logged_in"):
        return redirect(url_for("view_product"))
    Products.delete().where(Products.id == id).execute()
    flash("Product Deleted Successfully")
    return redirect(url_for("view_product"))

@app.route('/update_product/<int:id>', methods=['GET','POST'])
def update_product(id):
    view_product = Products.get(Products.id == id)
    if request.method == 'POST':
        updated_name = request.form["jina"]
        updated_quantity = request.form["wingi"]
        updated_price = request.form["bei"]
        view_product.name = updated_name
        view_product.quantity = updated_quantity
        view_product.price = updated_price
        view_product.save()
        flash("Product Updated Successfully")
        return redirect(url_for("view_product"))
    return render_template("update_Product.html", product = view_product)

if __name__ == '__main__':
    app.run()
