# -*- coding: utf-8 -*-
from python2nix.utils import to_nixname
from python2nix.utils import nix_metadata

import python2nix.utils
import unittest 
 
class UtilsTest(unittest.TestCase):

    def mock_get_metadata(self, metadata):
        python2nix.utils.get_metadata = lambda x: metadata

    def test_to_nixname_camelcase(self):
        """Test that CamelCase names are converted to lowercase"""
        self.assertEqual(to_nixname("CamelCase"), "camelcase")

    def test_to_nixname_hypen_to_underscore(self):
        """Test that hyphens in names are replace with underscores"""
        self.assertEqual(to_nixname("hyphen-name"), "hyphen_name")

    def test_to_nixname_dots_to_underscore(self):
        """Test that CamelCase names are converted to lowercase"""
        self.assertEqual(to_nixname("dot.name"), "dot_name")

    def test_nix_metadata_homepage(self):
        self.mock_get_metadata({"Home-page": "http://nixos.org"})
        self.assertTrue("homepage" in nix_metadata(None))

    def test_nix_metadata_description(self):
        self.mock_get_metadata({"Summary": "Package description"})
        self.assertTrue("description" in nix_metadata(None))

    def test_nix_metadata_license(self):
        self.mock_get_metadata({"License": "GPL"})
        self.assertTrue("license" in nix_metadata(None))

if __name__ == '__main__':
    unittest.main()
 
