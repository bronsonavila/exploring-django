from django.contrib import admin
from datetime import date

from . import models


def make_published(modeladmin, request, queryset):
    queryset.update(status='p', published=True)


# The message users will see when using the "Action" dropdown menu
# to change the published status of their courses.
make_published.short_description = 'Mark selected courses as Published'


class TextInline(admin.StackedInline):
    model = models.Text
    fieldsets = (
        (None, {
            'fields': (('title', 'order'), 'description', 'content')
        }),
    )


class QuizInline(admin.StackedInline):
    model = models.Quiz


class AnswerInline(admin.TabularInline):
    model = models.Answer


class YearListFilter(admin.SimpleListFilter):
    # `title` appears after the word "By" in the filter sidebar.
    title = 'year created'
    # `parameter_name` is used in the URL whenever the filter is selected.
    parameter_name = 'year'

    # Creates the clickable links for the filter. Returns a tuple of tuples.
    def lookups(self, request, model_admin):
        return (
            # First value appears in the URL, the second in the sidebar.
            ('2016', '2016'),
            ('2019', '2019'),
            ('2020', '2020'),
        )

    # Returns the objects that fit the parameters of the filter.
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                created_at__gte=date(int(self.value()), 1, 1),
                created_at__lte=date(int(self.value()), 12, 31)
            )


class CourseAdmin(admin.ModelAdmin):
    inlines = [TextInline, QuizInline]
    # Insert the name of attributes that will be made searchable.
    search_fields = ['title', 'description']
    # Filter courses by creation date and "live" status.
    list_filter = ['created_at', 'published', YearListFilter]
    # Show additional fields along with the title in list view.
    list_display = ['title',
                    'created_at',
                    'time_to_complete',
                    'published',
                    'status']
    list_editable = ['status']
    # Add the `make_published()` function to the "Action" dropdown menu.
    actions = [make_published]

    class Media:
        js = ('js/vendor/markdown.js', 'js/preview.js')
        css = {
            'all': ('css/preview.css',),
        }


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    search_fields = ['prompt']
    list_display = ['prompt', 'quiz', 'order']
    list_editable = ['quiz', 'order']
    # Displays the quiz options as a set of horizontal radio buttons.
    radio_fields = {'quiz': admin.HORIZONTAL}


class QuizAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'description', 'order', 'total_questions']


class TextAdmin(admin.ModelAdmin):
    # Do not use `fields` when using `fieldsets`.
    # fields = ['course', 'title', 'order', 'description', 'content']

    # `fieldsets` is a list of two-tuples. Each two-tuple represents a
    # separate section of the form.
    fieldsets = (
        # The first element is the heading that will be displayed above the
        # fieldset; the second element consists of the field options.
        (None, {
            'fields': ('course', 'title', 'order', 'description')
        }),
        ('Add content', {
            # Trailing comma indicates this is a tuple.
            'fields': ('content',),
            'classes': ('collapse',)  # Makes the section collapsible.
        })
    )


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Text, TextAdmin)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.MultipleChoiceQuestion, QuestionAdmin)
admin.site.register(models.TrueFalseQuestion, QuestionAdmin)
admin.site.register(models.Answer)
