from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Portfolio(db.Model):
    __tablename__ = "portfolios"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    thumb_image_url = db.Column(db.String(200), nullable=False)
    thumb_image_id = db.Column(db.String(200), nullable=False)
    banner_image_url = db.Column(db.String(200), nullable=False)
    banner_image_id = db.Column(db.String(200), nullable=False)
    logo_url = db.Column(db.String(200), nullable=False)
    logo_id = db.Column(db.String(200), nullable=False)

    def __init__(self, name, description, url, category, position, thumb_image_id, thumb_image_url, banner_image_id, banner_image_url, logo_id, logo_url):
        self.name = name
        self.description = description
        self.url = url
        self.category = category
        self.position = position
        self.thumb_image_id = thumb_image_id
        self.thumb_image_url = thumb_image_url
        self.banner_image_id = banner_image_id
        self.banner_image_url = banner_image_url
        self.logo_id = logo_id
        self.logo_url = logo_url

class PortfolioSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "url", "category", "position", "thumb_image_id", "thumb_image_url", "banner_image_id", "banner_image_url", "logo_id", "logo_url")

portfolio_schema = PortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)

@app.route("/")
def hello():
    return "Hello Trent!"

@app.route("/api/v1/portfolio", methods=["POST"])
def add_portfolio():
    name = request.json["name"]
    description = request.json["description"]
    url = request.json["url"]
    category = request.json["category"]
    position = request.json["position"]
    thumb_image_id = request.json["thumb_image_id"]
    thumb_image_url = request.json["thumb_image_url"]
    banner_image_id = request.json["banner_image_id"]
    banner_image_url = request.json["banner_image_url"]
    logo_id = request.json["logo_id"]
    logo_url = request.json["logo_url"]
    
    new_portfolio = Portfolio(name, description, url, category, position, thumb_image_id, thumb_image_url, banner_image_id, banner_image_url, logo_id, logo_url)

    db.session.add(new_portfolio)
    db.session.commit()

    portfolio = Portfolio.query.get(new_portfolio.id)
    return portfolio_schema.jsonify(portfolio)

@app.route("/api/v1/portfolios", methods=["GET"])
def add_portfolios():
    all_portfolios = Portfolio.query.all()
    result = portfolios_schema.dump(all_portfolios)

    return jsonify(result)

@app.route("/api/v1/portfolio/<id>", methods=["PATCH"])
def update_portfolio(id):
    portfolio = Portfolio.query.get(id)

    new_name = request.json["name"]
    new_description = request.json["description"]
    new_url = request.json["url"]
    new_category = request.json["category"]
    new_position = request.json["position"]
    new_thumb_image_id = request.json["thumb_image_id"]
    new_thumb_image_url = request.json["thumb_image_url"]
    new_banner_image_id = request.json["banner_image_id"]
    new_banner_image_url = request.json["banner_image_url"]
    new_logo_id = request.json["logo_id"]
    new_logo_url = request.json ["logo_url"]

    portfolio.name = new_name    
    portfolio.description = new_description
    portfolio.url = new_url
    portfolio.category = new_category
    portfolio.position = new_position
    portfolio.thumb_image_id = new_thumb_image_id
    portfolio.thumb_image_url = new_thumb_image_url
    portfolio.banner_image_id = new_banner_image_id
    portfolio.banner_image_url = new_banner_image_url
    portfolio.logo_id = new_logo_id
    portfolio.logo_url = new_logo_url

    db.session.commit()
    return portfolio_schema.jsonify(portfolio)

@app.route("/api/v1/portfolio/<id>", methods=["DELETE"])
def delete_portfolio(id):
    portfolio = Portfolio.query.get(id)
    db.session.delete(portfolio)
    db.session.commit()
    # Cloud.api.delete_resources([portfolio.thumb_image_id])
    # Cloud.api.delete_resources([portfolio.banner_image_id])
    # Cloud.api.delete_resources([portfolio.logo_id])

    return jsonify("Portfolio Item GONE!!")


if __name__ == "__main__":
    app.debug = True 
    app.run()