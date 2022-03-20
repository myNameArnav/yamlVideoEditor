from flask import Flask, redirect, render_template, request, url_for
from submit import strToYAML
import os
from editor import edit
# from deleteFiles import deleteMedia

app = Flask(__name__)


def saveFile(yaml, name):
    # file = open(r"static/yaml/" + name + ".yaml", "w")
    file = open(name + ".yaml", "w")
    file.write(yaml)
    file.close()
    return "Success"


def readFile(name):
    # file = open(r"static/yaml/" + name + ".yaml", "r")
    file = open(name + ".yaml", "r")
    trueYAML = file.read()
    file.close()
    return trueYAML


@app.route("/")
def index():
    return render_template("index.html")


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
                vidUpload.save(os.path.join(uploadsDir + "\\" + vids))
                vidCounter += 1

            imgCounter = 1

            for imgs in img:
                imgUpload = request.files["imgAsset" + str(imgCounter)]
                imgUpload.save(os.path.join(uploadsDir + "\\" + imgs))
                imgCounter += 1
            # print(vidUpload, imgUpload)

            return redirect(url_for("render", name=name))
    else:
        dictionary = strToYAML(readFile(yamlName))
        dictionary = dictionary["Project"]["assets"]
        vid = list(dictionary["video"].keys())
        img = list(dictionary["image"].keys())
        return render_template("assetLoading.html", vid=vid, img=img, name=name)


@app.route("/editor/<name>/render")
def render(name):
    edit(yamlName + ".yaml")
    # deleteMedia()
    return render_template("render.html", name=name)


if __name__ == "__main__":
    app.run(debug=True)
