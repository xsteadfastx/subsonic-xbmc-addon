import unittest
import addon


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.subsonic_url = 'http://demo.subsonic.org'
        self.username = 'guest3'
        self.password = 'guest'

    def test_artist_list(self):
        subsonic = addon.Subsonic(self.subsonic_url,
                                  self.username,
                                  self.password)
        response = subsonic.artist_list()
        for item in response:
            self.assertIn('name', item.keys())
            self.assertIn('id', item.keys())

    def test_music_directory_list(self):
        subsonic = addon.Subsonic(self.subsonic_url,
                                  self.username,
                                  self.password)
        response = subsonic.music_directory_list(1)
        for item in response:
            self.assertIn('artist', item.keys())
            self.assertIn('title', item.keys())
            self.assertIn('id', item.keys())

    def test_cover_art(self):
        subsonic = addon.Subsonic(self.subsonic_url,
                                  self.username,
                                  self.password)
        response = subsonic.cover_art(1)
        expected = '%s/rest/getCoverArt.view?u=%s&p=enc:%s&v=1.1.0&c=xbmc-subsonic&f=json&id=1' % (
            self.subsonic_url, self.username, self.password.encode('hex'))
        self.assertEqual(response, expected)

    def test_genre_list(self):
        subsonic = addon.Subsonic(self.subsonic_url,
                                  self.username,
                                  self.password)
        response = subsonic.genre_list()
        for item in response:
            self.assertIn('songCount', item.keys())
            self.assertIn('albumCount', item.keys())
            self.assertIn('value', item.keys())

    def test_albums_by_genre_list(self):
        subsonic = addon.Subsonic(self.subsonic_url,
                                  self.username,
                                  self.password)
        response = subsonic.albums_by_genre_list('Rock')
        for item in response:
            self.assertIn('artist', item.keys())
            self.assertIn('title', item.keys())
            self.assertIn('id', item.keys())


if __name__ == '__main__':
    unittest.main()
