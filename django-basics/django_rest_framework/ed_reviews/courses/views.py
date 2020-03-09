from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers


class ListCreateCourse(APIView):
    # `format` controls the format of the output.
    def get(self, request, format=None):
        courses = models.Course.objects.all()
        # Use `many=True` when serializing multipe objects.
        serializer = serializers.CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.CourseSerializer(data=request.data)
        # Returns a 400 Bad Request error if the data is not valid.
        serializer.is_valid(raise_exception=True)
        # `save()` both saves the data to the database and updates
        #  `serializer.data` to include all fields entered into the
        # database, such as the primary key and `created_at` values.
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
