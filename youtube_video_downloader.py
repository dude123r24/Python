# pip3 install pytube
# pip3 install --upgrade certifi


import pytube
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

link = input("Enter a YouTube video's URL: ")
try:
    yt = pytube.YouTube(link)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream.download()
    print(f"Downloaded {link}")
except pytube.exceptions.RegexMatchError:
    print("Invalid YouTube video URL")
except pytube.exceptions.VideoUnavailable:
    print("YouTube video is unavailable")
except pytube.exceptions.PytubeError as e:
    print(f"An error occurred: {str(e)}")


# https://youtu.be/dQw4w9WgXcQ
