from django.test import TestCase

from book.models import Publisher, Author, Book
from model_mommy import mommy


class PublisherTestMommy(TestCase):

    def test_publisher_creation_mommy(self):
        publisher = mommy.make(Publisher)
        self.assertTrue(isinstance(publisher, Publisher))
        self.assertEqual(str(publisher), publisher.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Publisher._meta.verbose_name_plural), "publishers")


class AuthorTestMommy(TestCase):

    def test_author_creation_mommy(self):
        author = mommy.make(Author)
        self.assertTrue(isinstance(author, Author))
        self.assertEqual(str(author), author.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Author._meta.verbose_name_plural), "authors")


class BookTestMommy(TestCase):

    def test_book_creation_mommy(self):
        book = mommy.make(Book, make_m2m=True)
        self.assertTrue(isinstance(book, Book))
        self.assertEqual(str(book), book.title)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Book._meta.verbose_name_plural), "books")