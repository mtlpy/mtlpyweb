from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from django.views.generic import ListView

from .models import Post, Category
from .forms import CatTransferForm


class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 10
    queryset = Post.published_objects.all()
    template_name = 'category.html'

    @cached_property
    def category(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Category, slug=slug) if slug else None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category=self.category) if self.category else qs


class UserPostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 10
    queryset = Post.published_objects.all()
    template_name = 'category.html'

    @cached_property
    def user(self):
        return get_object_or_404(User, id=self.kwargs['userid'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.user
        return context

    def get_queryset(self):
        return super().get_queryset().filter(author=self.user)


def post(request, year, month, slug):
    article = get_object_or_404(Post, publish__year=year,
                                publish__month=month, slug=slug)
    ctx = {'article': article}
    return render(request, 'article.html', ctx)


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
