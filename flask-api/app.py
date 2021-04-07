from flask import Flask, jsonify, request, render_template
import PyPDF2
from werkzeug.utils import secure_filename


from predictor import predict

from getUrls import collect_url_links
from getPolicyText import getPolicies
import os
# importing module
import logging
import re

from flask_cors import CORS, cross_origin

ROOT_FOLDER = "static/"
UPLOAD_FOLDER = ROOT_FOLDER + "uploads/"


app = Flask(__name__)  # create an app instance
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.config["UPLOADS"] = UPLOAD_FOLDER
# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')


# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Test messages
logger.debug("Harmless debug Message")
logger.info("Just an information")
logger.warning("Its a Warning")
logger.error("Did you try to divide by zero")
logger.critical("Internet is down")


@app.route("/test", methods=["GET", "POST"])
@cross_origin()
def testfn():
    # POST request
    if request.method == "POST":
        tabUrl = request.get_json()["tabUrl"]
        # tabUrl.split('/')
        # print(tabUrl)
        url_list = collect_url_links(tabUrl)  # parse as JSON
        print(url_list)
        for link in url_list:
            print(link)
            with open("output.txt", "w", encoding="utf8") as f:
                print(getPolicies(link), file=f)
                logger.info("scraping complete")
        with open("output.txt", encoding="utf8") as f:
            text = f.read()
        data = predict_text(text)
        message = {"good": data["bad"][0], "bad": data["bad"][0]}
        return jsonify(message)
    return jsonify(message)


@app.route("/uploads", methods=["POST"])
@cross_origin()
def uploads():
    # GET request
    # serialize and use JSON headers
    # POST request
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        #  uploaded_folder = create_folder_entry(app.config['UPLOAD_FOLDER'],"uploaded")
        file.save(os.path.join(app.config["UPLOADS"], "output.pdf"))
        print("File uploaded to " +
              os.path.join(app.config["UPLOADS"], filename))
        print("file", request.files["file"])
        print(request)
        logger.info("upload file done")

        #print("In upload:", pdfFileName)

        return "Sucesss", 200


@app.route("/predict", methods=["GET"])
def check_if_bad():
    with open("output.txt", encoding="utf8") as f:
        text = f.read()
    result = predict_text(text)
    return result

@app.route("/checkPDF", methods=["GET"])
def check_PDF():
    pdfFileObj = open(os.path.join(app.config["UPLOADS"], "output.pdf"), 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    fileText = ""

    for i in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        fileText += pageObj.extractText()
        
    pdfFileObj.close()

    result = predict_text(fileText)
    
    return jsonify(result)


def predict_text(textInput):
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', textInput)
    bad = []
    good = []
    output = {}
    #sentences = [sentences]
    #sentence = [request.args.get('sentence')]
    for sentence in sentences:
        # print(sentence)
        # print("\n")
        if(len(sentence) > 100):
            if predict(sentence):
                good.append(sentence)
                #print(sentence, 'sentence is bad')
            else:
                bad.append(sentence)
                #print(sentence, 'sentence is good')
    data = {'good': good, 'bad': bad}

    return data

if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
