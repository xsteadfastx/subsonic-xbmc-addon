import sys
import urllib
import urlparse
sys.path.append('./resources/lib')
import requests


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


class Subsonic(object):

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def api(self, method, parameters={'none': 'none'}):
        return self.url + '/rest/' + method + '?u=%s&p=enc:%s&v=1.1.0&c=xbmc-subsonic&f=json&' % (
            self.username, self.password.encode('hex')) + urllib.urlencode(parameters)

    def artist_list(self):
        api_url = self.api('getIndexes.view',
                           parameters={'musicFolderId': '0'})
        r = requests.get(api_url)
        artists = []
        for index in r.json()['subsonic-response']['indexes']['index']:
            for artist in index['artist']:
                item = {}
                item['name'] = artist['name'].encode('utf-8')
                item['id'] = artist['id'].encode('utf-8')
                artists.append(item)

        return artists

    def music_directory_list(self, id):
        api_url = self.api('getMusicDirectory.view',
                           parameters={'id': id})
        r = requests.get(api_url)
        albums = []
        for album in r.json()['subsonic-response']['directory']['child']:
            item = {}
            item['artist'] = album['artist'].encode('utf-8')
            item['title'] = album['title'].encode('utf-8')
            item['id'] = album['id'].encode('utf-8')
            albums.append(item)

        return albums

    def genre_list(self):
        api_url = self.api('getGenres.view')
        r = requests.get(api_url)
        genres = []
        for genre in r.json()['subsonic-response']['genres']['genre']:
            item = {}
            item['songCount'] = genre['songCount']
            item['albumCount'] = genre['albumCount']
            item['value'] = genre['value']
            genres.append(item)

        return genres

    def albums_by_genre_list(self, genre):
        api_url = self.api('getAlbumList.view',
                           parameters={'type': 'byGenre',
                                       'genre': genre,
                                       'size': '500'})
        r = requests.get(api_url)
        albums = []
        for album in r.json()['subsonic-response']['albumList']['album']:
            item = {}
            item['artist'] = album['artist'].encode('utf-8')
            item['title'] = album['title'].encode('utf-8')
            item['id'] = album['id'].encode('utf-8')
            albums.append(item)

        return albums

    def cover_art(self, id):
        return self.api('getCoverArt.view', parameters={'id': id})


def main_page():
    menu = [{'mode': 'artist_list', 'foldername': 'Artists'},
            {'mode': 'genre_list', 'foldername': 'Genres'}]
    for entry in menu:
        url = build_url(entry)
        li = xbmcgui.ListItem(entry['foldername'],
                              iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=url,
            listitem=li,
            isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


def genre_list():
    subsonic = Subsonic(subsonic_url, username, password)
    genres = subsonic.genre_list()
    for genre in genres:
        url = build_url({'mode': 'albums_by_genre_list',
                         'foldername': genre['value']})
        li = xbmcgui.ListItem(genre['value'],
                              iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=url,
            listitem=li,
            isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


def albums_by_genre_list():
    genre = args.get('foldername', None)
    subsonic = Subsonic(subsonic_url, username, password)
    albums = subsonic.albums_by_genre_list(genre[0])
    for album in albums:
        url = build_url({'mode': 'track_list',
                         'foldername': album['title'],
                         'album_id': album['id']})
        li = xbmcgui.ListItem(album['artist'] + ' - ' + album['title'])
        li.setIconImage(subsonic.cover_art(album['id']))
        li.setThumbnailImage(subsonic.cover_art(album['id']))
        li.setProperty('fanart_image', subsonic.cover_art(album['id']))
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=url,
            listitem=li,
            isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


def artist_list():
    subsonic = Subsonic(subsonic_url, username, password)
    artists = subsonic.artist_list()
    for artist in artists:
        url = build_url({'mode': 'album_list',
                         'foldername': artist['name'],
                         'artist_id': artist['id']})
        li = xbmcgui.ListItem(artist['name'])
        li.setIconImage(subsonic.cover_art(artist['id']))
        li.setThumbnailImage(subsonic.cover_art(artist['id']))
        li.setProperty('fanart_image', subsonic.cover_art(artist['id']))
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=url,
            listitem=li,
            isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


def album_list():
    artist_id = args.get('artist_id', None)
    subsonic = Subsonic(subsonic_url, username, password)
    albums = subsonic.music_directory_list(artist_id[0])
    for album in albums:
        url = build_url({'mode': 'track_list',
                         'foldername': album['title'],
                         'album_id': album['id']})
        li = xbmcgui.ListItem(album['title'])
        li.setIconImage(subsonic.cover_art(album['id']))
        li.setThumbnailImage(subsonic.cover_art(album['id']))
        li.setProperty('fanart_image', subsonic.cover_art(album['id']))
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=url,
            listitem=li,
            isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


def track_list():
    album_id = args.get('album_id', None)
    subsonic = Subsonic(subsonic_url, username, password)
    tracks = subsonic.music_directory_list(album_id[0])
    for track in tracks:
        url = subsonic.api(
            'stream.view',
            parameters={'id': track['id'],
                        'maxBitRate': bitrate,
                        'format': trans_format})
        li = xbmcgui.ListItem(track['title'])
        li.setIconImage(subsonic.cover_art(track['id']))
        li.setThumbnailImage(subsonic.cover_art(track['id']))
        li.setProperty('fanart_image', subsonic.cover_art(track['id']))
        li.setProperty('IsPlayable', 'true')
        li.setInfo(
            type='Music',
            infoLabels={'Artist': track['artist'],
                        'Title': track['title']})
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=url,
            listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)


if __name__ == '__main__':
    import xbmcaddon
    import xbmcgui
    import xbmcplugin

    my_addon = xbmcaddon.Addon('plugin.audio.subsonic')
    subsonic_url = my_addon.getSetting('subsonic_url')
    username = my_addon.getSetting('username')
    password = my_addon.getSetting('password')
    trans_format = my_addon.getSetting('format')
    bitrate = my_addon.getSetting('bitrate')

    base_url = sys.argv[0]
    addon_handle = int(sys.argv[1])
    args = urlparse.parse_qs(sys.argv[2][1:])

    xbmcplugin.setContent(addon_handle, 'songs')

    mode = args.get('mode', None)

    if mode is None:
        main_page()
    elif mode[0] == 'artist_list':
        artist_list()
    elif mode[0] == 'album_list':
        album_list()
    elif mode[0] == 'track_list':
        track_list()
    elif mode[0] == 'genre_list':
        genre_list()
    elif mode[0] == 'albums_by_genre_list':
        albums_by_genre_list()
