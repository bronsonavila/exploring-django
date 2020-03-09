class PageTitleMixin:
    page_title = ''

    # Allows page title to be set dynamically.
    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        return context
