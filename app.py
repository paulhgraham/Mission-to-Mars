# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

# create instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")


def index():
    mars_data = mongo.db.collection.find_one()
    return render_template('index.html', mars_data=mars_data)


@app.route('/scrape')
def scrape():
    mars_data = mongo.db.mars_data
    mars_data_scrape = mission_to_mars.mars_scrape()
    mars.update(
                   {},
                   mars_data,
                   upsert=True
                   )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
