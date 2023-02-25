from pytube import YouTube

# enter the video URL
url = input("Enter the video URL: ")

# create a YouTube object
video = YouTube(url)

# print the available video streams
print("Available video streams:")
for stream in video.streams:
    print(stream)

# select the desired video stream and download the video
itag = input("Enter the itag of the video stream to download: ")
stream = video.streams.get_by_itag(itag)

# prompt user for the download directory path
dir_path = input("Enter the directory path where you want to save the video: ")

# download the video to the specified directory
stream.download(output_path=dir_path)

print("Video downloaded successfully!")
