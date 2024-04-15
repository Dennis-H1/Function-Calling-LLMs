import pandas as pd

# multi step
SONGS_SQL = pd.read_excel("./src/data/songs_2.xlsx")
ARTISTS_SQL = pd.read_excel("./src/data/artists_2.xlsx")
ALBUMS_SQL = pd.read_excel("./src/data/albums_2.xlsx")

# single step
ALBUMS = pd.read_csv("./src/data/albums_1.csv")
SONGS = pd.read_csv("./src/data/songs_1.csv")


# single step functions

def albums_by_artist_1(artist_name: str):
    """
    Returns all album titles by a given artist.

    Parameters:
        artist_name (str): The name of the artist.

    Returns:
        list[str]: A list of album titles.
    """
    albums = ALBUMS[ALBUMS['artist_name'] == artist_name]
    return albums.to_dict(orient="records")


def top_rated_albums(n: int = 10):
    """
    Returns the top-rated albums based on average rating.

    Parameters:
        n (int): The number of albums to return. Default is 10.

    Returns:
        list[dict]: A list of dictionaries representing the top-rated albums.
    """
    top_rated = ALBUMS.sort_values(by='avg_rating', ascending=False).head(n)
    return top_rated.to_dict(orient='records')


def artist_by_album(album_name):
    """
    Returns the artist of an album by its name.

    Parameters:
        album_name (str): The name of the album.

    Returns:
        dict: A dictionary with the album name and the artist.
              If the album is not found, the dictionary will be empty.
    """
    artist_dict = {}
    album = ALBUMS[ALBUMS['release_name'] == album_name]
    if not album.empty:
        artist_dict['Album name'] = album_name
        artist_dict['artist'] = album.iloc[0]['artist_name']
    return artist_dict


def albums_by_genres(genres: list[str]):
    """
    Get albums that contain any of the specified genres in 'genres_in'.

    Parameters:
        genres_in (list[str]): A list of genre strings the albums must contain.

    Returns:
        list[dict]: A list of dictionaries representing albums that contain any of the specified genres.
    """
    albums = ALBUMS[ALBUMS['genres'].apply(
        lambda x: any(genre for genre in genres if genre in x))]
    return albums.to_dict(orient='records')


def top_streamed_songs(n: int = 10):
    """
    Returns the top-streamed songs.

    Parameters:
        n (int): The number of songs to return. Default is 10.

    Returns:
        list[dict]: A list of dictionaries representing the top-streamed songs.
    """
    top_songs = SONGS.sort_values(by='streams', ascending=False).head(n)
    return top_songs.to_dict(orient='records')


def songs_by_release_date(release_date: str):
    """
    Get all songs released on a specific date, month, or year.

    Parameters:
        release_date (str): Release date to filter by. Can be in YYYY, YYYY-MM, or YYYY-MM-DD format.

    Returns:
        list[dict]: A list of dictionaries representing all songs released on the specified date.
    """
    # Determine the length of the release_date string to understand the format
    date_length = len(release_date)

    if date_length == 4:  # Year format YYYY
        filter_condition = (SONGS['release_date'].str.startswith(release_date))
    elif date_length == 7:  # Month format YYYY-MM
        filter_condition = (SONGS['release_date'].str[:7] == release_date)
    elif date_length == 10:  # Day format YYYY-MM-DD
        filter_condition = (SONGS['release_date'] == release_date)
    else:
        raise ValueError(
            "Invalid date format. Please use YYYY, YYYY-MM, or YYYY-MM-DD.")

    filtered_songs = SONGS[filter_condition]
    return filtered_songs.to_dict(orient='records')


def songs_by_longest_duration(n: int = 10):
    """
    Returns the top n songs sorted by longest duration.

    Parameters:
        n (int): The number of top songs to return based on duration.

    Returns:
        list[dict]: A list of dictionaries representing the top n songs sorted by duration.
    """
    sorted_songs = SONGS.sort_values(by="duration_in_min", ascending=False)
    top_n_songs = sorted_songs.head(n)
    return top_n_songs.to_dict(orient='records')


