import addon
import json
import mock
import unittest


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.subsonic_url = 'http://foo.subsonic.bar'
        self.username = 'foo'
        self.password = 'bar'
        self.subsonic = addon.Subsonic(self.subsonic_url,
                                       self.username,
                                       self.password)

    @mock.patch('addon.requests')
    def test_artist_list(self, mock_requests):
        mock_requests.get.return_value = mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = json.load(
            open('test/test_artist_list.json'))
        response = self.subsonic.artist_list()
        for item in response:
            self.assertIn('name', item.keys())
            self.assertIn('id', item.keys())

    @mock.patch('addon.requests')
    def test_music_directory_list(self, mock_requests):
        mock_requests.get.return_value = mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = json.load(
            open('test/test_music_directory_list.json'))
        response = self.subsonic.music_directory_list(1)
        for item in response:
            self.assertIn('artist', item.keys())
            self.assertIn('title', item.keys())
            self.assertIn('id', item.keys())

    @mock.patch('addon.requests')
    def test_cover_art(self, mock_requests):
        mock_requests.get.return_value = mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = json.load(
            open('test/test_music_directory_list.json'))
        response = self.subsonic.cover_art(1)
        expected = '%s/rest/getCoverArt.view?u=%s&p=enc:%s&v=1.1.0&c=xbmc-subsonic&f=json&id=1' % (
            self.subsonic_url, self.username, self.password.encode('hex'))
        self.assertEqual(response, expected)

    @mock.patch('addon.requests')
    def test_random_songs_from_to_year(self, mock_requests):
        mock_requests.get.return_value = mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = json.load(
            open('test/test_random_songs_from_to_year.json'))
        response = self.subsonic.random_songs_from_to_year('2006', '2007')
        for item in response:
            self.assertIn('id', item.keys())
            self.assertIn('title', item.keys())
            self.assertIn('year', item.keys())
            self.assertIn('genre', item.keys())
            self.assertIn('albumId', item.keys())
            self.assertIn('artistId', item.keys())
            self.assertIn(int(item['year']), [2006, 2007])


if __name__ == '__main__':
    unittest.main()
