from youtubesearchpython import VideosSearch
import pytube as pt
from pathlib import Path
from moviepy.editor import *
import csv
def search_for_song(name):
    video_search = VideosSearch(name + " official audio", limit=4)
    for v in video_search.result()['result']:
        return v["id"], v["title"], v["thumbnails"][0]['url'], "https://www.youtube.com/watch?v=" + v["id"]


class Song:
    def __init__(self, name,url=None):
        if url is not None:
            self.url = url
            yt = pt.YouTube(self.url)
            self.title = yt.title
            self.video_id = yt.video_id
            self.cover_image_url = yt.thumbnail_url
        else:
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


def listSongsInPlaylist(playlistURL):
    play_list = pt.Playlist(playlistURL)
    song_list = []
    for p in play_list:
        print(p)
        song_list.append(Song(name="",url=p))
    return play_list.initial_data['header']['playlistHeaderRenderer']['title']['simpleText'],song_list


if __name__ == '__main__':


    # opening the CSV file
    with open('swim.csv', mode='r') as file:

        # reading the CSV file
        csvFile = csv.reader(file)
        headers = {}
        songList = []
        # displaying the contents of the CSV file
        for lines in csvFile:
            if len(headers) == 0:
                for (i,d) in enumerate(lines):
                    headers[d] = i
            else:
                id,title,thumbnails,url = search_for_song("{0} - {1}".format(headers["Track name"], headers["Artist name"]))
                print("Adding song - {0} - {1}".format(title,url))
                songList.append(Song(name="", url=url))

        for s in songList:
            s.download("./playlists/"+"swim")

    # playlist_url = input("youtube playlist url:")
    # playlistName,songs = listSongsInPlaylist(playlist_url)
    # for s in songs:
    #     s.download("./playlists/"+playlistName)
