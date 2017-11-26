from django import template
from django.utils.translation import get_language

from mtlpy.pages.models import I18NFlatPage


# Exemple d'utilisation:
# {% i18npage /about/ %}{% if found_page %}
# <li><a href="{{ found_page.get_absolute_url }}">{{ found_page.title }}</a></li>
# {% endif %}{% endi18npage %}


register = template.Library()


@register.tag('i18npage')
def i18n_page(parser, token):
    # parser.delete_first_token()
    nodelist = parser.parse(('endi18npage'))
    parser.delete_first_token()
    tokens = token.contents.split()
    return I18NPageNode(nodelist, *tokens)


class I18NPageNode(template.Node):

    def __init__(self, nodelist, _, url, language_code=None):
        self.url = url
        self.lang = language_code
        self.nodelist = nodelist

    def render(self, context):

        language_code = self.lang

        if not language_code:
            language_code = get_language()
        language_code = language_code[:2]

        try:
            page = I18NFlatPage.objects.get(url=self.url, listed=True)
        except I18NFlatPage.DoesNotExist:
            return self.nodelist.render(context)

        if page.language != language_code:
            try:
                page = page.translation
            except I18NFlatPage.DoesNotExist:
                return self.nodelist.render(context)
            else:
                if page.language != language_code:
                    return self.nodelist.render(context)

        context['found_page'] = page

        output = self.nodelist.render(context)

        del context['found_page']
        return output
