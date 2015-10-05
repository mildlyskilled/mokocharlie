from django.test import Client
from django.test import TestCase


class HomepageTest(TestCase):

    fixtures = ["common/fixtures/initial_data.json"]

    def setUp(self):
        self.c = Client()
        self.home = self.c.get('/')

    def tearDown(self):
        self.c = None
        self.home = None

    def test_homepage(self):
        """Homepage returns a 200 and has the correct title of Mokocharlie: Organising Community Photos"""
        self.assertEqual(self.home.status_code, 200)
        self.assertTrue(self.home.content.startswith(b'<!DOCTYPE html>'))
        self.assertIn(b'<title>Mokocharlie: Organising Community Photos</title>', self.home.content)
        self.assertTrue(self.home.content.endswith(b'</html>'))

    def test_homepage_has_album_covers(self):
        """Homepage returns has non-empty featured albums in context"""
        self.assertIn('featured_albums', self.home.context)
        self.assertGreater(len(self.home.context['featured_albums']), 0,
                           "The Homepage does not have any featured albums")

    def test_homepage_has_collections(self):
        """Homepage returns has non-empty featured collection of albums in context"""
        self.assertIn('featured_collections', self.home.context)
        self.assertGreater(len(self.home.context['featured_collections']), 0, "The Homepage has no collections")

    def test_photos_page_has_photos(self):
        """Photos page must have a photo set to loop through"""
        self.photos = self.c.get('/photos/')
        self.assertIn('images', self.photos.context)
