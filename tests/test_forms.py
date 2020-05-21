import pytest

from findartist.forms import ArtistForm


class TestForms:
    """ Tests for forms.py """

    @pytest.mark.skip
    def test_artistform_validators_valid(self, app):
        """ https://stackoverflow.com/questions/61683650/flask-form-test-fails-for-some-reason """
        form = ArtistForm(artist="Earl Sweatshirt")
        assert form.validate_on_submit()

    def test_artistform_validators_invalid(self, app):
        form = ArtistForm(artist='')
        assert not form.validate()
