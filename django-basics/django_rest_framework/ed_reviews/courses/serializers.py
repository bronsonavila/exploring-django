from rest_framework import serializers

from . import models


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = (
            'id',
            'course',
            'name',
            'email',
            'comment',
            'rating',
            'created_at',
        )
        # Sepcify that the `email` field can be supplied by the user,
        # but it will not be sent back out upon serialization.
        extra_kwargs = {
            'email': {'write_only': True}
        }


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = (
            'id',
            'title',
            'url',
        )
