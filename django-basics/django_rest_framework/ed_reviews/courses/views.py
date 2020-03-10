from django.shortcuts import get_object_or_404

from rest_framework import generics
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

class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

    # This viewset method only applies to the detail view (rather than
    # the list view), and it will only work for GET requests.
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        course = self.get_object()
        serializer = serializers.ReviewSerializer(
            course.reviews.all(), many=True
        )
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
