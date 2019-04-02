from django.urls import path
import book.views
from book.views import PublisherDetail, PublisherList, BookList,  BookDetail, AuthorDetailView, \
    AuthorCreate, AuthorUpdate, AuthorDelete, AuthorList, PublisherCreate, PublisherUpdate, PublisherDelete, BookCreate, \
    BookUpdate, BookDelete

app_name = 'books'
urlpatterns = [
    path('', book.views.home, name="home"),
    path('publishers/', PublisherList.as_view(), name='publisher_list'),
    path('publisheradd/', PublisherCreate.as_view(), name='publisher-add'),
    path('publisherupdate/<pk>/', PublisherUpdate.as_view(), name='publisher-update'),
    path('publisher/<pk>/delete/', PublisherDelete.as_view(), name='publisher-delete'),
    path('<int:pk>/', PublisherDetail.as_view(), name='publisher-detail'),
    path('books/', BookList.as_view(), name='book_list'),
    path('bookadd/', BookCreate.as_view(), name='book-add'),
    path('bookupdate/<pk>/', BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', BookDelete.as_view(), name='book-delete'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('authors/', AuthorList.as_view(), name='author-list'),
    path('authors/<pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('add/', AuthorCreate.as_view(), name='author-add'),
    path('update/<pk>/', AuthorUpdate.as_view(), name='author-update'),
    path('authors/<pk>/delete/', AuthorDelete.as_view(), name='author-delete'),
]
