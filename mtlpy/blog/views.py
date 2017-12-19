from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from .models import Post, Category
from .forms import CatTransferForm


def category(request, slug=None):
    if slug:
        instance = get_object_or_404(Category, slug=slug)
        all_posts = Post.published_objects.filter(category=instance)
    else:
        instance = None
        all_posts = Post.published_objects.all()

    ctx = {'category': instance, 'posts': all_posts}
    return render(request, 'category.html', ctx)


def post(request, year, month, slug):
    article = get_object_or_404(Post, publish__year=year,
                                publish__month=month, slug=slug)
    ctx = {'article': article}
    return render(request, 'article.html', ctx)


def user_posts(request, userid):
    user = get_object_or_404(User, id=userid)
    all_posts = Post.objects.filter(author=user, publish__isnull=False)

    ctx = {'author': user, 'posts': all_posts}
    return render(request, 'category.html', ctx)


@staff_member_required
def transfer_posts_tool(request):
    if request.method == 'POST':
        form = CatTransferForm(request.POST)
        if form.is_valid():
            Post.objects.filter(category__in=form.cleaned_data['from_cats']).update(
                category=form.cleaned_data['to_cat'])

    else:
        form = CatTransferForm()

    ctx = {
        'form': form,
    }
    return render(request, 'transfer_tool.html', ctx)
