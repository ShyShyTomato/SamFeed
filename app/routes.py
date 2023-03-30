from app import app, db, models, forms

from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_manager, current_user
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

        user = models.User.query.filter_by(username=loginForm.username.data).first()
        #If the user exists
        if user:
            print("user exists")
            #If the password is correct
            if user.password == loginForm.password.data:
                print("password correct")
                login_user(user)
                flash('Logged in successfully.')
                return render_template('user.html')
            else:
                flash("you suck, get the password right")
        else:
            flash("you suck, try again")

    return render_template('login.html', form=loginForm)

@app.route('/register/', methods=('GET', 'POST'))
def register():
    return render_template('register.html')

@app.route('/user/', methods=('GET', 'POST'))
def userPage():
    # Check if user is logged in
    if not current_user.is_authenticated:
        flash("You need to log in first")
        return redirect(url_for('login'))
    else:
        return render_template('user.html')

@app.route('/logout/')
def logout():
    # Logout the user
    logout_user()
    return render_template('accounts.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
