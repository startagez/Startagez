from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import Story, Comment, Like
from extensions import db

stories_bp = Blueprint("stories", __name__)

@stories_bp.route("/story/new", methods=["GET", "POST"])
@login_required
def new_story():
    if request.method == "POST":
        story = Story(
            title=request.form["title"],
            body=request.form["body"],
            author_id=current_user.id
        )
        db.session.add(story)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("new_story.html")

@stories_bp.route("/story/<int:story_id>", methods=["GET", "POST"])
def view_story(story_id):
    story = Story.query.get_or_404(story_id)

    if request.method == "POST":
        comment = Comment(
            body=request.form["comment"],
            story_id=story.id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()

    comments = Comment.query.filter_by(story_id=story.id).all()
    likes = Like.query.filter_by(story_id=story.id).count()

    return render_template("story.html", story=story, comments=comments, likes=likes)

@stories_bp.route("/story/<int:story_id>/like")
@login_required
def like_story(story_id):
    like = Like(story_id=story_id, user_id=current_user.id)
    db.session.add(like)
    db.session.commit()
    return redirect(url_for("stories.view_story", story_id=story_id))
