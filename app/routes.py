from app import app, db
from flask import (
    request,
    jsonify,
    url_for,
    render_template,
    redirect,
    flash,
    make_response,
    session,
)
from PIL import Image
from app.defaults import Sizes
import os
from app.forms import LoginForm, PostForm
from app.models import User, Post
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

movie_list = [
    {"duration": "1:45:00", "id": 1, "name": "Harry Porter 1", "rating": 9.5},
    {"duration": "1:30:00", "id": 2, "name": "Harry Porter 2", "rating": 9.0},
]
users = []
posts = [{"title": "Post 1", "description": "This is description."}]


@app.route("/")
def index():
    print(app.config)
    return jsonify({"service": "UP"}), 200


@app.route("/movies", methods=["GET", "POST"])
def movies():
    if request.method == "GET":
        return jsonify(movie_list), 200
    else:
        new_movie = {
            "duration": request.form.get("duration"),
            "id": len(movie_list) + 1,
            "name": request.form.get("name"),
            "rating": request.form.get("rating"),
        }
        movie_list.append(new_movie)
        return jsonify(movie_list), 201


@app.route("/movie/<int:id>", methods=["GET", "PUT", "DELETE"])
def movie(id):
    requested_movie = None
    for single_movie in movie_list:
        if single_movie.get("id") == id:
            requested_movie = single_movie
            break

    if not requested_movie:
        return "Not Found", 404

    if request.method == "GET":
        return jsonify(requested_movie), 200
    elif request.method == "PUT":
        requested_movie["duration"] = request.form.get("duration")
        requested_movie["name"] = request.form.get("name")
        requested_movie["rating"] = request.form.get("rating")
        return jsonify(requested_movie), 201
    else:
        movie_list.remove(requested_movie)
        return jsonify(None), 204


@app.route("/register", methods=["GET", "POST"])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        output_sizes = [(400, 400), (400, 600), (600, 400), (600, 600)]
        email = form.email.data
        password = form.password.data
        profile_pic = form.profile_pic.data
        username = form.username.data
        base_path = os.path.join(app.config.get("UPLOADS"), username)

        # flash(f"login requested for {username} with email {email}", category="info")s
        if not os.path.isdir(base_path):
            os.mkdir(base_path)
        files = []
        for size in output_sizes:
            current_file = "/".join([base_path, "x".join([str(dim) for dim in size])])
            current_file = ".png".join([current_file, ""])
            image = Image.open(profile_pic)
            image.thumbnail(size)
            print(current_file)
            image.save(current_file)
            files.append(current_file)
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username
        response = make_response(
            redirect(url_for("user", username=session.get("username")))
        )
        print(response, session)
        return response
    return make_response(render_template("register.html", form=form))


@app.route("/user/<string:username>", methods=["GET", "POST"])
def user(username):
    if "username" in session and session["username"] == username:
        if request.method == "GET":  # show user homepage
            flash(f"Welcome {username}", "success")
            posts = db.session.query(User).filter_by(username=username).one().posts
            return render_template(
                "user.html", username=username, sizes=Sizes, posts=posts
            )
        else:
            print(request.form)
            if request.form.get("new_post"):
                response = make_response(redirect(url_for("post")))
            else:
                # handle logout
                session.pop("username")
                response = make_response(redirect(url_for("register")))
            return response
    else:
        flash(f"User {username} not logged in!!!", "danger")
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        response = make_response(render_template("login.html"))
    else:
        emailaddress = request.form.get("email")
        password = request.form.get("password")
        user_from_db = (
            db.session.query(User).filter_by(email=emailaddress).one_or_none()
        )
        if user_from_db and check_password_hash(user_from_db.password_hash, password):
            session["username"] = user_from_db.username
            response = make_response(
                redirect(url_for("user", username=session.get("username")))
            )
        else:
            flash(f"Email Address/Password Invalid!!!", "danger")
            response = make_response(render_template("login.html"))
    return response


@app.route("/post", methods=["GET", "POST"])
def post():
    form = PostForm()
    username = session.get("username")
    if username:
        if request.method == "GET":
            response = make_response(render_template("post.html", form=form))
        else:
            if form.validate_on_submit():
                title = request.form.get("title")
                content = request.form.get("content")
                user = db.session.query(User).filter_by(username=username).one_or_none()
                if not user:
                    print("User not found in database")
                else:
                    post = Post(title=title, content=content, user_id=user.id)
                    db.session.add(post)
                    db.session.commit()
                response = make_response(redirect(url_for("user", username=username)))

    else:
        flash("Please login to view this page!!!", "danger")
        response = make_response(redirect(url_for("login")))
    return response
