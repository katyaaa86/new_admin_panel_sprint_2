from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import OuterRef
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Filmwork.objects.prefetch_related('genres', 'people') \
            .values('id', 'title', 'description', 'creation_date', 'rating', 'type') \
            .annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArraySubquery(
                PersonFilmwork.objects.filter(film_work_id=OuterRef('id'), role='actor').values('person__full_name')),
            directors=ArraySubquery(PersonFilmwork.objects.filter(film_work_id=OuterRef('id'), role='director').values(
                'person__full_name')),
            writers=ArraySubquery(
                PersonFilmwork.objects.filter(film_work_id=OuterRef('id'), role='writer').values('person__full_name')),
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': (page.number-1) if page.has_previous() else None,
            'next': (page.number+1) if page.has_next() else None,
            'results': list(self.get_queryset()),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_object()
