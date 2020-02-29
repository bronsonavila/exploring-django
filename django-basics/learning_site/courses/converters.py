# Custom path converters provide for more complex path matching requirements using regular expressions.
# See: https://docs.djangoproject.com/en/3.0/topics/http/urls/#registering-custom-path-converters
class QuestionType:
    regex = 'mc|tf'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return value