def artist_by_song(song_name):
    """
    Returns the artist of the song.

    Parameters:
        song_name (str): The name of the song.

    Returns:

        dict: A dictionary with the song name and the artist.

              If the song is not found, the dictionary will be empty.
    """
    artist_dict = {}
    song = SONGS[SONGS['track_name'] == song_name]
    if not song.empty:
        artist_dict['Song'] = song_name
        artist_dict['Artist'] = song.iloc[0]['artist(s)_name']
    return artist_dict


def songs_by_artist_1(artist_name):
    """
    Returns all songs by a given artist.

    Parameters:
        artist_name (str): The name of the artist.

    Returns:
        list[dict]: A list of dictionaries representing the songs by the given artist.
    """
    # songs = list(set(SONGS[SONGS['artist(s)_name'].filter == artist_name]["track_name"].to_list()))
    songs = SONGS[SONGS['artist(s)_name'].apply(lambda x:
                                                any(artist_name == potential_name.strip()
                                                    for potential_name in str(x).split(',')))]
    return songs.to_dict(orient="records")


def filter_albums_by_date_range(start_date: str, end_date: str):
    """
    Filters albums within a specified date range (inclusive).

    Parameters:
        start_date (str): Start date. Can be in YYYY, YYYY-MM, or YYYY-MM-DD format.
        end_date (str): End date. Can be in YYYY, YYYY-MM, or YYYY-MM-DD format.

    Returns:
        list[dict]: A list of dictionaries, each representing an album released within the specified date range.
    """
    start_year = pd.to_datetime(start_date)

    date_length = len(end_date)
    if date_length == 4:  # Year format YYYY
        end_date = pd.to_datetime(end_date) + pd.offsets.YearEnd()
    elif date_length == 7:  # Month format YYYY-MM
        end_date = pd.to_datetime(end_date) + pd.offsets.MonthEnd()
    elif date_length == 10:  # Day format YYYY-MM-DD
        end_date = pd.to_datetime(end_date)
    else:
        raise ValueError(
            "Invalid date format. Please use YYYY, YYYY-MM, or YYYY-MM-DD.")

    ALBUMS['release_date'] = pd.to_datetime(ALBUMS['release_date'])
    filtered_df = ALBUMS[(ALBUMS['release_date'] >= start_year) &
                         (ALBUMS['release_date'] <= end_date)].copy()

    filtered_df['release_date'] = filtered_df['release_date'].astype(str)

    filtered_dict = filtered_df.to_dict('records')
    return filtered_dict


def albums_by_genres2(genres_in: list[str], genres_out: list[str]):
    """
    Get albums that contain any of the specified genres in 'genres_in' and do not contain any of the genres in 'genres_out'.

    Parameters:
        genres_in (list[str]): A list of genre strings the albums must contain.
        genres_out (list[str]): A list of genre strings the albums must not contain.

    Returns:
        list[dict]: A list of dictionaries representing albums that meet the specified genre inclusion and exclusion criteria.
    """
    included_genre_albums = ALBUMS[ALBUMS['genres'].copy().apply(
        lambda x: any(str(genre).lower() in str(x).lower() for genre in genres_in))]

    filtered_albums = included_genre_albums[~included_genre_albums['genres'].apply(
        lambda x: any(str(genre).lower() in str(x).lower() for genre in genres_out))]

    filtered_albums = filtered_albums.map(lambda x: x.strftime(
        '%Y-%m-%d') if isinstance(x, pd.Timestamp) else x)

    return filtered_albums.to_dict(orient='records')


