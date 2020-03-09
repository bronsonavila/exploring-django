from rest_framework import generics

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
