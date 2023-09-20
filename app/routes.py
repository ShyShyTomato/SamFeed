"""
Samfeed routes.py
"""

from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_manager, current_user
from app import app, db, models, forms
login_manager = LoginManager()
login_manager.init_app(app)

# Check if text is malicious


def check_text(content_to_check):
    """This function checks if the text is malicious or too long."""
    contentlist = content_to_check.split()
    for word in contentlist:
        if len(word) > 50:
            return False
    if len(content_to_check) > 500:
        return False
    return True

# Management for calculating the number of pages for the post viewer.


def calculate_pages():
    """This function calculates the number of pages for the post viewer."""
    post = db.session.query(models.Post).all()
    post.reverse()
    # If there is under 11 posts, there is only one page.
    if len(post) < 11:
        return 1
    # Count how many pages there are.
    num_pages = len(post)/10
    if num_pages % 10 != 0:
        num_pages += 1
    num_pages = num_pages.__floor__()
    return num_pages


# Login manager to load users from the database.


@login_manager.user_loader
def load_user(user_id):
    """The user loader returns a user from the database."""
    return models.User.query.get(int(user_id))


@app.route('/', methods=('GET', 'POST'))
def home():
    """The homepage displays the 10 newest posts."""

    # Sort out flairs so we can see what each post is flaired with.
    flairs = models.Flair.query.all()
    flairs.append(models.Flair(name='All'))
    # Create the form
    sort_by_form = forms.SortByForm()
    # Add flairs to the flairs form field, so users can choose a flair.
    for flair in flairs:
        sort_by_form.flairs.choices.append((flair.name))

    # If the form is submitted, then redirect to the sort page.
    if sort_by_form.validate_on_submit():
        # If flairs is all, then ignore flairs.
        if sort_by_form.flairs.data == 'All':
            return redirect(url_for('sort', post_id=0, flair_id=0, 
                                    user_id=sort_by_form.userID.data))
        if sort_by_form.userID.data == 0 or None:
            return redirect(url_for('sort', post_id=0, 
                                    flair_id=models.Flair.query.filter_by(name=sort_by_form.flairs.data).first().id,
                                    user_id=0))
        return redirect(url_for('sort', post_id=0, 
                                flair_id=models.Flair.query.filter_by(name=sort_by_form.flairs.data).first().id,
                                user_id=sort_by_form.userID.data))

    # Draw all posts from the database.
    post = db.session.query(models.Post).all()
    # Reverse the post order so the newest post is at the top.
    post.reverse()
    # Make the posts displayed on the front page the newest 10.
    post = post[0:10]
    # Check whether the user is a superuser, and if they are, grant them unlimited power.
    if current_user.is_authenticated:
        if current_user.superuser:
            return render_template('home.html', title='Home', posts=post,
                                   nextpage=1, prevpage=-1,
                                   totalpages=calculate_pages(),
                                   lastPage=True if calculate_pages() == 1 else False,
                                   superuser=True,
                                   Flairs=models.Flair.query.all(),
                                   form=sort_by_form)

    # If there is only one page, then make sure that there is no next page button.
    return render_template('home.html', title='Home', posts=post, nextpage=1, prevpage=-1, 
                           totalpages=calculate_pages(), lastPage=True if calculate_pages() == 1 else False, 
                           superuser=False, Flairs=models.Flair.query.all(), form=sort_by_form)


@app.route('/<int:post_id>')
def post_viewer(post_id):
    """The postviewer displays posts past the first 10."""

    # The post viewer is a bit of a mess, but it works. I'll clean it up later.
    post = db.session.query(models.Post).all()
    # Reverse the post order so the newest post is at the top.
    post.reverse()
    # Display 10 posts in order of newest.
    post = post[(10*post_id):((10*post_id)+10)]
    print("There are " + str(calculate_pages()) + " page(s).")
    # If the user is on the last page, don't display a next page button.
    if post_id == calculate_pages()-1:
        return render_template('home.html', title='Home', posts=post, nextpage=post_id+1, prevpage=post_id-1, 
                               totalpages=calculate_pages(), lastPage=True, Flairs=models.Flair.query.all())
    # If the inputted page number is over the number of pages, display a 404.
    if post_id > calculate_pages()-1:
        return render_template('404.html')
    return render_template('home.html', title='Home', posts=post, nextpage=post_id+1,
                            prevpage=post_id-1, totalpages=calculate_pages(), Flairs=models.Flair.query.all())


