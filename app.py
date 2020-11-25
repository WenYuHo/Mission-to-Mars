from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping


app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Home page
@app.route("/")
def index():
    # PyMongo to find the "mars" collection in our database
    mars = mongo.db.mars.find_one()   
    # index.html as home page url, mars=mars tells Python to use the collection "mars" from mongodb
    return render_template("index.html", mars=mars)

# Scrape Button
@app.route("/scrape")
def scrape():
    # points to Mongo database 
    mars = mongo.db.mars
    # referencing the scrape_all function in the scraping.py
    mars_data = scraping.scrape_all()
    # update the database.
    # need to add an empty JSON object with {} in place of the query_parameter.
    # upsert=True, create a new document if one doesn't already exist,
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"

if __name__ == "__main__":
    app.run()