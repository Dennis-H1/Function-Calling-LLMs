from operator import itemgetter
from collections import namedtuple
import pandas as pd


class Albums:
    _albums = None

    @classmethod
    def load_albums(cls, path_to_data: str):
        album_columns_to_keep = ["release_name",    # Name of the album
                                 "artist_name",     # Name of the artist/band/group
                                 "release_date",    # Date the album was released
                                 "primary_genres",  # Primary genre classifications
                                 "secondary_genres",  # Secondary genre classifications
                                 "descriptors",     # Album tags
                                 "avg_rating",      # Average rating, on a scale of 0-5
                                 "rating_count",    # The number of ratings
                                 "review_count"     # The number of reviews
                                 ]

        cls._albums = pd.read_csv(path_to_data,
                                  usecols=album_columns_to_keep)

    @classmethod
    def top_rated_albums(cls, n=10):
        """
        Returns the top-rated albums based on average rating.

        Parameters:
            n (int): The number of albums to return. Default is 10.

        Returns:
            list[dict]: A list of dictionaries representing the top-rated albums.
        """

        print(n)

        top_rated = cls._albums.sort_values(
            by='avg_rating', ascending=False).head(n)
        return top_rated.to_dict(orient='records')

    @classmethod
    def most_reviewed_albums(cls, n=10):
        """
        Returns the most reviewed albums.

        Parameters:
            n (int): The number of albums to return. Default is 10.

        Returns:
            list[dict]: A list of dictionaries representing the most reviewed albums.
        """
        most_reviewed = cls._albums.sort_values(
            by='review_count', ascending=False).head(n)
        return most_reviewed.to_dict(orient='records')

    @classmethod
    def albums_by_artist(cls, artist_name):
        """
        Returns all albums by a given artist.

        Parameters:
            artist_name (str): The name of the artist.

        Returns:
            list[dict]: A list of dictionaries representing the albums by the given artist.
        """
        albums = cls._albums[cls._albums['artist_name'] == artist_name]
        return albums.to_dict(orient='records')

    @classmethod
    def artist_by_album(cls, album_name):
        """
        Returns the artist of an album by its name.

        Parameters:
            album_name (str): The name of the album.

        Returns:
            dict: A dictionary with the album name and the artist.
                If the album is not found, the dictionary will be empty.
        """

        artist_dict = {}

        # Search for the album by name and populate the dictionary
        album = cls._albums[cls._albums['release_name'] == album_name]
        if not album.empty:
            artist_dict['Album name'] = album_name
            artist_dict['artist'] = album.iloc[0]['artist_name']

        return artist_dict


class Songs:
    _songs = None

    @classmethod
    def load_songs(cls, path_to_data: str):
        song_columns_to_keep = ['track_name',           # Name of the song
                                # Name of the artist(s) of the song
                                'artist(s)_name',
                                'artist_count',         # Number of artists contributing to the song
                                'released_year',        # Year when the song was released
                                'released_month',       # Month when the song was released
                                'released_day',         # Day of the month when the song was released
                                'in_spotify_playlists',  # Number of Spotify playlists the song is included in
                                'in_spotify_charts',    # Presence and rank of the song on Spotify charts
                                'streams',              # Total number of streams on Spotify
                                'in_apple_playlists',   # Number of Apple Music playlists the song is included in
                                'in_apple_charts',      # Presence and rank of the song on Apple Music charts
                                'in_deezer_playlists',  # Number of Deezer playlists the song is included in
                                'in_deezer_charts',     # Presence and rank of the song on Deezer charts
                                'in_shazam_charts',     # Presence and rank of the song on Shazam charts
                                'bpm',                  # Beats per minute, a measure of song tempo
                                # Key of the song Mode of the song (major or minor)
                                'key',
                                'mode',
                                'danceability_%',       # Percentage indicating how suitable the song is for dancing
                                'valence_%',            # Positivity of the song's musical content
                                'energy_%',             # Perceived energy level of the song
                                'acousticness_%',       # Amount of acoustic sound in the song
                                'instrumentalness_%',   # Amount of instrumental content in the song
                                'liveness_%',           # Presence of live performance elements
                                'speechiness_%'         # Amount of spoken words in the song
                                ]

        cls._songs = pd.read_csv(
            path_to_data, usecols=song_columns_to_keep, encoding_errors="ignore")

    @classmethod
    def top_streamed_songs(cls, n=10):
        """
        Returns the top-streamed songs.

        Parameters:
            n (int): The number of songs to return. Default is 10.

        Returns:
            list[dict]: A list of dictionaries representing the top-streamed songs.
        """
        top_songs = cls._songs.sort_values(
            by='streams', ascending=False).head(n)
        return top_songs.to_dict(orient='records')

    @classmethod
    def songs_in_spotify_playlists(cls, n=10):
        """
        Returns the top songs featured in the most Spotify playlists.

        Parameters:
            n (int): The number of songs to return. Default is 10.

        Returns:
            list[dict]: A list of dictionaries representing the songs featured in the most Spotify playlists.
        """
        top_playlist_songs = cls._songs.sort_values(
            by='in_spotify_playlists', ascending=False).head(n)
        return top_playlist_songs.to_dict(orient='records')

    @classmethod
    def songs_by_artist(cls, artist_name):
        """
        Returns all songs by a given artist.

        Parameters:
            artist_name (str): The name of the artist.

        Returns:
            list[dict]: A list of dictionaries representing the songs by the given artist.
        """
        songs = cls._songs[cls._songs['artist(s)_name'] == artist_name]
        return songs.to_dict(orient='records')

    @classmethod
    def artist_by_song(cls, song_name):
        """
        Returns the artist of the song.

        Parameters:
            song_name (str): The name of the song.

        Returns:
            dict: A dictionary with the song name and the artist.
                If the song is not found, the dictionary will be empty.
        """
        artist_dict = {}

        # Search for the song by name and populate the dictionary
        song = cls._songs[cls._songs['track_name'] == song_name]
        if not song.empty:
            artist_dict['Song'] = song_name
            artist_dict['Artist'] = song.iloc[0]['artist(s)_name']

        return artist_dict


ClassMethod = namedtuple("ClassMethod", "cls name method")

all_functions = [ClassMethod(Songs, key, value.__func__) for key, value in Songs.__dict__.items() - {Songs.load_songs}
                 if isinstance(value, classmethod)] + \
                [ClassMethod(Albums, key, value.__func__) for key, value in Albums.__dict__.items() - {Albums.load_albums}
                 if isinstance(value, classmethod)]