def albums_by_date_and_genres(release_date: str, genres: list[str]):
    """
    Get albums released on a specific date that contain any of the specified genres.

    Parameters:
        release_date (str): The release date of the albums in YYYY-MM-DD format.
        genres (list[str]): A list of genre strings to filter albums by.

    Returns:
        list[dict]: A list of dictionaries representing albums released on the specified date that match any of the specified genres.
    """

    date_length = len(release_date)

    ALBUMS['release_date'] = ALBUMS['release_date'].astype(str)

    if date_length == 4:  # Year format YYYY
        filter_condition = (
            ALBUMS['release_date'].str.startswith(release_date))
    elif date_length == 7:  # Month format YYYY-MM
        filter_condition = (ALBUMS['release_date'].str[:7] == release_date)
    elif date_length == 10:  # Day format YYYY-MM-DD
        filter_condition = (ALBUMS['release_date'] == release_date)
    else:
        raise ValueError(
            "Invalid date format. Please use YYYY, YYYY-MM, or YYYY-MM-DD.")

    filtered_albums = ALBUMS[filter_condition]

    filtered_albums = filtered_albums[filtered_albums['genres'].apply(
        lambda x: any(str(genre).lower() in str(x).lower() for genre in genres))]

    return filtered_albums.to_dict(orient='records')


def high_rated_albums(rating_threshold: float = 4.0, min_ratings: int = 100):
    """
    Returns albums with a rating above a specified threshold and with at least a minimum number of ratings.

    Parameters:
        rating_threshold (float): The minimum average rating for the albums. Default is 4.0.
        min_ratings (int): The minimum number of ratings an album must have. Default is 100.

    Returns:
        list[dict]: A list of dictionaries representing albums that meet the rating threshold and minimum number of ratings.
    """
    filtered_albums = ALBUMS[(ALBUMS['avg_rating'] >= rating_threshold) & (
        ALBUMS['rating_count'] >= min_ratings)]

    return filtered_albums.to_dict(orient='records')


def top_streamed_songs_by_artist(artist_name: str, n: int = 5):
    """
    Returns the top n streamed songs by a specific artist.

    Parameters:
        artist_name (str): The name of the artist.
        n (int): The number of top-streamed songs to return. Default is 5.

    Returns:
        list[dict]: A list of dictionaries representing the top n streamed songs by the specified artist.
    """
    artist_songs = SONGS[SONGS['artist(s)_name'].str.contains(
        artist_name, case=False, na=False)]
    top_songs = artist_songs.sort_values(by='streams', ascending=False).head(n)

    return top_songs.to_dict(orient='records')


def songs_by_danceability_explicitness(danceability_threshold: float, explicit: bool = True):
    """
    Get songs filtered by their danceability rating and explicitness.

    Parameters:
        danceability_threshold (float): The minimum danceability rating to filter songs by.
        explicit (bool): Flag to filter songs by explicit content. Default is True.

    Returns:
        list[dict]: A list of dictionaries representing songs meeting the danceability threshold and explicitness criteria.
    """
    filtered_songs = SONGS[(SONGS['danceability_%'] > danceability_threshold) & (
        SONGS['explicit'] == explicit)]

    return filtered_songs.to_dict(orient='records')


def albums_by_year_genres_and_descriptors(release_date: str, genres: list[str], descriptors: list[str]):
    """
    Get albums released on a specific date, month, or year, within a genres, and matching specified descriptors.

    Parameters:
        release_date (str): Release date to filter by in YYYY, YYYY-MM, or YYYY-MM-DD format.
        genres (list[str]): Genres to filter by.
        descriptors (list[str]): Descriptors to match.

    Returns:
        list[dict]: A list of dictionaries representing albums by the given criteria.
    """

    date_length = len(release_date)

    if date_length == 4:  # Year format YYYY
        filter_condition = (pd.to_datetime(
            ALBUMS['release_date']).dt.year == int(release_date))
    elif date_length == 7:  # Month format YYYY-MM
        filter_condition = (
            ALBUMS['release_date'].str.startswith(release_date))
    elif date_length == 10:  # Day format YYYY-MM-DD
        filter_condition = (pd.to_datetime(
            ALBUMS['release_date']) == pd.to_datetime(release_date))
    else:
        raise ValueError(
            "Invalid date format. Please use YYYY, YYYY-MM, or YYYY-MM-DD.")

    filtered_albums = ALBUMS[
        filter_condition &
        (ALBUMS['genres'].apply(lambda x: any(str(g).lower() in str(x).lower() for g in genres))) &
        (ALBUMS['descriptors'].apply(lambda x: any(
            str(d).lower() in str(x).lower() for d in descriptors)))
    ]

    return filtered_albums.to_dict(orient='records')


