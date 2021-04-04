from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
from getUrls import collect_url_links
from getPolicyText import getPolicies
import os

from flask_cors import CORS, cross_origin

ROOT_FOLDER = "static/"
UPLOAD_FOLDER = ROOT_FOLDER + "uploads/"


app = Flask(__name__)  # create an app instance
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.config["UPLOADS"] = UPLOAD_FOLDER


@app.route("/test", methods=["GET", "POST"])
@cross_origin()
def testfn():
    # GET request
    if request.method == "GET":
        message = {"greeting": "Hello from Flask!"}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == "POST":
        url_list = collect_url_links(request.get_json()["tabUrl"])  # parse as JSON
        for link in url_list:
            with open("output.txt", "w") as f:
                print(getPolicies(link), file=f)
        return "Sucesss", 200


@app.route("/uploads", methods=["GET", "POST"])
@cross_origin()
def uploads():
    # GET request
    if request.method == "GET":
        message = {"greeting": "Hello from Flask!"}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        #  uploaded_folder = create_folder_entry(app.config['UPLOAD_FOLDER'],"uploaded")
        file.save(os.path.join(app.config["UPLOADS"], file.filename))
        print("File uploaded to " + os.path.join(app.config["UPLOADS"], filename))
        print("file", request.files["file"])
        print(request)
        return "Sucesss", 200


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
