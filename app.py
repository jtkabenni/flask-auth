from flask import Flask, render_template, redirect, jsonify, request, session, flash
from models import User, db, connect_db, Feedback
from forms import RegisterUserForm, LoginUserForm, AddFeedback
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth-users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "verysecret"
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)

@app.route('/')
def home_page():
    users = User.query.all()
    return render_template('index.html', users = users)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.username
        flash('Welcome! Successfully Created Your Account!')
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!")
            session['user_id'] = user.username
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def display_user(username):
  if "user_id" not in session:
      flash("Please login first!")
      return redirect('/login')
  form = AddFeedback()
  user = User.query.get_or_404(username)
  return render_template('user.html', user=user, form = form)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete user"""
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id')
    return redirect ('/')

@app.route("/users/<username>/feedback/add", methods=['GET', 'POST'])
def add_feedback(username):
    form = AddFeedback()
    status = { "form_type": "Add feedback", "action": "Add"}
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect (f'/users/{username}')
    return render_template('feedback.html', form=form, status=status)

@app.route("/feedback/<int:id>/update", methods=['GET', 'POST'])
def update_feedback(id):
    feedback = Feedback.query.filter_by(id=id).first()
    form = AddFeedback(obj=feedback)
    status = { "form_type": "Update feedback", "action":  "Save"}
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        return redirect (f'/users/{feedback.username}')
    
    return render_template('feedback.html', form=form, feedback = feedback, status=status )

@app.route('/feedback/<int:id>/delete', methods=["POST"])
def delete_feedback(id):
    """Delete feedback"""
    feedback = Feedback.query.get_or_404(id)
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    if feedback.user.username == session['user_id']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!", "info")
        return redirect('/')
    flash("You don't have permission to do that!", "danger")
    return redirect('/')

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')