# def albums_by_artist_and_genres_descriptors(artist_name: str, genres: list[str], descriptors: list[str]):
    """
    Get albums by a specific artist that contain any of the specified genres and match any of the given descriptors.

    Parameters:
        artist_name (str): The name of the artist.
        genres (list[str]): A list of genre strings to filter albums by.
        descriptors (list[str]): A list of descriptor strings to filter albums by.

    Returns:
        list[dict]: A list of dictionaries representing albums by the specified artist that match any of the specified genres and descriptors.
    """
    artist_albums = ALBUMS[ALBUMS['artist_name'] == artist_name]

    genre_filtered_albums = artist_albums[artist_albums['genres'].apply(
        lambda x: any(genre in x for genre in genres))]

    final_filtered_albums = genre_filtered_albums[genre_filtered_albums['descriptors'].apply(
        lambda x: any(descriptor in x for descriptor in descriptors))]

    return final_filtered_albums.to_dict(orient='records')


def high_rated_reviewed_albums(rating_threshold: float, min_ratings: int, review_threshold: int):
    """
    Returns albums with a rating above a specified threshold, with at least a minimum number of ratings, and a minimum number of reviews.

    Parameters:
        rating_threshold (float): The minimum average rating for the albums.
        min_ratings (int): The minimum number of ratings an album must have.
        review_threshold (int): The minimum number of reviews an album must have.

    Returns:
        list[dict]: A list of dictionaries representing albums that meet the rating threshold, minimum number of ratings, and minimum number of reviews.
    """
    filtered_albums = ALBUMS[(ALBUMS['avg_rating'] >= rating_threshold) &
                             (ALBUMS['rating_count'] >= min_ratings) &
                             (ALBUMS['review_count'] >= review_threshold)]

    return filtered_albums.to_dict(orient='records')

# def compare_albums_by_years_from_genres(year1: str, year2: str, genres: list[str]):
    """
    Compares albums from two different years filtered by a list of genres.

    Parameters:
        year1 (str): The first year for filtering albums.
        year2 (str): The second year for filtering albums.
        genres (list[str]): A list of genre strings to filter albums by. If empty list, no genre filtering is applied!!!

    Returns:
        list[dict]: A list of dictionaries representing albums released in the specified years and filtered by the specified genres.
    """

    albums_year1 = filter_albums_by_date_range(
        year1 + '-01-01', year1 + '-12-31')
    albums_year2 = filter_albums_by_date_range(
        year2 + '-01-01', year2 + '-12-31')

    df_year1 = pd.DataFrame(albums_year1)
    df_year2 = pd.DataFrame(albums_year2)

    merged_albums = pd.concat([df_year1, df_year2])

    if len(genres) > 0:
        filtered_albums = merged_albums[merged_albums['genres'].apply(
            lambda x: any(genre.lower() in (g.lower() for g in x) for genre in genres))]
        return filtered_albums.to_dict(orient='records')

    return merged_albums.to_dict(orient='records')


def songs_by_danceability_explicitness_speechiness(danceability_threshold: float, speechiness_threshold: float, explicit: bool = True):
    """
    Get songs filtered by their danceability rating, speechiness rating, and explicitness.

    Parameters:
        danceability_threshold (float): The minimum danceability rating to filter songs by.
        speechiness_threshold (float): The minimum speechiness rating to filter songs by.
        explicit (bool): Flag to filter songs by explicit content. Default is True.

    Returns:
        list[dict]: A list of dictionaries representing songs meeting the danceability, speechiness threshold, and explicitness criteria.
    """
    filtered_songs = SONGS[
        (SONGS['danceability_%'] > danceability_threshold) &
        (SONGS['speechiness_%'] > speechiness_threshold) &
        (SONGS['explicit'] == explicit)
    ]

    return filtered_songs.to_dict(orient='records')