@app.route('/about/', methods=('GET', 'POST'))
def about():
    """ The about page."""
    return render_template('about.html')


@app.route('/login/', methods=('GET', 'POST'))
def login():
    """The login page allows a user to login to their profile."""
    login_form = forms.LoginForm()
    # Print something if the user logs in
    if login_form.validate_on_submit():
        # Login and validate the user.
        print('User tried to log in')
        print('Username: ' + login_form.username.data)
        # Flask Login
        user = models.User.query.filter_by(
            username=login_form.username.data).first()
        # If the user exists
        if user:
            print("user exists")
            # If the password hash is correct
            if models.check_password_hash(user.password, login_form.password.data):
                print("password correct")
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('user_page'))
            else:
                flash("you suck, get the password right")
        else:
            flash("you suck, try again")

    return render_template('login.html', form=login_form)





@app.route('/register/', methods=('GET', 'POST'))
def register():
    """This page is for letting a user register."""
    register_form = forms.RegisterForm()
    if register_form.validate_on_submit():
        # Register and validate the user.
        # Check the username
        if not check_text(register_form.username.data):
            flash('Please don\'t make your username too long.')
            return render_template('register.html', form=register_form)
        # Check if the username is already being used
        if models.User.query.filter_by(username=register_form.username.data).first():
            flash('This username is already in use.')
            return render_template('register.html', form=register_form)

        # Check the password
        if not check_text(register_form.password.data):
            flash('Please don\'t make your password too long.')
            return render_template('register.html', form=register_form)

        # Check if the email is unique before registration.
        if models.User.query.filter_by(email=register_form.email.data).first():
            flash('This email is already in use.')
            return render_template('register.html', form=register_form)
        if not check_text(register_form.email.data):
            flash('Please don\'t make your email too long.')
            return render_template('register.html', form=register_form)

        print('User tried to register')
        print('Username: ' + register_form.username.data)
        print('Email: ' + register_form.email.data)
        # Flask Login Register
        # Password hashing
        password = models.generate_password_hash(
            register_form.password.data, method='sha256')
        user = models.User(username=register_form.username.data,
                           password=password, email=register_form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully.')
        # return render_template('user.html')
    else:
        print('User tried to register')
        flash('Failed to register.')
    return render_template('register.html', form=register_form)





@app.route('/user/', methods=('GET', 'POST'))
def user_page():
    """The user_page is for managing a users account settings."""
    # Check if user is logged in
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # Create the bio form and make the default value the user's current bio
    bio_form = forms.BioForm(data={'text': current_user.bio})

    # Check if the user is trying to update their bio
    if request.method == 'POST' and bio_form.validate_on_submit():
        # Update the user's bio
        updated_bio = bio_form.text.data
        user = models.User.query.filter_by(
            username=current_user.username).first()
        user.bio = updated_bio
        # Overwrite the user bio
        db.session.add(user)
        db.session.commit()
        flash('Bio updated successfully.')
        forms.BioForm.default = current_user.bio
        return render_template('user.html', form=bio_form, user=current_user,
                                defaultBio=current_user.bio)

    else:
        if bio_form.errors:
            flash("Bio update failed.")
        forms.BioForm.default = current_user.bio
        return render_template('user.html', form=bio_form, user=current_user,
                                defaultBio=current_user.bio)


@app.route('/logout/')
def logout():
    """The logout page logs the user out."""
    # Logout the user
    logout_user()
    return render_template('accounts.html')


@app.route('/post/', methods=('GET', 'POST'))
def post():
    """The post page is for creating a post."""
    post_form = forms.PostForm()
    # Name confusion here is what was stopping me from getting everything working correctly.
    flairs = models.Flair.query.all()

    # Add flairs to the flairs form field, so users can choose a flair.
    for flair in flairs:
        post_form.flairs.choices.append((flair.name))

    # If the user isn't logged in, redirect them to the login page.
    if not current_user.is_authenticated:
        flash("You need to be logged in to post.")
        return redirect(url_for('login'))

    if post_form.validate_on_submit():
        # Register and validate the user.
        print('User tried to post')
        print('Content: ' + post_form.text.data)
        selected_flairs_string = ''
        selected_flairs = post_form.flairs.data
        # Print the selected flairs in the console.
        for flair in selected_flairs:
            selected_flairs_string = selected_flairs_string + flair + ', '
        print('Flairs: ' + str(selected_flairs_string))

        if check_text(post_form.text.data) is False:
            flash("You can't post that")
            return render_template('createpost.html', form=post_form, 
                                   flairs=models.Flair.query.all())

        # Add the post to the database.
        post = models.Post(text=post_form.text.data, userID=current_user.id)

        # Check the ID of the flairs selected and add them to the database.
        for flair in selected_flairs:
            flair_id = models.Flair.query.filter_by(name=flair).first()
            post.flairs.append(flair_id)
        db.session.add(post)
        db.session.commit()
        flash('Posted successfully.')
        # Add the flair id to the flairs joining table
        return redirect(url_for('home'))
    return render_template('createpost.html', form=post_form, flairs=models.Flair.query.all())


@app.route('/deletepost/<int:post_id>', methods=('GET', 'POST'))
def delete_post(post_id):
    """This function deletes a post."""
    # If the user isn't logged in, redirect them to the login page.
    if not current_user.is_authenticated:
        flash("You need to be logged in to delete a post.")
        return redirect(url_for('login'))
    # Get the post from the database.
    post = models.Post.query.filter_by(id=post_id).first()
    # Check that the post exists.
    if not post:
        flash("That post doesn't exist.")
        return redirect(url_for('home'))
    # If the user isn't the owner of the post, redirect them to the home page.
    if post.userID != current_user.id and not current_user.superuser is True:
        flash("You can't delete that post.")
        return redirect(url_for('home'))
    # Delete the post from the database.
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully.')
    return redirect(url_for('home'))


# Profile page for the currently logged in user.
@app.route('/profile/', methods=('GET', 'POST'))
def profile():
    """This function displays the profile
    page for the currently logged in user."""
    # If the user isn't logged in, redirect them to the login page.
    if not current_user.is_authenticated:
        flash("You need to be logged in to view your profile.")
        return redirect(url_for('login'))
    # Get the user from the database.
    selected_user = models.User.query.filter_by(id=current_user.id).first()
    # Set the bio
    bio = selected_user.bio
    if selected_user.bio is None:
        bio = 'This user hasn\'t set a bio yet.'
    # If the user is a superuser,
    # Then add a little note saying that they're a superuser.
    if selected_user.superuser is True:
        superuser = True
    else:
        superuser = False

    # Set the username
    selected_username = selected_user.username
    return render_template('profile.html', user=selected_username, bio=bio,
                           superuser=superuser)

# Profile page for a specific user.


@app.route('/profile/<int:userid>', methods=('GET', 'POST'))
def selected_profile(userid):
    """This function displays the profile page for a specific user."""
    # Get the user from the database.
    selected_user = models.User.query.filter_by(id=userid).first()
    # If there is no user for the id entered, return a 404 error.
    if not selected_user:
        return render_template('404.html'), 404
    viewed_user = selected_user.username
    bio = selected_user.bio
    if selected_user.bio is None:
        bio = 'This user hasn\'t set a bio yet.'
    if selected_user.superuser is True:
        superuser = True
    else:
        superuser = False

    return render_template('profile.html', user=viewed_user,
                           bio=bio, superuser=superuser)

# Editing page for editing a post.


@app.route('/editpost/<int:post_id>', methods=('GET', 'POST'))
def edit_post(post_id):
    """This function displays the edit post page."""
    # Create the form
    edit_form = forms.EditForm()

    # If the user isn't logged in, redirect them to the login page.
    if not current_user.is_authenticated:
        flash("You need to be logged in to edit a post.")
        return redirect(url_for('login'))
    # Get the post from the database.
    post = models.Post.query.filter_by(id=post_id).first()
    previous_text = post.text
    # Check that the post exists.
    if not post:
        flash("That post doesn't exist.")
        return redirect(url_for('home'))
    # If the user isn't the owner of the post, redirect them to the home page.
    if post.userID != current_user.id and not current_user.superuser:
        flash("You can't edit that post.")
        return redirect(url_for('home'))

    # Set the flairs
    flairs = models.Flair.query.all()
    for flair in flairs:
        edit_form.flairs.choices.append((flair.name))

    if edit_form.validate_on_submit():
        print('User tried to edit post')
        print('Content: ' + edit_form.text.data)
        selected_flairs_string = ''
        selected_flairs = edit_form.flairs.data
        # Print the selected flairs in the console.
        for flair in selected_flairs:
            selected_flairs_string = selected_flairs_string + flair + ', '
        print('Flairs: ' + str(selected_flairs_string))

        if check_text(edit_form.text.data) is False:
            flash("You can't post that")
            return render_template('editpost.html', form=edit_form, flairs=models.Flair.query.all())

        # Add the post to the database.
        post.text = edit_form.text.data
        post.flairs.clear()
        # Check the ID of the flairs selected and add them to the database.
        for flair in selected_flairs:
            flair_id = models.Flair.query.filter_by(name=flair).first()
            post.flairs.append(flair_id)
        db.session.add(post)
        db.session.commit()
        flash('Post edited successfully.')
        return redirect(url_for('home'))

    return render_template('editpost.html', form=edit_form, flairs=models.Flair.query.all(), 
                           PreviousText=previous_text)


@app.route('/sort/<int:post_id>/<int:flair_id>/<int:user_id>/', methods=('GET', 'POST'))
def sort(post_id, flair_id, user_id):
    """This function sorts posts for the user to see."""
    # Create the variable for filtered posts
    filtered_posts = []
    # If the flair ID is 0 and the user ID is 0, then return a 404.
    if flair_id == 0 and user_id == 0:
        return render_template('404.html'), 404

    # Query everything, including the posts that aren't needed
    post = db.session.query(models.Post).all()
    # Reverse the post order so the newest post is at the top.
    post.reverse()
    # Display 10 posts in order of newest.
    post = post[(10*post_id):((10*post_id)+10)]
    # Remove all the posts that don't have the selected flair.
    if flair_id != 0 or user_id != 0:
        # If the userID is zero, then only filter by flair.
        if user_id == 0 and flair_id != 0:
            for post_item in post:
                if flair_id in [flair.id for flair in post_item.flairs]:
                    filtered_posts.append(post_item)
        # If the flair_id is zero, then only filter by user.
        elif flair_id == 0 and user_id != 0:
            for post_item in post:
                if user_id == post_item.userID:
                    filtered_posts.append(post_item)
        # If neither are zero, then filter by both.
        else:
            for post_item in post:
                if flair_id in [flair.id for flair in post_item.flairs] and user_id == post_item.userID:
                    filtered_posts.append(post_item)
        # If there are no posts in the list, then return a 404.
        # I should update this later to make it so that it
        # displays a message instead of a 404.
        if len(filtered_posts) == 0:
            return render_template('404.html'), 404
    # Calculate the pages.
    print("There are " + str(calculate_pages()) + " page(s).")
    # If the user is on the last page, don't display a next page button.
    if post_id == calculate_pages()-1:
        return render_template('home.html', title='Home', posts=filtered_posts, 
                               nextpage=post_id+1, prevpage=post_id-1,
                               totalpages=calculate_pages(), lastPage=True,
                               Flairs=models.Flair.query.all())
    # If the inputted page number is over the number of pages, display a 404.
    if post_id > calculate_pages()-1:
        return render_template('404.html')
    return render_template('home.html', title='Home', posts=filtered_posts,
                           nextpage=1, prevpage=-1, totalpages=calculate_pages()-1,
                           lastPage=True if calculate_pages() == 1 or 2
                           else False, superuser=False)


@app.errorhandler(404)
def page_not_found(e):
    """This function is for displaying a 404 error page."""
    return render_template('404.html'), 404
