from datetime import datetime
from app import app,photos,db
from models import User,Tweet,followers
from forms import RegisterForm,LoginForm,TweetForm
from flask import render_template,request,redirect,url_for,abort
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,login_user,login_required,current_user,logout_user
# from flask_uploads import UploadSet,IMAGES,configure_uploads,UploadNotAllowed,ALL

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=['GET'])
def index():
    form = LoginForm()
    return render_template('index.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            return 'Login failed'
        if check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('profile'))
        return 'Login failed'
    return redirect(url_for('index'))

@app.route('/profile',defaults={'username':None})
@app.route('/profile/<username>')
@login_required
def profile(username):
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
    else:
        user = current_user
    followed_by = user.followed_by.all()
    # tweets = Tweet.query.filter_by(user=user).order_by(Tweet.date_created.desc()).all()
    tweets = Tweet.query.join(followers,(followers.c.followee_id == Tweet.user_id)).filter(followers.c.follower_id == current_user.id).order_by(Tweet.date_created.desc()).all()

    current_time = datetime.now()

    display_follow = True
    if current_user == user:
        display_follow = False
    elif current_user in followed_by:
        display_follow = False

    return render_template('profile.html',current_user=user,tweets=tweets,
                            current_time=current_time,followed_by=followed_by,
                            display_follow=display_follow)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/timeline',defaults={'username':None})
@app.route('/timeline/<username>')
def timeline(username):
    form = TweetForm()
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
        user_id = user.id
    else:
        user = current_user
        user_id = current_user.id

    tweets = Tweet.query.filter_by(user_id=user_id).order_by(Tweet.date_created.desc()).all()
    current_time = datetime.now()
    total_tweets = len(tweets)
    return render_template('timeline.html',form=form,tweets=tweets,
                            current_user=user,current_time=current_time,
                            total_tweets=total_tweets)

@app.route('/post_tweet',methods=['GET','POST'])
def post_tweet():
    form = TweetForm()
    if form.validate():
        tweet = Tweet(user_id=current_user.id,text=form.text.data,date_created=datetime.now())
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for('timeline'))

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        filename = None
        if 'file' not in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = photos.save(form.image.data,name=request.files['image'].filename)
        new_user = User(name=form.name.data,
                username=form.username.data,
                image=filename,
                password=generate_password_hash(form.password.data),
                join_date=datetime.now()
                )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('profile'))
    return render_template('register.html',form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()
    current_user.following.append(user_to_follow)
    db.session.commit()
    return redirect(url_for('profile'))