def top_streamed_songs_by_artist_date(artist_name: str, release_date: str, n: int = 5):
    """
    Returns the top n streamed songs by a specific artist, released on a specific date, month, or year.

    Parameters:
        artist_name (str): The name of the artist.
        release_date (str): Release date to filter by. Can be in YYYY, YYYY-MM, or YYYY-MM-DD format.
        n (int): The number of top-streamed songs to return. Default is 5.

    Returns:
        list[dict]: A list of dictionaries representing the top n streamed songs by the specified artist, released on the specified date.
    """
    date_length = len(release_date)

    artist_songs = SONGS[SONGS['artist(s)_name'] == artist_name]

    if date_length == 4:  # Year format YYYY
        filter_condition = (
            artist_songs['release_date'].str.startswith(release_date))
    elif date_length == 7:  # Month format YYYY-MM
        filter_condition = (
            artist_songs['release_date'].str[:7] == release_date)
    elif date_length == 10:  # Day format YYYY-MM-DD
        filter_condition = (artist_songs['release_date'] == release_date)
    else:
        raise ValueError(
            "Invalid date format. Please use YYYY, YYYY-MM, or YYYY-MM-DD.")

    filtered_songs = artist_songs[filter_condition].sort_values(
        by='streams', ascending=False)

    top_songs = filtered_songs.head(n)
    return top_songs.to_dict(orient='records')


def unique_albums(genres_threshold: int, artist_count_threshold: int, max_rating_threshold: float):
    """
    Retrieves albums that are notable for their genre diversity and number of collaborating artists, yet have average ratings below a specified threshold.

    Parameters:
        genres_threshold (int): Minimum genres an album must have.
        artist_count_threshold (int): Minimum number of artists on an album.
        max_rating_threshold (float): Maximum average rating for an album.

    Returns: 
        list[dict]: Albums meeting the specified criteria for genre diversity, artist collaboration, and average rating.
    """
    ALBUMS['artist_count'] = ALBUMS['artist_name'].apply(
        lambda x: len(x.split(', ')))

    filtered_albums = ALBUMS[
        (ALBUMS['genres'].apply(lambda x: len(x.split(', '))) > genres_threshold) &
        (ALBUMS['artist_count'] >= artist_count_threshold) &
        (ALBUMS['avg_rating'] < max_rating_threshold)
    ]
    return filtered_albums.to_dict(orient='records')


def albums_by_dates_genres_rating(start_date: str, end_date: str, genre_in: list[str], genre_out: list[str], min_rating: float):
    """
    Retrieves albums released within a specific date range, filtered by included and excluded genres, and having an average rating above a specified threshold.

    Parameters:
        start_date (str): The start date of the date range in YYYY-MM-DD format.
        end_date (str): The end date of the date range in YYYY-MM-DD format.
        genre_in (list[str]): List of genres the albums must include.
        genre_out (list[str]): List of genres the albums must not include.
        min_rating (float): Minimum average rating for the albums.

    Returns:
        list[dict]: A list of dictionaries representing albums that meet the specified criteria.
    """
    start_date_dt = pd.to_datetime(start_date)
    end_date_dt = pd.to_datetime(end_date)

    date_filtered_albums = ALBUMS[(pd.to_datetime(ALBUMS['release_date']) >= start_date_dt) &
                                  (pd.to_datetime(ALBUMS['release_date']) <= end_date_dt)]

    genre_filtered_albums = date_filtered_albums[
        date_filtered_albums['genres'].apply(lambda x: any(str(genre).lower() in str(x).lower() for genre in genre_in)) &
        ~date_filtered_albums['genres'].apply(
            lambda x: any(str(genre).lower() in str(x).lower() for genre in genre_out))
    ]

    final_filtered_albums = genre_filtered_albums[genre_filtered_albums['avg_rating'] >= min_rating]

    return final_filtered_albums.to_dict(orient='records')


