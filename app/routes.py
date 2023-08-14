from app import app, db, models, forms
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_manager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

# Check if text is malicious


def checkText(contentToCheck):
    """
    This function checks if the text is malicious or too long.
    """
    contentlist = contentToCheck.split()
    for word in contentlist:
        if len(word) > 50:
            return False
    if len(contentToCheck) > 500:
        return False
    return True

# Management for calculating the number of pages for the post viewer.


def calculatePages():
    post = db.session.query(models.Post).all()
    post.reverse()
    # If there is under 11 posts, there is only one page.
    if len(post) < 11:
        return 1
    # Count how many pages there are.
    numPages = len(post)/10
    if numPages % 10 != 0:
        numPages += 1
    numPages = numPages.__floor__()
    return numPages


# Login manager to load users from the database.


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@app.route('/', methods=('GET', 'POST'))
def home():
    """The homepage displays the 10 newest posts."""

    # Sort out flairs for the sorting system.
    flairs = models.Flair.query.all()
    flairs.append(models.Flair(name='All'))
    # Create the form
    sortByForm = forms.sortByForm()
    # Add flairs to the flairs form field, so users can choose a flair.
    for flair in flairs:
        sortByForm.flairs.choices.append((flair.name))

    # If the form is submitted, then redirect to the sort page.
    if sortByForm.validate_on_submit():
        # If flairs is all, then ignore flairs.
        if sortByForm.flairs.data == 'All':
            return redirect(url_for('sort', post_id=0, flair_id=0, user_id=sortByForm.userID.data))
        if sortByForm.userID.data == 0 or None:
            return redirect(url_for('sort', post_id=0, flair_id=models.Flair.query.filter_by(name=sortByForm.flairs.data).first().id, user_id=0))
        return redirect(url_for('sort', post_id=0, flair_id=models.Flair.query.filter_by(name=sortByForm.flairs.data).first().id, user_id=sortByForm.userID.data))

    # Draw all posts from the database.
    post = db.session.query(models.Post).all()
    # Reverse the post order so the newest post is at the top.
    post.reverse()
    # Make the posts displayed on the front page the newest 10.
    post = post[0:10]
    # Check whether the user is a superuser, and if they are, grant them unlimited power.
    if current_user.is_authenticated:
        if current_user.superuser:
            return render_template('home.html', title='Home', posts=post, nextpage=1, prevpage=-1, totalpages=calculatePages(), lastPage=True if calculatePages() == 1 else False, superuser=True, Flairs=models.Flair.query.all(), form=sortByForm)

    # If there is only one page, then make sure that there is no next page button.
    return render_template('home.html', title='Home', posts=post, nextpage=1, prevpage=-1, totalpages=calculatePages(), lastPage=True if calculatePages() == 1 else False, superuser=False, Flairs=models.Flair.query.all(), form=sortByForm)


@app.route('/<int:post_id>')
def postViewer(post_id):
    """The postviewer displays posts past the first 10."""

    # The post viewer is a bit of a mess, but it works. I'll clean it up later.
    post = db.session.query(models.Post).all()
    # Reverse the post order so the newest post is at the top.
    post.reverse()
    # Display 10 posts in order of newest.
    post = post[(10*post_id):((10*post_id)+10)]
    print("There are " + str(calculatePages()) + " page(s).")
    # If the user is on the last page, don't display a next page button.
    if post_id == calculatePages()-1:
        return render_template('home.html', title='Home', posts=post, nextpage=post_id+1, prevpage=post_id-1, totalpages=calculatePages(), lastPage=True, Flairs=models.Flair.query.all())
    # If the inputted page number is over the number of pages, display a 404.
    if post_id > calculatePages()-1:
        return render_template('404.html')
    return render_template('home.html', title='Home', posts=post, nextpage=post_id+1, prevpage=post_id-1, totalpages=calculatePages(), Flairs=models.Flair.query.all())


@app.route('/about/', methods=('GET', 'POST'))
def about():
    """ The about page."""
    return render_template('about.html')


@app.route('/login/', methods=('GET', 'POST'))
def login():
    login_form = forms.loginForm()
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
                return redirect(url_for('userPage'))
            else:
                flash("you suck, get the password right")
        else:
            flash("you suck, try again")

    return render_template('login.html', form=login_form)





