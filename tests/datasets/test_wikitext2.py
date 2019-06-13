from unittest import TestCase
from unittest.mock import patch
import tempfile


from lineflow.datasets import WikiText2
from lineflow.datasets.wikitext2 import TRAIN_URL, VALID_URL, TEST_URL


class WikiTextTestCase(TestCase):

    def setUp(self):
        fp = tempfile.NamedTemporaryFile()
        self.fp = fp

        cached_download_patcher = patch('lineflow.datasets.wikitext2.cached_download')
        cached_download_mock = cached_download_patcher.start()
        cached_download_mock.side_effect = lambda url: fp.name

        self.cached_download_patcher = cached_download_patcher
        self.cached_download_mock = cached_download_mock

    def tearDown(self):
        self.fp.close()
        self.cached_download_patcher.stop()

    def test_returns_train_set(self):
        WikiText2(split='train')
        self.cached_download_mock.assert_called_once_with(TRAIN_URL)

    def test_returns_valid_set(self):
        WikiText2(split='valid')
        self.cached_download_mock.assert_called_once_with(VALID_URL)

    def test_returns_test_set(self):
        WikiText2(split='test')
        self.cached_download_mock.assert_called_once_with(TEST_URL)

    def test_raises_value_error_with_invalid_split(self):
        with self.assertRaises(ValueError):
            WikiText2(split='invalid_split')
