from flask import Flask, jsonify, request, render_template
import PyPDF2  # package to extract text from PDF
from werkzeug.utils import secure_filename
from .model.predictor import predict_nb, predict_svm
from .scraper.getPolicyText import getPolicies
from .scraper.getUrls import collect_url_links
import os
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
logging.basicConfig(filename="logger.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')


# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Test messages
# logger.debug("Harmless debug Message")
# logger.warning("Its a Warning")
# logger.error("Did you try to divide by zero")
# logger.critical("Internet is down")
data = []


@app.route('/', methods=["GET"])
def home():
    return render_template('index.html', **locals())

# route to scrape current tab URL and then predict using the ML model


@app.route("/scrape", methods=["GET", "POST"])
@cross_origin()
def testfn():
    # POST request
    if request.method == "POST":
        tabUrl = request.get_json()["tabUrl"]
        url_list = collect_url_links(tabUrl)  # parse as JSON
        # get the current tab url
        logger.info(url_list)
        for link in url_list:
            # get the list of privacy policies
            logger.info(link)
            # write the scraped data from privacy policy page to a txt file
            with open("output.txt", "w", encoding="utf8") as f:
                print(getPolicies(link), file=f)
                logger.info("scraping complete")
        with open("output.txt", encoding="utf8") as f:
            # read the text file and make predictions
            text = f.read()
        data = predict_text(text)  # call the model
        message = {"good": data["bad"], "bad": data["bad"]}
        logger.info("prediction done")
        return jsonify(message)
    return jsonify(message)


# endpoint to upload a file to the server
@app.route("/uploads", methods=["POST"])
@cross_origin()
def uploads():
    # POST request
    if request.method == "POST":
        # get the file
        file = request.files["file"]
        # save the filename
        filename = secure_filename(file.filename)
        # save the file in the specified folder
        file.save(os.path.join(app.config["UPLOADS"], file.filename))
        # rename the file name
        os.rename(os.path.join(app.config["UPLOADS"], filename),
                  os.path.join(app.config["UPLOADS"], "output.pdf"))
        logger.info("File uploaded to " +
                    os.path.join(app.config["UPLOADS"], filename))
        logger.info("file", request.files["file"])
        logger.info(request)
        logger.info("upload file done")
    return "Sucesss", 200


# endpoint to make the predictions
@app.route("/predict", methods=["GET"])
def check_if_bad():
    model = request.args.get('model')
    with open("output.txt", encoding="utf8") as f:
        text = f.read()
    result = predict_text(text, model=model)
    result = result["bad"]
    return render_template('index.html', **locals())


# route to run the model in the PDF
@app.route("/checkPDF", methods=["GET"])
def check_PDF():
    if request.method == "GET":
        content = ""
        num_pages = 100
        pdfFileObj = open(os.path.join(
            app.config["UPLOADS"], "output.pdf"), 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        for i in range(0, num_pages):
            content += pdfReader.getPage(i).extractText() + "\n"
        content = " ".join(content.replace(u"\xa0", " ").strip().split())
        pdfFileObj.close()
        result = predict_text(content, "svm")
        global data
        data = result["good"]
        logger.info("data", data)
        logger.debug("PDF checked successfully")
        return jsonify(result)
    return jsonify(result)
 # redirect after pdf is checked


@app.route("/redirect", methods=["GET"])
def redirect():
    global data
    result = data
    logger.debug("redirected data", data)
    return render_template('index.html', **locals())

# function to predict individual sentences


def predict_text(textInput, model="svm"):
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', textInput)
    bad = []
    good = []
    output = {}
    for sentence in sentences:
      # check for number of words
        if(len(sentence) > 100):
            if model == 'nb':
                if predict_nb(sentence):
                    good.append(sentence)
                else:
                    bad.append(sentence)
            elif model == 'svm':
                if predict_svm(sentence):
                    good.append(sentence)
                else:
                    bad.append(sentence)

        data = {'good': good, 'bad': bad}  # return the result to frontend
        return data


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