def high_rated_reviewed_albums_by_date(rating_threshold: float, min_ratings: int, review_threshold: int, release_date: str):
    """
    Retrieves albums with a rating above a specified threshold, a minimum number of ratings, a minimum number of reviews, and released on a specified date.

    Parameters:
        rating_threshold (float): The minimum average rating for the albums.
        min_ratings (int): The minimum number of ratings an album must have.
        review_threshold (int): The minimum number of reviews an album must have.
        release_date (str): The release date of the albums in YYYY, YYYY-MM, or YYYY-MM-DD format.

    Returns:
        list[dict]: A list of dictionaries representing albums that meet the rating, number of ratings, number of reviews criteria, and are released on the specified date.
    """
    release_date_dt = pd.to_datetime(release_date)

    date_length = len(release_date)

    if date_length == 4:  # Year format YYYY
        filter_condition = (pd.to_datetime(
            ALBUMS['release_date']).dt.year == int(release_date))
    elif date_length == 7:  # Month format YYYY-MM
        filter_condition = (
            ALBUMS['release_date'].str.startswith(release_date))
    elif date_length == 10:  # Day format YYYY-MM-DD
        filter_condition = (pd.to_datetime(
            ALBUMS['release_date']) == release_date_dt)
    else:
        raise ValueError(
            "Invalid date format. Please use YYYY, YYYY-MM, or YYYY-MM-DD.")

    filtered_albums = ALBUMS[
        filter_condition &
        (ALBUMS['avg_rating'] >= rating_threshold) &
        (ALBUMS['rating_count'] >= min_ratings) &
        (ALBUMS['review_count'] >= review_threshold)
    ]

    return filtered_albums.to_dict(orient='records')


def top_streamed_songs_by_artist_date_range(artist_name: str, start_date: str, end_date: str, n: int = 5):
    """
    Returns the top n streamed songs by a specific artist, released within a specified date range.

    Parameters:
        artist_name (str): The name of the artist.
        start_date (str): The start date of the date range in YYYY-MM-DD format.
        end_date (str): The end date of the date range in YYYY-MM-DD format.
        n (int): The number of top-streamed songs to return. Default is 5.

    Returns:
        list[dict]: A list of dictionaries representing the top n streamed songs by the specified artist, released within the specified date range.
    """
    start_date_dt = pd.to_datetime(start_date)
    end_date_dt = pd.to_datetime(end_date)

    artist_songs = SONGS[SONGS['artist(s)_name'] == artist_name].copy()

    artist_songs['release_date'] = pd.to_datetime(artist_songs['release_date'])

    # Filter songs within the date range
    date_range_songs = artist_songs[(artist_songs['release_date'] >= start_date_dt) &
                                    (artist_songs['release_date'] <= end_date_dt)]

    top_songs = date_range_songs.sort_values(
        by='streams', ascending=False).head(n)

    return top_songs.to_dict(orient='records')


def speechiness_songs(speechiness: float, energy: float, explicit: bool, bpm: int, threshold: int = 20):
    """
    Retrieves songs with specific speechiness and energy scores, explicit content, and within a BPM range +/- the threshold.

    Parameters:
        speechiness (float): Target threshold for speechiness.
        energy (float): Target threshold for energy.
        explicit (bool): Flag for filtering by explicit content.
        bpm (int): Beats per minute to filter albums by.
        threshold (int): Range value to determine the acceptable deviation from the speechiness and energy thresholds.

    Returns:
        list[dict]: A list of dictionaries representing songs that meet the speechiness, energy, explicit, and BPM criteria within the specified range.
    """
    filtered_albums = SONGS[
        (SONGS['speechiness_%'] >= speechiness - threshold) & (SONGS['speechiness_%'] <= speechiness + threshold) &
        (SONGS['energy_%'] >= energy - threshold) & (SONGS['energy_%'] <= energy + threshold) &
        (SONGS['bpm'] >= bpm - threshold) & (SONGS['bpm'] <= bpm + threshold) &
        (SONGS['explicit'] == explicit)
    ]

    return filtered_albums.to_dict(orient='records')


