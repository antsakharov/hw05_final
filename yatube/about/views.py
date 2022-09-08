from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Класс отображения страницы Об Авторе"""
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """Класс отображения страницы Технологии"""
    template_name = 'about/tech.html'
