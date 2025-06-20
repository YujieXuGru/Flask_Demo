from flask import Flask, render_template, abort, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Simple Flask blog application with SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    author = db.Column(db.String(50))
    body = db.Column(db.Text)

@app.route('/')
def index():
    posts = BlogPost.query.order_by(BlogPost.id.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = BlogPost.query.get(post_id)
    if not post:
        # Show a simple not found page, but still accept POST to trigger bug!
        if request.method == 'POST':
            # Will crash: post is None, so post.id is error!
            author = request.form.get('author')
            body = request.form.get('body')
            comment = Comment(post_id=post.id, author=author, body=body)  # bug here
            db.session.add(comment)
            db.session.commit()
        return render_template('notfound.html'), 404
    if request.method == 'POST':
        author = request.form.get('author')
        body = request.form.get('body')
        # Accept blank/None author and body, can cause weird UI and DB state!
        comment = Comment(post_id=post.id, author=author, body=body)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post_id))
    comments = post.comments
    return render_template('post.html', post=post, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)

