from django.shortcuts import render
from django.http import HttpResponse, Http404
from jinja2 import Environment, PackageLoader, select_autoescape

# Create your views here.


def index(request):

    env = Environment(
        loader=PackageLoader('app', 'templates'),
        autoescape=select_autoescape(['html', 'xml']),
    )

    template = env.get_template("index.html")
    return HttpResponse(template.render(number=42, string="xxx", collection=list(range(1, 51))))


