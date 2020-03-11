from django.db.models import Avg

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

    # Just as with field-level validations for forms (e.g., `clean_field`),
    # custom serializer validation methods must be `validate_field`.
    def validate_rating(self, value):
        if value in range(1, 6):
            return value
        raise serializers.ValidationError(
            'Rating must be an integer between 1 and 5'
        )


class CourseSerializer(serializers.ModelSerializer):
    """
    Automatically include any reviews related to a course instance.
    NOTE: This will bring in EVERY review related to the course, so
    this method is best when only working with limited amounts of data
    (ideally situations where there's just a one-to-one relationship).
    """
    # reviews = ReviewSerializer(many=True, read_only=True)

    """
    Alternative to the above, in which you only fetch the hyperlink(s)
    of related field(s), rather than all the data from the related object.
    `review-detail` is the automatically-generated view name for the
    viewset in the API v2 router. NOTE: This will still return ALL items.
    See: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
    """
    # reviews = serializers.HyperlinkedRelatedField(many=True,
    #                                               read_only=True,
    #                                               view_name='apiv2:review-detail')

    """
    Another option in which you only fetch the primary key(s) of related
    field(s). This is generally the fastest option.
    """
    reviews = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = (
            'id',
            'title',
            'url',
            # Should correspond to the `related_name` in `models.py`:
            'reviews',
            'average_rating',
        )

    # When working with `SerializerMethodField` to add custom data to the
    # serialized output, the method needs to follow a `get_field` pattern.
    # `obj` is the object that is being serialized.
    def get_average_rating(self, obj):
        # NOTE: This is probably not the best way to get average ratings,
        # as it will be taxing on your query time as the database continues
        # to grow. It would be best to add an `average_rating` field to the
        # model itself and store a value that is calculated and updated
        # each time a review is submitted using Django's `signals`.
        average = obj.reviews.aggregate(Avg('rating')).get('rating__avg')

        if average is None:
            return 0
        # Ensure you're always dealing 0.5 increments (e.g., 1.0, 2.5, etc.).
        return round(average * 2) / 2

