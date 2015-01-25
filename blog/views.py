import mistune

from flask import render_template, request, redirect, url_for

from blog import app
from database import session
from models import Post

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=5):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )


@app.route("/post/add", methods=["GET"])
def add_post_get():
    return render_template("add_post.html")


@app.route("/post/add", methods=["POST"])
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))


@app.route("/post/<int:post_id>", methods=["GET"])
def get_specific_post(post_id):
    post = session.query(Post)
    post = post.get(post_id)
    total_posts = session.query(Post).count()
    # Set some initial variables
    # talk to mentor about doing this better!
    has_next = 0
    has_prev = 0
    # If this isn't the last post, set has_next to the next post_id
    if post_id < total_posts:
        has_next = post_id + 1
    # If this isn't the first post, set has_prev to the previous post_id
    if post_id >= 1:
        has_prev = post_id -1

    return render_template("one_post.html", post=post,
                           has_next=has_next,
                           has_prev=has_prev)


@app.route("/post/<int:post_id>/edit", methods=["GET"])
def edit_post(post_id):
    post = session.query(Post)
    post = post.get(post_id)
    return render_template("edit_post.html", post=post)

@app.route("/post/<int:post_id>/edit", methods=["POST"])
def post_edit(post_id):
    # Get the post for the current post ID
    post = session.query(Post)
    post = post.get(post_id)
    # Get the title and content from the post
    title=request.form["title"]
    content=request.form["content"]
    # Update the post - create new session obj
    session.query(Post).filter(Post.id == post_id).update(
        {"title":title, "content":content} )
    session.commit()
    # return to the post you edited.
    # Set some initial variables
    # talk to mentor about doing this better!
    total_posts = session.query(Post).count()
    has_next = 0
    has_prev = 0
    # If this isn't the last post, set has_next to the next post_id
    if post_id < total_posts:
        has_next = post_id + 1
    # If this isn't the first post, set has_prev to the previous post_id
    if post_id >= 1:
        has_prev = post_id -1

    return render_template("one_post.html", post=post,
                           has_next=has_next,
                           has_prev=has_prev)
