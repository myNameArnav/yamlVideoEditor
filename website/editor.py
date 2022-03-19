from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, TextClip, CompositeVideoClip
# from moviepy.editor import *
from parser import assetList
# from imgSize import imageResize
from moviepy.config import change_settings
import os
change_settings(
    {"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe"}
)

# os.chdir("static\\yaml")

def edit(yamlFile):
    lists = assetList(yamlFile)
    os.chdir("media")
    # * --------- Video ------------
    #! videoClip = (VideoFileClip("vid.mp4")
    #!                 .subclip(5000,5010))

    vidList = lists[0][0]
    vidInfo = lists[1][0]
    # print(vidList, vidInfo)

    clips = []
    for i in range(len(vidList)):
        clips.append(
            VideoFileClip(vidList[i]).subclip(
                vidInfo[0]["subclip"][0], vidInfo[0]["subclip"][1]
            )
        )
    concatClip = concatenate_videoclips(clips)


    # * --------- Image ------------
    #! logo = (
    #!     ImageClip("logo_small.png")
    #!     .set_duration(videoClip.duration)
    #!     .set_opacity(0.6)
    #!     .set_position(("right", "bottom"))
    #!     .margin(right = 10, bottom = 10)
    #!     )

    imgList = lists[0][2]
    imgInfo = lists[1][2]
    givenParams = ["timings", "opacity"]



    givenParamsImg = {
        "timings": [],
        "position": ["center", "center"],
        "opacity": 1,
        "margin" : [0, 0, 0, 0],
        "size": 10
        }
    # print(imgInfo[1].keys())

    # imgName = imageResize("logo.png", imgInfo[0]["size"])

    def imgParams():
        temp = 0
        for a in range(len(imgList)):
            for i, j in givenParamsImg.items():
                temp = 0
                for k in imgInfo[a].keys():
                    if str(i) == str(k):
                        temp = 1
                if temp == 0:
                    imgInfo[a][i] = j
                    # pass


    imgParams()

    # print(imgInfo[0]["timings"][0])
    img = []
    for i in range(len(imgList)):
        # print((str(imgInfo[i]["position"][0]), str(imgInfo[i]["position"][1])))

        logo = (
            ImageClip(imgList[i])
            .set_start(imgInfo[i]["timings"][0])
            .set_end(imgInfo[i]["timings"][1])
            .set_opacity(float(imgInfo[i]["opacity"]))
            .margin(top = imgInfo[i]["margin"][0], right = imgInfo[i]["margin"][1], bottom = imgInfo[i]["margin"][2], left = imgInfo[i]["margin"][3], opacity = 0)
        )
        img.append(logo)

    # * --------- Text ------------
    #! txt = (
    #!     TextClip(text, color='grey', font='Arial', fontsize=sizeOfFont)
    #!     .set_duration(videoClip.duration)
    #!     .set_opacity(0.5)
    #!     .set_position((("center", "center")))
    #!     )

    txtList = lists[0][3]
    txtInfo = lists[1][3]

    givenParamsTxt = {
        "timings": [0, 5],
        "position": ["center", "center"],
        "opacity": 1,
        "size": 10,
        "font": "Arial",
        "color": "black",
        "margin": [0, 0, 0, 0]
    }
    # print(imgInfo[1].keys())
    def txtParams():
        temp = 0
        for a in range(len(txtList)):
            for i, j in givenParamsTxt.items():
                temp = 0
                for k in txtInfo[a].keys():
                    if str(i) == str(k):
                        temp = 1
                if temp == 0:
                    txtInfo[a][i] = j


    txtParams()

    txt = []
    for i in range(len(txtList)):
        text = (
            TextClip(
                txtList[i],
                font=txtInfo[i]["font"],
                fontsize=txtInfo[i]["size"],
                color=txtInfo[i]["color"],
            )
            .set_start(txtInfo[i]["timings"][0])
            .set_end(txtInfo[i]["timings"][1])
            .set_opacity(float(txtInfo[i]["opacity"]))
            .set_position((str(txtInfo[i]["position"][0]), str(txtInfo[i]["position"][1])))
            .margin(top = txtInfo[i]["margin"][0], right = txtInfo[i]["margin"][1], bottom = txtInfo[i]["margin"][2], left = txtInfo[i]["margin"][3], opacity = 0)
        )
        txt.append(text)


    # print(txtInfo[0], txtInfo[1])

    # * --------- Audio ------------

    # audList = lists[0][1]
    # audInfo = lists[1][1]
    # # print(audList, audInfo)

    # aud = []
    # for i in range(len(audList)):
    #     audio = (
    #         AudioFileClip(
    #             audList[i]
    #         )
    #         # .set_start(audInfo[i]["timings"][0])
    #         # .set_end(audInfo[i]["timings"][1])
    #     )
    #     aud.append(audio)


    cvc = [concatClip]
    cvc = cvc + img + txt
    final_clip = CompositeVideoClip(cvc)

    outputList = lists[2]
    outputInfo = lists[2][0]
    # print(outputName)

    if outputInfo["isGIF"] == True:
        print(final_clip.write_gif(outputInfo["outputName"]))
    elif outputInfo["isGIF"] == False:
        print(final_clip.write_videofile(outputInfo["outputName"], fps=30))
    else:
        print("Try Again")