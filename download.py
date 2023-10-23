import time
from pytube import YouTube

FORBIDDEN_FOLDER_CHARS = '\\/:*?"<>|'

def get_data_spotify(url):
    pass



def get_data_yt(url):
    # TODO
    # GET SUBTITLES IF THERE ARE SUBTITLES
    # PUNCTUATE AND PARAGRAPH AND REMOVE REDUNCANCIES IN TRANSCRIPT
    # SUBTITLES HAVE TIMESTAMPS, FIGURE OUT HOW TO MAKE TRANSCRIPTION TIMESTAMPS FROM WHISPER CODE
    # WITH SUMMARY, CAN MAKE LIKE A CONTENTS PAGE (IF THERE ISNT ALREADY)
    # GPT PULL OUT KEY POINTS, AND TIMESTAMPS WHERE

    start = time.time()
    print("getting youtube audio")
    yt = YouTube(url)
    stream = yt.streams.first()
    title = yt.title
    description = yt.description
    print(yt)
    for char in FORBIDDEN_FOLDER_CHARS:
        title = title.replace(char, "")
        description = description.replace(char, "")
    path = yt.streams.get_audio_only().download(f"transcriptions\\{title}")
    with open(f"transcriptions/{title}/url.txt", "w") as f:
        f.write(url)
    download_time = time.time() - start
    print(f"youtube audio downloaded in {download_time // 60} minute(s) and {download_time % 60} second(s)")
    print(yt.captions)
    return title, description, path

def main():
    get_data_yt(input("Enter youtube url: "))


if __name__ == "__main__":
    main()