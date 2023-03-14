from app import app, db, models

from flask import render_template

# The homepage.
@app.route('/', methods=('GET', 'POST'))
def home():
    post=db.session.query(models.Post).all()
    return render_template('index.html', title='Home', user='Sam', posts=post)



# The about page.
@app.route('/about/', methods=('GET', 'POST'))
def about():
    return 'About'
