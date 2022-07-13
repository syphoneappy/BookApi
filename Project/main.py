from flask import *
import json
from urllib.request import urlopen

app = Flask(__name__)

api = "https://www.googleapis.com/books/v1/volumes?q=intitle:"

@app.route("/")
def covid():
    resp = urlopen(api + "Happy")
    book_data = json.load(resp)
    volume_info = book_data["items"][0]["volumeInfo"]
    author = volume_info["authors"]
    return render_template('index.html',book_data = volume_info)



if __name__ == "__main__":
    app.run(debug=True)