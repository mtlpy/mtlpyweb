from apiclient.discovery import build
import arrow


def get_all_videos(api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    channels_response = (
        youtube.channels()
        .list(part='contentDetails', forUsername='MontrealPython')
        .execute())
    channel = channels_response['items'][0]
    uploads_list_id = channel['contentDetails']['relatedPlaylists']['uploads']

    playlist_items_response = (
        youtube.playlistItems()
        .list(part='snippet', playlistId=uploads_list_id, maxResults=50)
        .execute())
    playlist_items = [
        item['snippet'] for item in playlist_items_response['items']]
    for item in playlist_items:
        video_id = item['resourceId']['videoId']
        item['video_url'] = 'https://www.youtube.com/watch?v=' + video_id
        item['thumbnail_url'] = item['thumbnails']['high']['url']
        item['published'] = arrow.get(item['publishedAt'])

    return sorted(playlist_items,
                  key=lambda item: item['published'],
                  reverse=True)
