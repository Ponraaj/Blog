from flask import Flask, render_template, request
import requests
import yagmail
import config

my_mail = config.MAIL;
my_pass = config.PASS;
# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


def send_email(name, email, phone, message):
    mail_message = f"Name: {name} \n Email: {email} \n Phone: {phone} \n Message: {message}"
    with yagmail.SMTP(my_mail, my_pass) as connection:
        connection.send(to=my_mail, contents=mail_message, subject="New message")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
