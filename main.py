import random
from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, db

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET"])
def index():
    email_address = request.cookies.get("email")  # check if there is already a cookie named secret_number

    if email_address:
        user = db.query(User).filter_by(email=email_address).first()
    else:
        user = None

    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    # napravi secret number
    secret_number = random.randint(1, 30)

    # pogledaj postoji li user
    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, secret_number=secret_number)

        # save the user object into a database
        db.add(user)
        db.commit()

    # spremi userov email u cookie
    response = make_response(redirect(url_for("index")))
    response.set_cookie("email", email)

    return response

@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))

    email_address = request.cookies.get("email")

    # get user from the data base based on her/his email address
    user = db.query(User).filter_by(email=email_address).first()

    if guess == user.secret_number:
        message_correct = "Correct! The secret number is {0}".format(str(secret_number))
        return render_template("result.html", message=message_correct)

        new_secret = random.randint(1, 30)

        user.secret_number = new_secret

        db.add(user)
        db.commit()

    elif guess > user.secret_number:
        message = "Your guess is not correct... try something smaller."
        return render_template("result.html", message=message)
    elif guess < user.secret_number:
        message = "Your guess is not correct... try something bigger."

        return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run(debug=True)  # if you use the port parameter, delete it before deploying to Heroku