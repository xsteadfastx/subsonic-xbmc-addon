import sys
import urllib
import urlparse
import xbmcaddon
import xbmcgui
import xbmcplugin
sys.path.append('./resources/lib')
import requests


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


def subsonic_api(method, parameters={'none': 'none'}):
    return subsonic_url + '/rest/' + method + '?u=%s&p=enc:%s&v=1.1.0&c=xbmc-subsonic&f=json&' % (username, password.encode('hex')) + urllib.urlencode(parameters)


def get_artist_list():
    api_url = subsonic_api(
        'getIndexes.view',
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


def get_music_directory_list(id):
    api_url = subsonic_api('getMusicDirectory.view', parameters={'id': id})
    r = requests.get(api_url)
    albums = []
    for album in r.json()['subsonic-response']['directory']['child']:
        item = {}
        item['artist'] = album['artist'].encode('utf-8')
        item['title'] = album['title'].encode('utf-8')
        item['id'] = album['id'].encode('utf-8')
        albums.append(item)

    return albums


def get_cover_art(id):
    return subsonic_api('getCoverArt.view', parameters={'id': id})


def main_page():
    url = build_url({'mode': 'artist_list', 'foldername': 'Artists'})
    li = xbmcgui.ListItem('Artists', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url=url,
        listitem=li,
        isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


def artist_list():
    artists = get_artist_list()
    for artist in artists:
        url = build_url({'mode': 'album_list',
                         'foldername': artist['name'],
                         'artist_id': artist['id']})
        li = xbmcgui.ListItem(artist['name'],
                              iconImage=get_cover_art(artist['id']))
        li.setProperty('fanart_image', get_cover_art(artist['id']))
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=url,
            listitem=li,
            isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


def album_list():
    artist_id = args.get('artist_id', None)
    albums = get_music_directory_list(artist_id[0])
    for album in albums:
        url = build_url({'mode': 'track_list',
                         'foldername': album['title'],
                         'album_id': album['id']})
        li = xbmcgui.ListItem(album['title'], iconImage=get_cover_art(album['id']))
        li.setProperty('fanart_image', get_cover_art(album['id']))
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=url,
            listitem=li,
            isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


def track_list():
    album_id = args.get('album_id', None)
    tracks = get_music_directory_list(album_id[0])
    for track in tracks:
        url = subsonic_api(
            'stream.view',
            parameters={'id': track['id'],
                        'maxBitRate': bitrate,
                        'format': trans_format,
                        'estimateContentLength': 'true'})
        li = xbmcgui.ListItem(track['title'], iconImage=get_cover_art(track['id']))
        li.setProperty('fanart_image', get_cover_art(track['id']))
        li.setProperty('IsPlayable', 'true')
        li.setInfo(type='Music', infoLabels={'Title': track['title']})
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=url,
            listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)


if __name__ == '__main__':
    my_addon = xbmcaddon.Addon('plugin.audio.subsonic')
    subsonic_url = my_addon.getSetting('subsonic_url')
    username = my_addon.getSetting('username')
    password = my_addon.getSetting('password')
    trans_format = my_addon.getSetting('format')
    bitrate = my_addon.getSetting('bitrate')

    base_url = sys.argv[0]
    addon_handle = int(sys.argv[1])
    args = urlparse.parse_qs(sys.argv[2][1:])

    xbmcplugin.setContent(addon_handle, 'movies')

    mode = args.get('mode', None)

    if mode is None:
        main_page()
    elif mode[0] == 'artist_list':
        artist_list()
    elif mode[0] == 'album_list':
        album_list()
    elif mode[0] == 'track_list':
        track_list()
