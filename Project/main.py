from flask import *
import json
from urllib.request import urlopen

app = Flask(__name__)
api = "https://www.googleapis.com/books/v1/volumes?q=filter=free-ebooks:"
apiSearch = "https://www.googleapis.com/books/v1/volumes?q=intitle:"

@app.route("/")
def covid():
    resp = urlopen(api)
    book_data = json.load(resp)
    book =  book_data["items"]
    Maps = map(lambda datum: datum['volumeInfo'], book)
    return render_template('index.html',vol = Maps)



if __name__ == "__main__":
    app.run(debug=True)