from app import db, BlogPost, Comment, app

def init_db():
    with app.app_context():
        db.create_all()
        if not BlogPost.query.first():
            post1 = BlogPost(title="Welcome to Flask Blog", content="This is the first sample post.")
            post2 = BlogPost(title="Second Post", content="Flask works well with SQLite.")
            db.session.add_all([post1, post2])
            db.session.commit()
            # Insert sample comments, some with missing values
            c1 = Comment(post_id=post1.id, author="Alice", body="Great article!")
            c2 = Comment(post_id=post1.id, author=None, body="Author forgot to enter a name")
            c3 = Comment(post_id=post2.id, author="Bob", body=None)
            db.session.add_all([c1, c2, c3])
            db.session.commit()
            print("Database initialized with sample posts and comments.")
        else:
            print("Database already exists. No need to re-initialize.")

if __name__ == '__main__':
    init_db()
