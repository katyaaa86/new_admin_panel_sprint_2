import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'person'
        verbose_name_plural = 'people'

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class Type(models.TextChoices):
        MOVIE = 'movie', _("Movie")
        TV_SHOW = 'tv_show', _("TV show")

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    rating = models.IntegerField(
        _('rating'), blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(_('type'), choices=Type.choices, default=Type.MOVIE, max_length=10)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    people = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'filmwork'
        verbose_name_plural = 'filmworks'
        indexes = [models.Index(fields=['creation_date'], name='film_work_creation_date_idx')]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [models.UniqueConstraint(fields=['film_work_id', 'genre_id'], name='film_work_genre_idx')]


class PersonFilmwork(UUIDMixin):

    class Role(models.TextChoices):
        DIRECTOR = 'director', _("director")
        WRITER = 'writer', _("writer")
        ACTOR = 'actor', _('actor')

    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=Role.choices, default=Role.ACTOR, max_length=10)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=['film_work_id', 'person_id', 'role'],
                name='film_work_person_role'
            ),
        ]
