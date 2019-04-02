from model_mommy import mommy
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from ..models import Publisher, Author, Book
from ..views import PublisherUpdate, home, AuthorUpdate, BookCreate, BookUpdate
from model_mommy.recipe import Recipe, foreign_key


class HomeTests(TestCase):
    def setUp(self):
        self.board = Publisher.objects.create(name='Django', address='Django board.')
        url = reverse('books:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class PublisherListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_publisher = 15

        for publisher_id in range(number_of_publisher):
            Publisher.objects.create(
                name='ali {publisher_id}', address='ryk {publisher_id}', city='bwp {publisher_id}',
                state_province='punjab {publisher_id}',
                country='pak {publisher_id}', website='https://www.google.com/ {publisher_id}'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/publishers/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('books:publisher_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('books:publisher_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/publisher_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('books:publisher_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['publisher_list']) == 10)

    def test_lists_all_publishers(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('books:publisher_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['publisher_list']) == 5)


class PublisherCreateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='123')
        self.create_url = reverse('books:publisher-add')
        self.publisher1 = Publisher.objects.create(name="ali", address="ryk", city="bwp", state_province="punjab",
                                                   country="pak", website="https://www.google.com/")

    def test_create_success_url(self):
        response = self.client.post(self.create_url,
                                    {'name': 'ali',
                                     'address': 'new blog',
                                     'city': 'bwp',
                                     'state_province': 'punjab',
                                     'country': 'pak',
                                     'website': 'https://www.google.com/'
                                     }
                                    )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/publishers/')

    def test_publisher_POST_data(self):
        response = self.client.post(self.create_url)
        self.assertEquals(response.status_code, 200)


class PublisherUpdateTestCase(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name='Django', address='Django board.')
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.client.login(username='john', password='123')
        self.update_url = reverse('books:publisher-update', args={'pk': self.user.id})

        self.url = reverse('books:publisher-update', kwargs={
            'pk': self.publisher.pk,

        })
        self.url_delete = reverse('books:publisher-delete', kwargs={
            'pk': self.publisher.pk,

        })


class PublisherUpdateViewTests(PublisherUpdateTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_update_publisher(self):
        book = Publisher.objects.create(name='The Catcher in the Rye')

        response = self.client.post(
            reverse('books:publisher-update', kwargs={'pk': book.id}),
            {'name': 'The Catcher in the Rye', 'address': 'new blog',
             'city': 'bwp',
             'state_province': 'punjab',
             'country': 'pak',
             'website': 'https://www.google.com/'})

        self.assertEqual(response.status_code, 302)

        book.refresh_from_db()
        self.assertEqual(book.address, 'new blog')

    def test_update_inputs(self):
        self.assertContains(self.response, '<name', 0)
        self.assertContains(self.response, '<address', 0)

    def test_view_class(self):
        view = resolve('/publisherupdate/1/')
        self.assertEquals(view.func.view_class, PublisherUpdate)


class TestDeletePublisher(PublisherUpdateTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)

    def test_my_get_request(self):
        response = self.client.get(self.url_delete)
        self.assertEqual(response.status_code, 200)

    def test_my_post_request(self):
        response = self.client.post(self.url_delete)
        self.assertRedirects(response, '/publishers/', status_code=302)


class PublisherDetailViewTestCase(TestCase):

    def setUp(self):
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.client.login(username='john', password='123')
        self.publisher = Publisher.objects.create(
            name="ali", address="ryk", city="bwp", state_province="punjab",
            country="pak", website="https://www.google.com/"
        )
        self.url_delete = reverse('books:publisher-detail', kwargs={
                    'pk': self.publisher.pk,

                })

    def test_detail_template(self):

        resp = self.client.get(self.url_delete)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'book/publisher_detail.html')


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_publisher = 15

        for publisher_id in range(number_of_publisher):
            Author.objects.create(
                salutation='ali {publisher_id}', name='ryk {publisher_id}',
                email='https://www.google.com/ {publisher_id}',
                headshot='punjab {publisher_id}'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('books:author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('books:author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('books:author-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 5)


class AuthorCreateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='123')
        self.create_url = reverse('books:author-add')
        self.author1 = Author.objects.create(salutation="sir", name="ali", email="shah870@gmail.com", headshot="bwp")

    def test_create_success_url(self):
        response = self.client.post(self.create_url,
                                    {'salutation': 'sir',
                                     'name': 'ali',
                                     'email': 'shah870@gmail.com',
                                     'headshot': 'bwp',
                                     }
                                    )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/authors/')

    def test_publisher_POST_data(self):
        response = self.client.post(self.create_url)
        self.assertEquals(response.status_code, 200)


class AuthorUpdateTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(salutation='sir', name='Django')
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.client.login(username='john', password='123')
        self.update_url = reverse('books:author-update', args={'pk': self.user.id})

        self.url = reverse('books:author-update', kwargs={
            'pk': self.author.pk,

        })
        self.url_delete = reverse('books:author-delete', kwargs={
            'pk': self.author.pk,

        })


class AuthorUpdateViewTests(AuthorUpdateTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_update_author(self):
        book = Author.objects.create(name='The Catcher in the Rye')

        response = self.client.post(
            reverse('books:author-update', kwargs={'pk': book.id}),
            {'salutation': 'sir',
             'name': 'ali',
             'email': 'shah870@gmail.com',
             'headshot': 'bwp',
             })

        self.assertEqual(response.status_code, 302)

        book.refresh_from_db()
        self.assertEqual(book.email, 'shah870@gmail.com')

    def test_update_inputs(self):
        self.assertContains(self.response, '<name', 0)
        self.assertContains(self.response, '<headshot', 0)

    def test_view_class(self):
        view = resolve('/update/1/')
        self.assertEquals(view.func.view_class, AuthorUpdate)


class TestDeleteAuthor(AuthorUpdateTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)

    def test_my_get_request(self):
        response = self.client.get(self.url_delete)
        self.assertEqual(response.status_code, 200)

    def test_my_post_request(self):
        response = self.client.post(self.url_delete)
        self.assertRedirects(response, '/authors/', status_code=302)

class AuthorDetailViewTestCase(TestCase):
    '''Tests for the Article detail view'''

    def setUp(self):
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.client.login(username='john', password='123')
        self.author = Author.objects.create(salutation="sir", name="ali", email="shah870@gmail.com", headshot="bwp")
        self.url_delete = reverse('books:author-detail', kwargs={
                    'pk': self.author.pk,

                })

    def test_detail_template(self):

        resp = self.client.get(self.url_delete)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'book/author_detail.html')


class BooklistTest(TestCase):

    def setUp(self):
        number_of_publisher = 15

        for publisher_id in range(number_of_publisher):
            self.kid = mommy.make(Book, make_m2m=True)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/book_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['book_list']) == 10)

    def test_lists_all_books(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('books:book_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['book_list']) == 5)


# class BookCreateTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='john', password='123')
#         self.create_url = reverse('books:book-add')
#         self.author1 = mommy.make(Book, make_m2m=True)
#
#     def test_publisher_POST_data(self):
#         response = self.client.post(self.create_url)
#         self.assertEquals(response.status_code, 200)
#

class BookCreateTests(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(
            name="ali", address="ryk", city="bwp", state_province="punjab",
            country="pak", website="https://www.google.com/"
        )
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.author = Author.objects.create(salutation="sir", name="ali", email="shah870@gmail.com", headshot="bwp")
        self.book = mommy.make(Book, make_m2m=True)
        # Book.objects.create(title='python', authors=self.author.id, publisher=self.publisher.id,
        #                     publication_date="2001-01-01", created_by=user)
        url = reverse('books:book_list')
        self.response = self.client.get(url)
        self.create_url = reverse('books:book-add')

    def test_create_success_url(self):

        response = self.client.post(self.create_url,
                                            {'title': 'sir',
                                             'publisher': self.publisher.id,
                                             'authors': self.author.id,
                                             'publication_date': '2001-01-01',
                                             }
                                            )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/books/')

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/bookadd/')
        self.assertEquals(view.func.view_class, BookCreate)


class BookUpdateTestCase(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(
            name="ali", address="ryk", city="bwp", state_province="punjab",
            country="pak", website="https://www.google.com/"
        )
        self.author = Author.objects.create(salutation="sir", name="ali", email="shah870@gmail.com", headshot="bwp")
        self.book = mommy.make(Book, make_m2m=True)
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.client.login(username='john', password='123')
        self.update_url = reverse('books:book-update', args={'pk': self.user.id})

        self.url = reverse('books:book-update', kwargs={
            'pk': self.author.pk,

        })
        self.url_delete = reverse('books:book-delete', kwargs={
            'pk': self.author.pk,

        })


class BookUpdateViewTests(BookUpdateTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_update_author(self):
        book = mommy.make(Book, make_m2m=True)

        response = self.client.post(
            reverse('books:book-update', kwargs={'pk': book.id}),
            {'title': 'sir',
             'publisher': self.publisher.id,
             'authors': self.author.id,
             'publication_date': '2001-01-01',
             })

        self.assertEqual(response.status_code, 302)

        book.refresh_from_db()
        self.assertEqual(book.title, 'sir')

    def test_update_inputs(self):
        self.assertContains(self.response, '<title', 0)
        #self.assertContains(self.response, '<headshot', 0)

    def test_view_class(self):
        view = resolve('/bookupdate/1/')
        self.assertEquals(view.func.view_class, BookUpdate)

class TestDeleteBook(BookUpdateTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)

    def test_my_get_request(self):
        response = self.client.get(self.url_delete)
        self.assertEqual(response.status_code, 200)

    def test_my_post_request(self):
        response = self.client.post(self.url_delete)
        self.assertRedirects(response, '/books/', status_code=302)


class BookDetailViewTestCase(TestCase):
    '''Tests for the Article detail view'''

    def setUp(self):
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.client.login(username='john', password='123')
        self.book = mommy.make(Book, make_m2m=True)
        self.url_delete = reverse('books:book-detail', kwargs={
                    'pk': self.book.pk,

                })

    def test_detail_template(self):

        resp = self.client.get(self.url_delete)
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'book/book_detail.html')

