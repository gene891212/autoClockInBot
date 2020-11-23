import markdown
from django.shortcuts import get_object_or_404, render

from .models import *
# Create your views here.


def detail(request, title):
    print(title)
    disease = get_object_or_404(Disease, title=title)
    # disease = Post.objects.get(title='title')
    disease.body = markdown.markdown(
        disease.body,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )

    return render(request, 'mdblog/detail.html', context={'disease': disease})

from django.views import generic

class DiseaseListView(generic.ListView):
    model = Disease