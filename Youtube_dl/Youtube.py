import subprocess
import pytube
import os

def Streams(url):
    yt=pytube.YouTube(url)
    video=yt.streams.filter(subtype='mp4')
    dico={}
    for i in range(len(video)):
        dico[i]=video[i]
    audio=yt.streams.filter(only_audio=True)
    dico["mp3"]=audio[0]
    dico["img"]=yt.thumbnail_url
    return dico


# Faire une fonction qui prends en entrée l'index de streams et qui va le dl et qui return sur linked


def download(videos,index,links):
    print(os.getcwd())
    if index != "mp3":
        index=int(index)
        mp4=videos[index].default_filename
        if mp4.replace(".mp4",f" en {videos[index].resolution}.mp4") not in os.listdir(os.getcwd()+"\\static"):
            videos[index].download()
            os.rename(mp4,"video.mp4")
            mp3_file=videos["mp3"].default_filename
            videos["mp3"].download()
            os.rename(mp3_file,"temp.mp4")
            mp3="temp.mp4"
            temp="video.mp4"
            cmd=f"ffmpeg -analyzeduration 999999999 -probesize 999999999 -i {temp} -i {mp3} -c:v copy -map 0:v:0 -map 1:a:0 output.mp4" # "ffmpeg -i {temp} -i {mp3} output.mp4"
            print(cmd)
            os.system(cmd)
            os.remove(mp3)
            os.remove(temp)
            # mp4=mp4.replace(".mp4",f" {videos[index].resolution},{videos[index].fps}.mp4")
            os.rename("output.mp4",mp4)
            os.replace(os.getcwd()+"\\"+mp4,os.getcwd()+"\\static\\"+mp4)
        links[videos[index].title+".mp4"+f"(en {videos[index].resolution},{videos[index].fps})"]=mp4.replace(" ","%20")
    else:
        mp3_file=videos["mp3"].default_filename
        if mp3_file.replace("mp4","mp3") not in os.listdir(os.getcwd()+"\\static"):
            videos["mp3"].download()
            os.rename(mp3_file,mp3_file.replace("mp4","mp3"))
            os.replace(os.getcwd()+"\\"+mp3_file.replace("mp4","mp3"),os.getcwd()+"\\static\\"+mp3_file.replace("mp4","mp3"))
        links[videos[index].title+".mp3"]=mp3_file.replace("mp4","mp3").replace(" ","%20")


# <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">