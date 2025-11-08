from flask import Flask, render_template, request, redirect, url_for
import requests

# Create a simple Flask application to retrieve memes from https://meme-api.com/gimme/wholesomememes.
app = Flask(__name__)

# Route to display a random meme
@app.route('/meme') # Will route to http://127.0.0.1:5000/meme
def show_meme():
    meme_url = title = subreddit = None
    try:
        meme = requests.get("https://meme-api.com/gimme/wholesomememes").json()
        meme_url = meme.get("url")
        title = meme.get("title")
        subreddit = meme.get("subreddit")
    except Exception:
        pass # In case of any error, meme_url, title, and subreddit will remain None

    return render_template("meme.html", meme_url=meme_url, title=title, subreddit=subreddit)

if __name__ == '__main__':
    app.run(debug=True)
