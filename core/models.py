from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


SHELF_CHOICES = (
    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)
)

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'languages'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name=_("Title"))
    author = models.CharField(max_length=100, null=False, blank=False, verbose_name=_("Author"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='books', null=True, blank=True, verbose_name=_("Language"))
    publication_year = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Publication Year"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shelf = models.PositiveIntegerField(null=True, blank=True, choices=SHELF_CHOICES, verbose_name=_("Shelf"))
    genre = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', null=True, blank=True, verbose_name=_("Genre"))
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True, verbose_name=_("Book Cover"))
    book_count = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Quantity"))

    class Meta:
        db_table = 'books'

    def not_in_stock(self):
        if self.book_count <= 0:
            return True
        else:
            return False



class BookLibrary(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='books_library')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books_library')
    book_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('book', 'user')