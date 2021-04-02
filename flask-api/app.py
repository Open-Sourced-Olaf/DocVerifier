from flask import Flask, jsonify, request, render_template

from predictor import predict

from getUrls import collect_url_links
from getPolicyText import getPolicies


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
        url_list = collect_url_links(request.get_json()["tabUrl"])  # parse as JSON
        for link in url_list:
            with open("output.txt", "a") as f:
                print(getPolicies(link), file=f)
        return "Sucesss", 200

@app.route("/predict")
def check_if_bad():
    sentence = [request.args.get('sentence')]
    if predict(sentence):
        return 'sentence is bad'
    else:
        return 'sentence is good'


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
