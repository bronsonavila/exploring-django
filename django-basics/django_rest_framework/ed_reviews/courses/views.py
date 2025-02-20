from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from . import serializers


# Extends a generic API view rather than the standard `APIView`.
class ListCreateCourse(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    # Specifies which serializer will be used on the queryset.
    serializer_class = serializers.CourseSerializer


class RetrieveUpdateDestroyCourse(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer


# v1 API

class ListCreateReview(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    # Override the default `get_queryset` method to have it use `course_pk`.
    def get_queryset(self):
        return self.queryset.filter(course_id=self.kwargs.get('course_pk'))

    # This method is run when an object is created by the view.
    def perform_create(self, serializer):
        # Prevent the user from assigning a `course_pk` which differs from the
        # primary key of the course in which the review is being submitted.
        course = get_object_or_404(
            models.Course, pk=self.kwargs.get('course_pk')
        )
        serializer.save(course=course)


class RetrieveUpdateDestroyReview(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    # `get_object` is similar to `get_queryset`, but instead gets a
    # single item rather than multiple items.
    def get_object(self):
        # Get a single object from the queryset that has the specified
        # `course_id` and `pk`. Ensures that an object can only be
        # updated or destroyed based on the query parameters provided.
        return get_object_or_404(
            self.get_queryset(),
            course_id=self.kwargs.get('course_pk'),
            pk=self.kwargs.get('pk')
        )


# v2 API

# Only allow superusers to delete objects. All other users can peform
# any other request.
class SuperUserCanDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'DELETE' or request.user.is_superuser:
            return True
        return False


class CourseViewSet(viewsets.ModelViewSet):
    # This will override the default permissions in `settings.py`.
    # The permission checks will run in the order they are listed.
    # Here, a non-superuser will not be able to delete a course,
    # even if they have that ability via Django permissions.
    permission_classes = (
        SuperUserCanDelete,
        permissions.DjangoModelPermissions
    )
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

    # This viewset method only applies to the detail view (rather than
    # the list view), and it will only work for GET requests.
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        # Calls the `pagination_class` set in `settings.py` with the
        # specified page size.
        self.pagination_class.page_size = 1
        reviews = models.Review.objects.filter(course_id=pk)

        page = self.paginate_queryset(reviews)

        if page is not None:
            serializer = serializers.ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


"""
`ModelViewSet` essentially consists of the following definitions:
    - `mixins.CreateModelMixin`
    - `mixins.RetrieveModelMixin`
    - `mixins.UpdateModelMixin`
    - `mixins.DestroyModelMixin`
    - `mixins.ListModelMixin`
    - `viewsets.GenericViewSet`

So if you want to customize a viewset that will not display a list view,
then simply create a new model that inherits from `GenericViewSet` and
all of the mixins execpt for `ListModelMixin`. The end result is that users
can retrieve individual reviews (e.g., `/api/v2/courses/1/reviews/2/`), but
they cannot retrieve a list of all reviews (e.g., `/api/v2/reviews/).
Attempting to go to the latter will yield: "Method 'GET' not allowed."
"""
# Mixins must be evaluated before the class they are modifying.


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