def instrumental_songs(instrumentalness: float, valence: float, danceability: float, bpm: int, threshold: int):
    """
    Retrieves songs with specific instrumentalness, valence, danceability, and within a BPM range +/- the threshold.

    Parameters:
        instrumentalness (float): Target threshold for instrumentalness.
        valence (float): Target threshold for valence.
        danceability (float): Target threshold for danceability.
        bpm (int): Beats per minute to filter songs by.
        threshold (int): Range value to determine the acceptable deviation from the instrumentalness, valence, and danceability thresholds.

    Returns:
        list[dict]: A list of dictionaries representing songs that meet the instrumentalness, valence, danceability, and BPM criteria within the specified range.
    """
    # Apply filter for instrumentalness, valence, danceability, and BPM
    filtered_songs = SONGS[
        (SONGS['instrumentalness_%'] >= instrumentalness - threshold) & (SONGS['instrumentalness_%'] <= instrumentalness + threshold) &
        (SONGS['valence_%'] >= valence - threshold) & (SONGS['valence_%'] <= valence + threshold) &
        (SONGS['danceability_%'] >= danceability - threshold) & (SONGS['danceability_%'] <= danceability + threshold) &
        (SONGS['bpm'] >= bpm - threshold) & (SONGS['bpm'] <= bpm + threshold)
    ]

    return filtered_songs.to_dict(orient='records')


def albums_by_release_date_1(release_date: str):
    """
    Get all albums released on a specific date, month, or year.

    Parameters:
        release_date (str): Release date to filter by. Can be in YYYY, YYYY-MM, or YYYY-MM-DD format.

    Returns:
        list[dict]: A list of dictionaries representing all albums released on the specified date.
    """
    # Determine the length of the release_date string to understand the format
    date_length = len(release_date)

    if date_length == 4:  # Year format YYYY
        filter_condition = (
            ALBUMS['release_date'].str.startswith(release_date))
    elif date_length == 7:  # Month format YYYY-MM
        filter_condition = (ALBUMS['release_date'].str[:7] == release_date)
    elif date_length == 10:  # Day format YYYY-MM-DD
        filter_condition = (ALBUMS['release_date'] == release_date)
    else:
        raise ValueError(
            "Invalid date format. Please use YYYY, YYYY-MM, or YYYY-MM-DD.")

    filtered_albums = ALBUMS[filter_condition]
    return filtered_albums.to_dict(orient='records')


def artist_info(artist_name: str):
    artist_info = ARTISTS_SQL[ARTISTS_SQL['Name'] == artist_name]
    return artist_info.to_dict(orient='records')


def album_info(album_name: str):
    album_info = ALBUMS_SQL[ALBUMS_SQL['release_name'] == album_name]
    return album_info.to_dict(orient='records')


def song_info(song_name: str):
    song_info = SONGS_SQL[SONGS_SQL['track_name'] == song_name]
    return song_info.to_dict(orient='records')


def albums_by_artist_2(artist_name: str):
    filtered_albums = ALBUMS_SQL[ALBUMS_SQL['artist_name'].apply(
        lambda x: artist_name in x)]
    return filtered_albums.to_dict(orient='records')


def songs_by_artist_2(artist_name: str):
    filtered_albums = SONGS_SQL[SONGS_SQL['artist(s)_name'].apply(
        lambda x: artist_name in x)]
    return filtered_albums.to_dict(orient='records')


def songs_by_album(album_name: str):
    filtered_songs = SONGS_SQL[SONGS_SQL['album_name'] == album_name]
    return filtered_songs.to_dict(orient='records')


