import yaml


def assetList(yamlFile):
    with open(yamlFile) as f:
        dict = yaml.load(f, Loader=yaml.FullLoader)

        # ? fullYaml = dict

        videoInfo = []
        videoList = list(dict["Project"]["assets"]["video"].keys())

        def videoListInfo():
            for i in range(len(videoList)):
                videoInfo.append(dict["Project"]["assets"]["video"][videoList[i]])
            return videoInfo

        videoListInfo()

        audioInfo = []
        audioList = list(dict["Project"]["assets"]["audio"].keys())

        def audioListInfo():
            for i in range(len(audioList)):
                audioInfo.append(dict["Project"]["assets"]["audio"][audioList[i]])
            return audioInfo

        audioListInfo()

        imageInfo = []
        imageList = list(dict["Project"]["assets"]["image"].keys())

        def imageListInfo():
            for i in range(len(imageList)):
                imageInfo.append(dict["Project"]["assets"]["image"][imageList[i]])
            return imageInfo

        imageListInfo()

        textInfo = []
        textList = list(dict["Project"]["assets"]["text"].keys())

        def textListInfo():
            for i in range(len(textList)):
                textInfo.append(dict["Project"]["assets"]["text"][textList[i]])
            return textInfo

        textListInfo()

    output = dict["Project"]["export"]

    return (
        [videoList, audioList, imageList, textList],
        [videoInfo, audioInfo, imageInfo, textInfo],
        [output],
    )


# print(assetList("test.yaml"))