@app.route('/register/', methods=('GET', 'POST'))
def register():
    """This page is for letting a user register."""
    registerForm = forms.registerForm()
    if registerForm.validate_on_submit():
        # Register and validate the user.
        # Check the username
        if not checkText(registerForm.username.data):
            flash('Please don\'t make your username too long.')
            return render_template('register.html', form=registerForm)
        # Check if the username is already being used
        if models.User.query.filter_by(username=registerForm.username.data).first():
            flash('This username is already in use.')
            return render_template('register.html', form=registerForm)

        # Check the password
        if not checkText(registerForm.password.data):
            flash('Please don\'t make your password too long.')
            return render_template('register.html', form=registerForm)

        # Check if the email is unique before registration.
        if models.User.query.filter_by(email=registerForm.email.data).first():
            flash('This email is already in use.')
            return render_template('register.html', form=registerForm)
        if not checkText(registerForm.email.data):
            flash('Please don\'t make your email too long.')
            return render_template('register.html', form=registerForm)

        print('User tried to register')
        print('Username: ' + registerForm.username.data)
        print('Email: ' + registerForm.email.data)
        # Flask Login Register
        # Password hashing
        password = models.generate_password_hash(
            registerForm.password.data, method='sha256')
        user = models.User(username=registerForm.username.data,
                           password=password, email=registerForm.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully.')
        # return render_template('user.html')
    else:
        print('User tried to register')
        flash('Failed to register.')
    return render_template('register.html', form=registerForm)





@app.route('/user/', methods=('GET', 'POST'))
def userPage():
    """The userPage is for managing a users account settings."""
    # Check if user is logged in
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # Create the bio form and make the default value the user's current bio
    bioForm = forms.bioForm(data={'text': current_user.bio})

    # Check if the user is trying to update their bio
    if request.method == 'POST' and bioForm.validate_on_submit():
        # Update the user's bio
        updatedBio = bioForm.text.data
        user = models.User.query.filter_by(
            username=current_user.username).first()
        user.bio = updatedBio
        # Overwrite the user bio
        db.session.add(user)
        db.session.commit()
        flash('Bio updated successfully.')
        forms.bioForm.default = current_user.bio
        return render_template('user.html', form=bioForm, user=current_user, defaultBio=current_user.bio)

    else:
        if bioForm.errors:
            flash("Bio update failed.")
        forms.bioForm.default = current_user.bio
        return render_template('user.html', form=bioForm, user=current_user, defaultBio=current_user.bio)


@app.route('/logout/')
def logout():
    # Logout the user
    logout_user()
    return render_template('accounts.html')


@app.route('/post/', methods=('GET', 'POST'))
def post():
    postForm = forms.postForm()
    # Name confusion here is what was stopping me from getting everything working correctly.
    flairs = models.Flair.query.all()

    # Add flairs to the flairs form field, so users can choose a flair.
    for flair in flairs:
        postForm.flairs.choices.append((flair.name))

    # If the user isn't logged in, redirect them to the login page.
    if not current_user.is_authenticated:
        flash("You need to be logged in to post.")
        return redirect(url_for('login'))

    if postForm.validate_on_submit():
        # Register and validate the user.
        print('User tried to post')
        print('Content: ' + postForm.text.data)
        selectedFlairsString = ''
        selectedFlairs = postForm.flairs.data
        # Print the selected flairs in the console.
        for flair in selectedFlairs:
            selectedFlairsString = selectedFlairsString + flair + ', '
        print('Flairs: ' + str(selectedFlairsString))

        if checkText(postForm.text.data) == False:
            flash("You can't post that")
            return render_template('createpost.html', form=postForm, flairs=models.Flair.query.all())

        # Add the post to the database.
        post = models.Post(text=postForm.text.data, userID=current_user.id)

        # Check the ID of the flairs selected and add them to the database.
        for flair in selectedFlairs:
            flairID = models.Flair.query.filter_by(name=flair).first()
            post.flairs.append(flairID)
        db.session.add(post)
        db.session.commit()
        flash('Posted successfully.')
        # Add the flair id to the flairs joining table
        return redirect(url_for('home'))
    return render_template('createpost.html', form=postForm, flairs=models.Flair.query.all())


@app.route('/deletepost/<int:post_id>', methods=('GET', 'POST'))
def deletePost(post_id):
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
    # If the user isn't logged in, redirect them to the login page.
    if not current_user.is_authenticated:
        flash("You need to be logged in to view your profile.")
        return redirect(url_for('login'))
    # Get the user from the database.
    selectedUser = models.User.query.filter_by(id=current_user.id).first()
    # Set the bio
    bio = selectedUser.bio
    if selectedUser.bio is None:
        bio = 'This user hasn\'t set a bio yet.'
    # If the user is a superuser, then add a little note saying that they're a superuser.
    if selectedUser.superuser is True:
        superuser = True
    else:
        superuser = False

    # Set the username
    selectedUsername = selectedUser.username
    return render_template('profile.html', user=selectedUsername, bio=bio, superuser=superuser)

# Profile page for a specific user.


@app.route('/profile/<int:userid>', methods=('GET', 'POST'))
def selectedProfile(userid):
    # Get the user from the database.
    selectedUser = models.User.query.filter_by(id=userid).first()
    # If there is no user for the id entered, return a 404 error.
    if not selectedUser:
        return render_template('404.html'), 404
    viewedUser = selectedUser.username
    bio = selectedUser.bio
    if selectedUser.bio is None:
        bio = 'This user hasn\'t set a bio yet.'
    if selectedUser.superuser is True:
        superuser = True
    else:
        superuser = False

    return render_template('profile.html', user=viewedUser, bio=bio, superuser=superuser)

# Editing page for editing a post.


@app.route('/editpost/<int:post_id>', methods=('GET', 'POST'))
def editPost(post_id):
    # Create the form
    editForm = forms.editForm()

    # If the user isn't logged in, redirect them to the login page.
    if not current_user.is_authenticated:
        flash("You need to be logged in to edit a post.")
        return redirect(url_for('login'))
    # Get the post from the database.
    post = models.Post.query.filter_by(id=post_id).first()
    previousText = post.text
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
        editForm.flairs.choices.append((flair.name))

    if editForm.validate_on_submit():
        print('User tried to edit post')
        print('Content: ' + editForm.text.data)
        selectedFlairsString = ''
        selectedFlairs = editForm.flairs.data
        # Print the selected flairs in the console.
        for flair in selectedFlairs:
            selectedFlairsString = selectedFlairsString + flair + ', '
        print('Flairs: ' + str(selectedFlairsString))

        if checkText(editForm.text.data) == False:
            flash("You can't post that")
            return render_template('editpost.html', form=editForm, flairs=models.Flair.query.all())

        # Add the post to the database.
        post.text = editForm.text.data
        post.flairs.clear()
        # Check the ID of the flairs selected and add them to the database.
        for flair in selectedFlairs:
            flairID = models.Flair.query.filter_by(name=flair).first()
            post.flairs.append(flairID)
        db.session.add(post)
        db.session.commit()
        flash('Post edited successfully.')
        return redirect(url_for('home'))

    return render_template('editpost.html', form=editForm, flairs=models.Flair.query.all(), previousText=previousText)


@app.route('/sort/<int:post_id>/<int:flair_id>/<int:user_id>/', methods=('GET', 'POST'))
def sort(post_id, flair_id, user_id):
    """This function sorts posts for the user to see."""
    # Create the variable for filtered posts
    filteredPosts = []
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
            for postItem in post:
                if flair_id in [flair.id for flair in postItem.flairs]:
                    filteredPosts.append(postItem)
        # If the flairID is zero, then only filter by user.
        elif flair_id == 0 and user_id != 0:
            for postItem in post:
                if user_id == postItem.userID:
                    filteredPosts.append(postItem)
        # If neither are zero, then filter by both.
        else:
            for postItem in post:
                if flair_id in [flair.id for flair in postItem.flairs] and user_id == postItem.userID:
                    filteredPosts.append(postItem)
        # If there are no posts in the list, then return a 404.
        # I should update this later to make it so that it displays a message instead of a 404.
        if len(filteredPosts) == 0:
            return render_template('404.html'), 404
    # Calculate the pages.
    print("There are " + str(calculatePages()) + " page(s).")
    # If the user is on the last page, don't display a next page button.
    if post_id == calculatePages()-1:
        return render_template('home.html', title='Home', posts=filteredPosts, 
                               nextpage=post_id+1, prevpage=post_id-1,
                               totalpages=calculatePages(), lastPage=True, Flairs=models.Flair.query.all())
    # If the inputted page number is over the number of pages, display a 404.
    if post_id > calculatePages()-1:
        return render_template('404.html')
    return render_template('home.html', title='Home', posts=filteredPosts,
                           nextpage=1, prevpage=-1, totalpages=calculatePages()-1, 
                           lastPage=True if calculatePages() == 1 or 2 else False, superuser=False)


@app.errorhandler(404)
def page_not_found(e):
    """This function is for displaying a 404 error page."""
    return render_template('404.html'), 404
