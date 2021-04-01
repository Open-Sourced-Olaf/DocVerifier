from flask import Flask, jsonify, request, render_template
from getUrls import collect_url_links

app = Flask(__name__)  # create an app instance


@app.route("/")  # at the end point /
def hello():  # call method hello
    return "Hello World!"  # which returns "hello world"


@app.route("/test", methods=["GET", "POST"])
def testfn():
    # GET request
    if request.method == "GET":
        message = {"greeting": "Hello from Flask!"}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == "POST":
        print(collect_url_links(request.get_json()["tabUrl"]))  # parse as JSON
        return "Sucesss", 200


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
