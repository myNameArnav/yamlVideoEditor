from flask import Flask, redirect, render_template, request, url_for
from submit import strToYAML

app = Flask(__name__)

def saveFile(yaml, name):
    file = open(r"static/yaml/" + name + ".yaml", "w")
    file.write(yaml)
    file.close()
    return "Success"

def readFile(name):
    file = open(r"static/yaml/" + name + ".yaml", "r")
    trueYAML = file.read()
    file.close()
    return trueYAML

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/editor", methods=["GET", "POST"])
def editor():
    if request.method == "POST":
        yaml = request.form["yamlConf"]
        global yamlName
        yamlName = str((yaml.split("\n"))[1])[9:-2]
        saveFile(yaml = yaml, name = yamlName)
        return redirect(url_for("assetLoading", name = yamlName))
    else:
        return render_template("editor.html")

@app.route("/editor/<name>/assetUploading", methods = ["GET", "POST"])
def assetLoading(name):
    if request.method == "POST":
        pass
    else:
        dictionary = strToYAML(readFile(yamlName))
        dictionary = dictionary["Project"]["assets"]
        vid = list(dictionary["video"].keys())
        img = list(dictionary["image"].keys())
        return render_template("assetLoading.html", vid = vid, img = img, name = name)

if __name__ == "__main__":
    app.run(debug=True)