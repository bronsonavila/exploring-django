from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers


class ListCourse(APIView):
    # `format` controls the format of the output.
    def get(self, request, format=None):
        courses = models.Course.objects.all()
        # Use `many=True` when serializing multipe objects.
        serializer = serializers.CourseSerializer(courses, many=True)
        return Response(serializer.data)
