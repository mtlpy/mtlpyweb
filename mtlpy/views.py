# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django import forms
from django.utils.translation import gettext_lazy as _
from django.shortcuts import (render, render_to_response,
                              get_object_or_404, redirect)
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

from mtlpy.blog.models import Post
from mtlpy.api.videos import get_all_videos
from .models import Sponsor


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    message = forms.CharField()
    email = forms.EmailField()


def home_page(request):
    posts = Post.published_objects.all()[:3]
    sponsors = (Sponsor.objects
                .filter(frontpage=True)
                .filter(~Q(partner=True))
                .order_by('ordering'))
    partners = (Sponsor.objects.filter(frontpage=True, partner=True)
                .order_by('ordering'))
    ctx = {
        'blog_posts': posts,
        'sponsors': sponsors,
        'partners': partners,
        }
    return render_to_response(
        'index.html', ctx,
        context_instance=RequestContext(request)
        )


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            recipients = settings.CONTACT_EMAILS
            message = _('From: %(name)s\n\nMessage: %(message)s') % {
                'name': name,
                'message': message,
            }
            subject = _('Message from MontrealPython.org contact form')
            send_mail(subject, message, sender, recipients)
    else:
        form = ContactForm()

    return render(request, "contact.html", {
        'form': form,
        'contact_email': settings.CONTACT_EMAILS[0],
    })


def styleguide(request):
    return render_to_response('styleguide.html', {},
                              context_instance=RequestContext(request))


def videos(request):
    videos = get_all_videos(settings.YOUTUBE_URL)
    return render_to_response('videos.html', {"videos": videos},
                              context_instance=RequestContext(request))


def sponsor_details(request, slug):
    sponsor = get_object_or_404(Sponsor, slug=slug)
    return render_to_response('sponsor_details.html', {"sponsor": sponsor},
                              context_instance=RequestContext(request))


def sponsorship(request):
    sponsors = (Sponsor.objects
                .filter(frontpage=True)
                .filter(~Q(partner=True))
                .order_by('ordering'))
    return render_to_response('sponsorship.html', {"sponsors": sponsors},
                              context_instance=RequestContext(request))
