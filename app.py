from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

@app.route("/")
def app_root():
    return redirect(url_for("index"), code=300)
    
@app.route("/index")
def index():
    # return render_template("index")
    return "Index page"

if __name__ == "__main__":
    app.run()