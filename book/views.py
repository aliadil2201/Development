from book.forms import MyCommentForm
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic import ListView
from book.models import Book, Publisher
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from book.models import Author
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'book/home.html')


class PublisherList(ListView):
    model = Publisher
    paginate_by = 10
    template_name = 'book/publisher_list.html'


class PublisherCreate(CreateView):
    template_name = 'book/publisher_form.html'
    queryset = Publisher.objects.all()
    model = Publisher
    fields = ['name', 'address', 'city', 'state_province', 'country', 'website']

    def get_success_url(self):
        return reverse_lazy('books:publisher_list')


class PublisherUpdate(UpdateView):
    template_name = 'book/publisher_update_form.html'
    queryset = Publisher.objects.all()
    model = Publisher
    fields = ['name', 'address', 'city', 'state_province', 'country', 'website']

    def get_success_url(self):
        return reverse_lazy('books:publisher_list')


class PublisherDelete(DeleteView):
    template_name = 'book/publisher_confirm_delete.html'
    queryset = Publisher.objects.all()
    model = Publisher
    fields = ['name']

    def get_success_url(self):
        return reverse_lazy('books:publisher_list')


class PublisherDetail(DetailView):

    model = Publisher

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the Publisher
        context['book_list'] = Publisher.objects.all()
        return context


class BookList(ListView):
    model = Book
    paginate_by = 10
    template_name = 'book/book_list.html'


class BookCreate(CreateView):
    template_name = 'book/book_form.html'
    queryset = Book.objects.all()
    model = Book
    fields = ['title', 'authors', 'publisher', 'publication_date']

    def get_success_url(self):
        return reverse_lazy('books:book_list')


class BookUpdate(UpdateView):
    template_name = 'book/book_update_form.html'
    queryset = Book.objects.all()
    model = Book
    fields = ['title', 'authors', 'publisher', 'publication_date']

    def get_success_url(self):
        return reverse_lazy('books:book_list')


class BookDelete(DeleteView):
    template_name = 'book/book_confirm_delete.html'
    queryset = Book.objects.all()
    model = Book
    fields = ['name']

    def get_success_url(self):
        return reverse_lazy('books:book_list')


class BookDetail(DetailView):
    queryset = Book.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj


class AuthorDetailView(DetailView):

    queryset = Author.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj


class AuthorList(ListView):
    model = Author
    paginate_by = 10
    template_name = 'book/author_list.html'


class AuthorUpdate(UpdateView):
    template_name = 'book/author_update_form.html'
    queryset = Author.objects.all()
    model = Author
    fields = ['name','email']

    def get_success_url(self):
        return reverse_lazy('books:author-list')


class AuthorDelete(DeleteView):
    template_name = 'book/author_confirm_delete.html'
    queryset = Author.objects.all()
    model = Author
    fields = ['name']

    def get_success_url(self):
        return reverse_lazy('books:author-list')


class AuthorCreate(CreateView):
    template_name = 'book/author_form.html'
    queryset = Author.objects.all()
    model = Author
    fields = ['salutation', 'name', 'email']

    def get_success_url(self):
        return reverse_lazy('books:author-list')
