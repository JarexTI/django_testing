from notes.models import Note
from notes.tests.fixtures import SLUG, BaseFixture


class ContentFixture(BaseFixture):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.note = Note.objects.create(
            author=cls.user,
            title=cls.TITLE,
            text=cls.TEXT,
            slug=SLUG,
        )
