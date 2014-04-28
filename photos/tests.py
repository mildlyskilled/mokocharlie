from django.test import Client
from django.test import TestCase
from moko.views import HomeTemplateView


class HomepageTest(TestCase):
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
        self.assertGreater(len(self.home.context['featured_albums']), 0)

    def test_homepage_has_collections(self):
        """Homepage returns has non-empty featured collection of albums in context"""
        self.assertIn('featured_collections', self.home.context)
        self.assertGreater(len(self.home.context['featured_collections']), 0)

    def test_homepage_has_classifieds(self):
        """Homepage returns has non-empty classifieds in context"""
        self.assertIn('classifieds', self.home.context)
        self.assertGreater(len(self.home.context['classifieds']), 0)
