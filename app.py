from flask import Flask, render_template, redirect, request
# from flask_ngrok import run_with_ngrok
from pytube import YouTube
import subprocess
import os


app = Flask(__name__)

# Tried ngrok to make it temporarily accessible over the internet
# run_with_ngrok(app)


@app.route('/')
def start():
    return render_template("index.html") # through this app.py render the html


@app.route('/download', methods=['POST'])
def download():
    try:
        YouTubeUrl = request.form['youTubeUrl']
        yt = YouTube(YouTubeUrl)
        video = yt.streams.get_highest_resolution()

        # find the user's download directory, if doesn't exist, then create it for them
        userHomeDir = os.path.expanduser("~")
        userDownloadDir = os.path.join(userHomeDir, "Downloads")
        os.makedirs(userDownloadDir, exist_ok=True)
        targetDownloadPath = userDownloadDir

        videoPath = video.download(targetDownloadPath)
        print(videoPath)
        audioPath = videoPath.replace(".mp4", ".mp3")
        print(audioPath)

        # subprocess.run(['ffmpeg', '-i', videoPath, '-q:a', '0', '-map', 'a', audioPath])

        print("Success")
        return redirect('/')
    
    except Exception as e:
        return f"Error Occurred: {e}"


# flask run will successfully run the server without the code below, but python3 app.py can only run the server successfully with the code below
if __name__ == '__main__':
    app.run()