def artists_by_genres(genres: list[str]):
    filtered_artists = ARTISTS_SQL[ARTISTS_SQL['genres'].apply(lambda x:
                                                               any(genre.strip().lower() in map(str.strip, map(str.lower, str(x).split(',')))
                                                                   for genre in genres))]
    return filtered_artists.to_dict(orient='records')


def max_rating_given_albums(albums: list[str]):
    filtered_albums = ALBUMS_SQL[ALBUMS_SQL['release_name'].isin(albums)]
    max_avg_rating = filtered_albums['avg_rating'].max()
    albums_with_max_rating = filtered_albums[filtered_albums['avg_rating']
                                             == max_avg_rating]['release_name'].tolist()
    return {"max_avg_rating": max_avg_rating, "album": albums_with_max_rating}


def sum_streams_given_songs(songs: list[str]):
    if isinstance(songs, str):
        songs = [song.strip() for song in songs.split(',')]

    filtered_songs = SONGS_SQL[SONGS_SQL['track_name'].isin(songs)]
    total_streams = int(filtered_songs['streams'].sum())
    return {"total_streams": total_streams}


def albums_by_release_date_2(release_date: str):
    date_length = len(release_date)

    if date_length == 4:  # Year format YYYY
        filter_condition = (
            ALBUMS_SQL['release_date'].str.startswith(release_date))
    elif date_length == 7:  # Month format YYYY-MM
        filter_condition = (ALBUMS_SQL['release_date'].str[:7] == release_date)
    elif date_length == 10:  # Day format YYYY-MM-DD
        filter_condition = (ALBUMS_SQL['release_date'] == release_date)
    else:
        raise ValueError(
            "Invalid date format. Please use YYYY, YYYY-MM, or YYYY-MM-DD.")

    filtered_songs = ALBUMS_SQL[filter_condition]
    return filtered_songs.to_dict(orient='records')

# - ADDITIONAL -


def filter_by_release_date(start_date: str, end_date: str, target_is_album: bool):
    target = (ALBUMS_SQL if target_is_album == True else SONGS_SQL).copy()

    target["release_date"] = pd.to_datetime(target["release_date"])

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    target_filtered = target[(target['release_date'] >= start_date)
                             & (target['release_date'] <= end_date)]

    return target_filtered.to_dict(orient='records')


def highest_rated_albums(rating_threshold: float = 4.0, min_ratings: int = 100):
    filtered_albums = ALBUMS_SQL[(ALBUMS_SQL['avg_rating'] >= rating_threshold) &
                                 (ALBUMS_SQL['rating_count'] >= min_ratings)]
    return filtered_albums.to_dict(orient='records')


class MusicFunctions:
    functions = set((
        # single-step functions
        albums_by_artist_1,
        albums_by_date_and_genres,
        albums_by_dates_genres_rating,
        albums_by_genres,
        albums_by_genres2,
        albums_by_year_genres_and_descriptors,
        artist_by_album,
        artist_by_song,
        filter_albums_by_date_range,
        high_rated_albums,
        high_rated_reviewed_albums,
        high_rated_reviewed_albums_by_date,
        instrumental_songs,
        songs_by_artist_1,
        songs_by_danceability_explicitness,
        songs_by_danceability_explicitness_speechiness,
        songs_by_longest_duration,
        songs_by_release_date,
        speechiness_songs,
        top_rated_albums,
        top_streamed_songs,
        top_streamed_songs_by_artist,
        top_streamed_songs_by_artist_date,
        top_streamed_songs_by_artist_date_range,
        unique_albums,
        albums_by_release_date_1,

        # multi-step functions
        album_info,
        albums_by_artist_2,
        albums_by_release_date_2,
        artist_info,
        artists_by_genres,
        filter_by_release_date,
        highest_rated_albums,
        max_rating_given_albums,
        song_info,
        songs_by_album,
        songs_by_artist_2,
        sum_streams_given_songs
    ))
