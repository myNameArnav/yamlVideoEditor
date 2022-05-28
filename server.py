from flask import Flask, redirect, render_template, request, send_file, url_for
from parser import assetList
from submit import strToYAML
import os
from editor import edit
import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017")

myDB = myClient["yamlVideoEditor"]

users = myDB.users

# from deleteFiles import deleteMedia

app = Flask(__name__)


def saveFile(yaml, name):
    file = open(name + ".yaml", "w")
    file.write(yaml)
    file.close()
    return "Success"


def readFile(name):
    file = open(name + ".yaml", "r")
    trueYAML = file.read()
    file.close()
    return trueYAML


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        x = users.find()
        for data in x:
            tempUser = data["username"]
            if username == tempUser:
                tempPass = data["password"]
                if tempPass == password:
                    return redirect(url_for("editor"))
                else:
                    return redirect(url_for("signUp"))

        return redirect(url_for("editor"))
    else:
        return render_template("login.html")


@app.route("/signUp", methods=["POST", "GET"])
def signUp():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)
        cred = {
            "username": username,
            "password": password
        }
        users.insert_one(cred)
        return redirect(url_for("login"))
    else:
        return render_template("signUp.html")


@app.route("/documentation")
def docs():
    return render_template("documentation.html")


@app.route("/editor", methods=["GET", "POST"])
def editor():
    if request.method == "POST":
        yaml = request.form["yamlConf"]
        global yamlName
        yamlName = str((yaml.split("\n"))[1])[9:-2]
        saveFile(yaml=yaml, name=yamlName)
        # fullYAML = (assetList())[3]
        return redirect(url_for("assetLoading", name=yamlName))
    else:
        return render_template("editor.html")


@app.route("/editor/<name>/assetUploading", methods=["GET", "POST"])
def assetLoading(name):
    if request.method == "POST":
        if request.files:
            dictionary = strToYAML(readFile(yamlName))
            dictionary = dictionary["Project"]["assets"]

            vid = list(dictionary["video"].keys())
            img = list(dictionary["image"].keys())
            # imgUpload = request.files["imgAsset"]
            uploadsDir = "media"

            # for hehe in range(len(vid)):

            vidCounter = 1

            for vids in vid:
                vidUpload = request.files["vidAsset" + str(vidCounter)]
                vidUpload.save(os.path.join(uploadsDir, vids))
                vidCounter += 1

            imgCounter = 1

            for imgs in img:
                imgUpload = request.files["imgAsset" + str(imgCounter)]
                imgUpload.save(os.path.join(uploadsDir, imgs))
                imgCounter += 1
            # print(vidUpload, imgUpload)
            name = yamlName
            return redirect(url_for("render", name=name))
    else:
        dictionary = strToYAML(readFile(yamlName))
        dictionary = dictionary["Project"]["assets"]
        vid = list(dictionary["video"].keys())
        img = list(dictionary["image"].keys())
        name = yamlName
        return render_template("assetLoading.html", vid=vid, img=img, name=name)


@app.route("/editor/<name>/render")
def render(name):
    cwd = os.getcwd()
    # print(cwd)
    edit(yamlName + ".yaml")
    os.chdir("../")
    dictionary = strToYAML(readFile(yamlName))
    global outputName
    outputName = str(dictionary["Project"]["export"]["outputName"])
    # deleteMedia()
    name = yamlName
    return redirect(url_for("output", name=name))


@app.route("/editor/<name>/output")
def output(name):
    name = yamlName
    file = send_file(os.path.join("media", outputName))
    return file, name


if __name__ == "__main__":
    app.run(debug=True)
