import time
from flask import Flask, request
from resnet50 import predict

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def root():
  if (request.method == "GET"):
    return '''
      <!doctype html>
      <title>Upload new File</title>
      <h1>Upload new File</h1>
      <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
      </form>
      '''
  elif (request.method == "POST"):
    file = request.files["file"]
    file.save("/{}".format(file.filename))
    start = time.time()
    print(predict(file.filename))
    return str(time.time() - start)
  else:
    return "Unknown"