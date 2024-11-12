from flask import Flask, json, request
from api.getInseratDetails import *
from api.scrapeInserate import *
from api.getViews import *

api = Flask(__name__)

# Get details from a specific listing
@api.route('/getInseratDetails', methods=['GET'])
def details():
    url = request.headers['url']
    details = getInseratDetails(url)
    return json.dumps(details)


# Get all inserate listing
@api.route('/getInserateUrls', methods=['GET'])
def urls():
    # Extract query parameters from the request
    brand = request.args.get("brand", default="")
    model = request.args.get("model", default="")
    type_ = request.args.get("type", default="")
    shiftType = request.args.get("shiftType", default="")
    hu = request.args.get("hu", default="")
    fuelType = request.args.get("fuelType", default="")
    powerFrom = request.args.get("powerFrom", default="")
    powerTo = request.args.get("powerTo", default="")
    ezFrom = request.args.get("ezFrom", default="")
    ezTo = request.args.get("ezTo", default="")
    kmFrom = request.args.get("kmFrom", default="")
    kmTo = request.args.get("kmTo", default="")
    priceFrom = request.args.get("priceFrom", default="")
    priceTo = request.args.get("priceTo", default="")
    unlistedCarModel = request.args.get("unlistedCarModel", default="")

    urls = scrapeInserateUrls(brand, model, type_, shiftType, hu, fuelType, powerFrom, powerTo, ezFrom, ezTo, kmFrom, kmTo, priceFrom, priceTo, unlistedCarModel)
    return json.dumps(urls)


# Get views from a specific listing
@api.route('/getViews', methods=['GET'])
def viewsGet():
    url = request.headers['url']
    views = getViews(url)
    return json.dumps(views)

if __name__ == '__main__':
    # from waitress import serve
    # serve(api, host="0.0.0.0", port=80)
    api.run(host="0.0.0.0", port=80
    , debug=True
    )
