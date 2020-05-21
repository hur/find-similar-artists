from findartist.forms import ArtistForm


class TestForms:
    """ Tests for forms.py """

    def test_artistform_validators(self, app):
        form = ArtistForm(artist='')
        assert not form.validate()
