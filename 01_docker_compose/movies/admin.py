from django.contrib import admin

from movies.models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description', 'id',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 0


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 0


@admin.register(Filmwork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres',)
    list_prefetch_related = ('people', 'genres',)
    list_filter = ('type', 'creation_date', 'genres',)
    search_fields = ('title', 'description', 'id',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related(*self.list_prefetch_related)
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'
