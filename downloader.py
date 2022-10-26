from youtubesearchpython import VideosSearch
import youtube_dl
import pafy
import pytube as pt
from pathlib import Path
from moviepy.editor import *

def search_for_song(name):
    video_search = VideosSearch(name + " official audio", limit=4)
    for v in video_search.result()['result']:
        return v["id"], v["title"], v["thumbnails"][0]['url'], "https://www.youtube.com/watch?v=" + v["id"]


class Song:
    def __init__(self, name):
        vid, title, cover_image_url, u = search_for_song(name)
        self.title = title
        self.url = u
        self.cover_image_url = cover_image_url
        self.video_id = vid

    def to_string(self):
        return """
        title: {0}
        cover_image_url: {1}
        url: {2}
        video_id: {3}
        """.format(self.title, self.cover_image_url, self.url, self.video_id)

    def download(self,output=""):
        print("downloading song", self.to_string())
        Path(output).mkdir(parents=True, exist_ok=True)
        yt = pt.YouTube(self.url)
        video = yt.streams.filter(only_audio=True)
        out_file = video[0].download(output_path=output)
        v = AudioFileClip(out_file)
        print(out_file)

        v.write_audiofile(os.path.join(output,self.title+".mp3"))
        print(os.path.join(output,self.title+".mp3"))
        os.remove(out_file)


if __name__ == '__main__':
    s = Song("paradise ryan carveo")
    s.download(output="./songs/")