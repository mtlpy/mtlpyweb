import datetime

from django.contrib import admin
from django import forms

from sorl.thumbnail.admin import AdminImageMixin

from mtlpy.models import EventSponsor
from .models import Post, Category, Video


class VideoAdminForm(forms.ModelForm):
    class Meta:
        model = Video

    def __init__(self, *args, **kwds):
        super(VideoAdminForm, self).__init__(*args, **kwds)
        self.fields['post'].queryset = Post.objects.order_by("slug")


class EventSponsorshipInline(admin.StackedInline):
    model = EventSponsor
    extra = 1


class VideoInline(admin.StackedInline):
    prepopulated_fields = {"slug": ("title_en", "title_fr")}
    fields = (
        'title_en',
        'title_fr',
        'slug',
        'code',
        )
    model = Video
    extra = 1


class CatAdmin(admin.ModelAdmin, AdminImageMixin):
    list_display = ('slug', 'title_en', 'title_fr', 'post_count')
    prepopulated_fields = {"slug": ("title_en", "title_fr")}
    fields = (
        'title_en',
        'title_fr',
        'slug',
        'logo',
        )

    def post_count(self, obj):
        return obj.posts.all().count()


class VideoAdmin(admin.ModelAdmin, AdminImageMixin):
    form = VideoAdminForm
    list_display = ('slug', 'title_en', 'title_fr', 'code', 'post')
    prepopulated_fields = {"slug": ("title_en", "title_fr")}
    fields = (
        'title_en',
        'title_fr',
        'slug',
        'code',
        'post',
        )


class PostAdmin(admin.ModelAdmin, AdminImageMixin):
    class Media:
        js = ("js/markdown-0.5.0.js", "js/post_admin.js")
    list_display = ('slug', 'title', 'status', 'category')
    list_filter = ('category', 'status')
    actions = ('make_published', 'make_draft')
    inlines = [EventSponsorshipInline, VideoInline]
    prepopulated_fields = {"slug": ("title_en", "title_fr")}

    def make_published(self, request, queryset):
        queryset.update(status=2)
        queryset.filter(publish=None).update(publish=datetime.date.today())

    make_published.short_description = 'Mark selected as published'

    def make_draft(self, request, queryset):
        queryset.update(status=1)
    make_draft.short_description = 'Mark selected as draft'

    fields = (
        'title_en',
        'title_fr',
        'slug',
        'content_en',
        'content_fr',
        'publish',
        'status',
        'logo',
        'author',
        'category',
        )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CatAdmin)
admin.site.register(Video, VideoAdmin)
