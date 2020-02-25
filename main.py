from werkzeug.utils import secure_filename
from flask import Flask, render_template, flash, request, redirect, jsonify
import os
import urllib.request
import uuid
import shutil

import GoogleNews as gn
import Process
import AudioFileProcess as afp
import TextFileProcess as tfp
import ImageFileProcess as ifp
import TwitterText as tt

import joblib

# import keras.backend.tensorflow_backend as tb
# tb._SYMBOLIC_SCOPE.value = True

app = Flask(__name__)
app.secret_key = "secret key"
# app.config['UPLOAD_FOLDER'] = './data'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

respMsg = {}
param = None
completeFlag = 0

# w2v_model = None
tokenizer = None
model = None
modelLoaded = False

def allowed_file(filename, fileTypeList):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in [x.lower() for x in fileTypeList]


@app.route('/')
def render_main():
    return render_template("home.html")


@app.route('/predict', methods=['POST'])
def predict():
    global respMsg
    global tokenizer
    global model
    global modelLoaded

    if not modelLoaded:
        loadModel()
        modelLoaded = True

    audioFileExtn = ['mp3', 'wav']
    imageFileExtn = ['jpg', 'jpeg', 'gif', 'png']
    textFileExtn = ['txt', 'xls', 'xlsx', 'csv']
    uploadFolder = ''
    resp = {}
    inputList = []
    emoji = ''

    prc = Process.Process(model, tokenizer)

    inSource = ''
    inNewsLang = ''
    inManualText = ''
    inTwitHashTag = ''
    inTwitDate = ''
    inTwitLimit = ''
    inFileNameList = []
    inFilesList = []
    isValid = True
    fileWithPath = ''

    # try:
    if 1==1:
        if request.method == 'POST':

            formKeys = request.form.to_dict(flat=False).keys()
            source = 'source'
            newsLang = 'newsLang'
            manualText = 'manualText'
            twitHashTag = 'twitHashTag'
            twitDate = 'twitDate'
            twitLimit = 'twitLimit'
            fileNameList = 'fileNameList'
            filesList = 'filesList'

            print('==========================================')
            print(formKeys)
            print('==========================================')

            if source in formKeys:
                inSource = request.form[source]
            if newsLang in formKeys:
                inNewsLang = request.form[newsLang]
            if manualText in formKeys:
                inManualText = request.form[manualText]
            if twitHashTag in formKeys:
                inTwitHashTag = request.form[twitHashTag]
            if twitDate in formKeys:
                inTwitDate = request.form[twitDate]
            if twitLimit in formKeys:
                inTwitLimit = request.form[twitLimit]
            if fileNameList in formKeys:
                inFileName = request.form[fileNameList]
                if filesList in request.files:
                    print('-----------------------------------------------------------------------')
                    print(request.files)
                    inFilesList = request.files[filesList]
                    print(inFilesList)
                    print(inFilesList.filename)

            uid = uuid.uuid1().hex
            uploadFolder = '.\\data\\' + uid
            divider = "\\"
            fileTypeList = []
            if inSource == "News":
                pass
            elif inSource == "Audio":
                fileTypeList = audioFileExtn
            elif inSource == "Image":
                fileTypeList = imageFileExtn
            elif inSource == "File":
                fileTypeList = textFileExtn
            elif inSource == "ManualText":
                pass
            elif inSource == "Twitter":
                pass
            else:
                resp['message'] = 'Invalid option'
                isValid = False

            if isValid:
                if inSource in ['Audio', 'File', 'Image']:
                    isAllFilesValid = True
                    try:
                        os.mkdir(uploadFolder)
                    except Exception as x:
                        pass

                    if not (inFilesList and allowed_file(inFilesList.filename, fileTypeList)):
                        isAllFilesValid = False
                        resp[inFilesList.filename] = ' - Invalid file type'

                    if isAllFilesValid:
                        filename = secure_filename(inFilesList.filename)
                        fileWithPath = uploadFolder + divider + filename
                        inFilesList.save(os.path.join(uploadFolder, filename))

                print('---->'+fileWithPath)

                if inSource == 'News':
                    inputList, newsEnList = gn.getNews(inNewsLang)
                elif inSource == 'ManualText':
                    inputList.append(inManualText)
                elif inSource == 'Audio':
                    inputList.append(afp.extractTextFromAudio(fileWithPath))
                elif inSource == 'Image':
                    inputList.append(ifp.extractTextFromImage(fileWithPath))
                elif inSource == 'File':
                    inputList = tfp.extractTextFromTextFile(fileWithPath)
                elif inSource == 'Twitter':
                    inputList = tt.pullTweets(inTwitHashTag, inTwitDate, inTwitLimit)

                cleanedInputList = [prc.cleanText(x) for x in inputList]
                outputList = [prc.predict(x) for x in cleanedInputList]

            resp['inputList'] = inputList
            resp['outputList'] = outputList
    # except Exception:
    #     resp['message'] = 'ERROR in prediction'

    if inSource in ['Audio', 'File', 'Image']:
        try:
            shutil.rmtree(uploadFolder)
            print('Deleted folder - ' + uploadFolder)
        except Exception:
            pass

    resp = jsonify(resp)
    resp.status_code = 200
    return resp


def loadModel():
    # global w2v_model
    global tokenizer
    global model
    # w2v_model = joblib.load('word2vec.pkl')
    tokenizer = joblib.load('./modelDump/tokenizer_X_train_v2.pkl')
    model = joblib.load('./modelDump/final_model_cnn_v2.pkl')


if __name__ == '__main__':
    app.run(threaded=False)