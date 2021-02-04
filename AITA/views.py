from django.shortcuts import render
from .models import Post

import random


def landing_page(request):
    return render(request, 'AITA/landing.html')


def intro(request):
    return render(request, 'AITA/intro.html')


def show_post(request):
    post = Post.objects.all()
    random_post = random.choice(post)
    context = {
        'post': random_post
    }
    return render(request, 'AITA/detail.html', context=context)
