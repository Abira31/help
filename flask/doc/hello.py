from flask import Flask,request,render_template,session,abort

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/")
def index():
    session.pop('username', None)
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    
    return 'You are not logged in'

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("hello.html",name=name)

@app.route("/user/<username>")
def show_user_profile(username):
    return f'User {username}'

@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f'Post {post_id}'

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return f'Subpath {subpath}'

@app.route("/login",methods=["GET","POST"])
def login():
    # error = None
    # if request.method == "POST":
    #     if valid_login(request.form['username'],request.form['password']):
    #         return log_the_user_in(request.form['username'])
    #     else:
    #        error = 'Invalid username/password'
    # return render_template("login.html",error=error) 
    abort(401)

@app.errorhandler(401)
def page_not_found(error):
    return 'qewqewqae',401
