import pytest
from spotipy import SpotifyException
import findartist.spotify


class TestSpotifyMethods:
    """ Tests for methods in spotify.py"""

    @pytest.mark.long
    def test_mock_handle_rate_limiting_429(self, app, worker):
        """ Tests that a SpotifyException with a Retry-After header gets added to queue and is finished properly """
        mock_exception = SpotifyException(http_status=429, code=-1, msg="Mock exception", headers={'Retry-After': 1})
        job = findartist.spotify.handle_rate_limiting(mock_exception)

        assert job in app.task_queue.jobs
        worker.work(burst=True)
        assert job not in app.task_queue.jobs
        assert job.is_finished

    def test_mock_handle_rate_limiting_other(self, app, worker):
        """ Tests that SpotifyExceptions without a Retry-After header return none"""
        mock_exception = SpotifyException(http_status=500, code=-1, msg="Mock exception")
        job = findartist.spotify.handle_rate_limiting(mock_exception)
        assert job is None

    def test_mock_handle_rate_limiting_bad_response(self, app, worker):
        """ Tests the method with a string input instead of integer"""
        mock_exception = SpotifyException(http_status=429, code=-1, msg="Mock exception", headers={'Retry-After': '5'})
        job = findartist.spotify.handle_rate_limiting(mock_exception)
        assert job is None

