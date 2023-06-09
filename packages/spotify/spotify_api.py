import spotipy

from packages.spotify.spotify_web import SpotifyPlaylist
from packages.utilities.logger import Logger
from setup import Setup

logger = Logger("spotipy logger")
config = Setup()


class SpotifyAPI:
    # environment variables
    CLIENT_ID = config.CLIENT_ID
    CLIENT_SECRET = config.CLIENT_SECRET
    REDIRECT_URI = config.REDIRECT_URI

    # authorised actions
    SCOPE = """user-read-private user-library-read user-follow-read user-read-recently-played user-top-read 
    playlist-read-private user-library-modify playlist-modify-private"""

    def __init__(self):
        self.token = spotipy.SpotifyOAuth(
            client_id=SpotifyAPI.CLIENT_ID,
            client_secret=SpotifyAPI.CLIENT_SECRET,
            scope=SpotifyAPI.SCOPE,
            redirect_uri=SpotifyAPI.REDIRECT_URI
        )

        self.sp = spotipy.Spotify(auth_manager=self.token)

    def get_top_songs(self, limit: int = 10) -> list[str]:
        """
        Returns dict of top played songs from spotipy. Converts dict to list of song names

        :param: limit
        :return: top_songs_list
        """

        top_songs_list = []

        # get top songs
        top_songs = self.sp.current_user_top_tracks(limit=limit, time_range="short_term")

        # add contents to list
        for track in top_songs["items"]:
            track_name = track["name"]
            artist_names = ", ".join([artist["name"] for artist in track["artists"]])
            top_songs_list.append(f"{track_name} by {artist_names}")

        # output to log
        logger.log("info", f"Top songs list created. Limit: '{limit}', number of songs: '{len(top_songs_list)}'")
        logger.log("debug", f"Top songs list: '{top_songs_list}'")

        # return list
        return top_songs_list

    def get_recently_played(self, limit: int = 10) -> list[str]:
        """
        Returns dict of recently played songs from spotipy. Converts dict to list of song names

        :param: limit
        :return: recently_played_list
        """

        recently_played_list = []

        # get recently played songs
        recently_played = self.sp.current_user_recently_played(limit=limit)

        # add contents to list
        for track in recently_played["items"]:
            track_name = track["track"]["name"]
            artist_names = ", ".join([artist["name"] for artist in track["track"]["artists"]])
            recently_played_list.append(f"{track_name} by {artist_names}")

        # output to log
        logger.log("info",
                   f"Recent songs list created. Limit: '{limit}', number of songs: '{len(recently_played_list)}'")
        logger.log("debug", f"Recent songs list: '{recently_played_list}'")

        # return list
        return recently_played_list

    def get_playlist_items(self) -> list[str]:
        """Returns dict of songs from selected playlist. Converts dict to list of song names"""

        # select playlist
        playlist_url = SpotifyPlaylist().get_playlist()
        playlist_item_list = []

        # get playlist items
        playlist_items = self.sp.playlist_items(playlist_url)

        # add contents to list
        for track in playlist_items["items"]:
            track_name = track["track"]["name"]
            artist_names = ", ".join([artist["name"] for artist in track["track"]["artists"]])
            playlist_item_list.append(f"{track_name} by {artist_names}")

        # output to log
        logger.log("info", f"Fetched '{len(playlist_item_list)}' songs from '{playlist_url}'")
        logger.log("debug", f"Track list: '{playlist_item_list}'")

        # return list
        return playlist_item_list

    def get_tracks(self, track_ids: list[str]) -> dict:
        """Returns dict containing track name, image url and preview url for each track"""

        # empty dict to store data
        track_data = dict()

        # get track data
        tracks = self.sp.tracks(track_ids)

        # create dicts for each track returned
        for track in tracks["tracks"]:
            track_id = track["id"]

            track_data[track_id] = dict()
            track_data[track_id]["name"] = track["name"]
            track_data[track_id]["track_id"] = track["id"]
            track_data[track_id]["artist"] = track["artists"][0]["name"]
            track_data[track_id]["image_url"] = track["album"]["images"][0]["url"]
            track_data[track_id]["preview_url"] = track["preview_url"]

        # output to log
        logger.log("debug", "Got track data")

        # return data
        return track_data

    def search(self, queries: list) -> list[str]:
        """Search spotify with song name and artists"""

        track_ids = []

        for song in queries:
            track_data = self.sp.search(song, limit=10)
            track_id = track_data["tracks"]["items"][0]["id"]
            track_ids.append(track_id)

        return track_ids

    def add_track(self, track_id: str) -> None:
        """add track to liked songs"""

        self.sp.current_user_saved_tracks_add(tracks=[track_id])

        return logger.log("debug", "Added track to liked songs")
