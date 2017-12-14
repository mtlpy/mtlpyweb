from django.utils.translation import get_language
from django.conf import settings


def i18n_field(name, default=settings.LANGUAGE_CODE[:2], fallback=True):
    # This creates a property on this model, that will basically attempt
    # to access a property called <name>_<get_language()>, else return
    # return <name>_<default>.
    #
    # Sample usage:
    # class User(models.Model):
    #     bio_en = models.TextField(blank=True, null=True)
    #     bio_fr = models.TextField(blank=True, null=True)
    #     bio = i18n_field('bio')
    #
    # user1 = User.objects.get(id=1)
    # print user1.bio
    #
    # 'fallback' parameter will allow the field to return the default
    # language value if the requested language content does not exist.

    @property
    def i18n_field_getter(inst):
        lang = get_language()[:2]
        try:
            res = getattr(inst, '_'.join((name, lang)))
            if not res and fallback:
                res = getattr(inst, '_'.join((name, default)))
        except AttributeError:
            res = getattr(inst, '_'.join((name, default)))

        return res

    return i18n_field_getter
