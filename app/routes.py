from app import app, db, models, forms

from flask import render_template
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

# The homepage.
@app.route('/', methods=('GET', 'POST'))
def home():
    post=db.session.query(models.Post).all()
    return render_template('home.html', title='Home', user='Sam', posts=post)



# The about page.
@app.route('/about/', methods=('GET', 'POST'))
def about():
    return render_template('about.html')


@app.route('/login/', methods=('GET', 'POST'))
def login():
    loginForm = forms.loginForm()
# Print something if the user logs in
    if loginForm.validate_on_submit():
        #Login and validate the user.
        
        print('User tried to log in')
        print('Username: ' + loginForm.username.data)
        print('Password: ' + loginForm.password.data)
        # Flask Login
        
        # Authenticate user using flask forms
        try:
            # If the username is in the database, and there is a corresponding password, log in.
            if loginForm.username.data == db.session.query(models.User.username).filter_by(username=loginForm.username.data).first()[0] and loginForm.password.data == db.session.query(models.User.password).filter_by(username=loginForm.username.data).first()[0]:   
                print('User logged in')
                return render_template('user.html')
        except:
            print('User failed to log in')
            return render_template('login.html', form=loginForm)
        

        return render_template('user.html')

    return render_template('login.html', form=loginForm)

@app.route('/register/', methods=('GET', 'POST'))
def register():
    return render_template('register.html')

@app.route('/user/', methods=('GET', 'POST'))
def user():
    return render_template('user.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
