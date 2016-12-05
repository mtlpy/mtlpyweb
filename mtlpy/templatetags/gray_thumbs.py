from sorl.thumbnail.conf import settings, defaults as default_settings
from sorl.thumbnail.helpers import tokey, serialize
from sorl.thumbnail import default
from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode
from sorl.thumbnail.images import ImageFile
from sorl.thumbnail.images import DummyImageFile
from sorl.thumbnail.parsers import parse_geometry
from sorl.thumbnail.base import ThumbnailBackend, EXTENSIONS
from PIL.Image import MODES
from django.template import Library


register = Library()

TO_GRAY_INTENSITY = 0.5

class GrayBackend(ThumbnailBackend):

    def get_thumbnail(self, file_, geometry_string, **options):
        """
        Returns thumbnail as an ImageFile instance for file with geometry and
        options given. First it will try to get it from the key value store,
        secondly it will create it.
        """
        source = ImageFile(file_)
        for key, value in self.default_options.iteritems():
            options.setdefault(key, value)
        # For the future I think it is better to add options only if they
        # differ from the default settings as below. This will ensure the same
        # filenames beeing generated for new options at default.
        for key, attr in self.extra_options:
            value = getattr(settings, attr)
            if value != getattr(default_settings, attr):
                options.setdefault(key, value)
        name = self._get_thumbnail_filename(source, geometry_string, options)
        thumbnail = ImageFile(name, default.storage)
        cached = default.kvstore.get(thumbnail)
        if cached:
            return cached
        if not thumbnail.exists():
            # We have to check exists() because the Storage backend does not
            # overwrite in some implementations.
            source_image = default.engine.get_image(source)
            # We might as well set the size since we have the image in memory
            size = default.engine.get_image_size(source_image)
            source.set_size(size)
            self._create_thumbnail(source_image, geometry_string, options,
                                   thumbnail)
        # If the thumbnail exists we don't create it, the other option is
        # to delete and write but this could lead to race conditions so I
        # will just leave that out for now.
        default.kvstore.get_or_set(source)
        default.kvstore.set(thumbnail, source)
        return thumbnail

    @staticmethod
    def __calc_new_intensity(px):
        """
        To grayscale, and reduce intensity by TO_GRAY_INTENSITY
        """

        # Calc new px intensity

        grayscale = sum(px[:3]) / 3.0
        new_px = [int((
            grayscale + ((255 - grayscale) * (1 - TO_GRAY_INTENSITY))
        ))] * 3

        # Add alpha channel
        new_px.append(px[3])

        return tuple(new_px)

    def _create_thumbnail(self, source_image, geometry_string, options,
                          thumbnail):
        """
        Creates the thumbnail by using default.engine
        """
        ratio = default.engine.get_image_ratio(source_image, options)
        geometry = parse_geometry(geometry_string, ratio)
        image = default.engine.create(source_image, geometry, options)

        # To RGBA!
        image = image.convert(mode='RGBA')

        # Per pixel calculations.
        #
        # This is slow and could be optimized.. but it works in any case.
        new_data = []
        for item in image.getdata():
            # If px is white, make transparent
            if item[:3] == (255,255,255):
                new_data.append((255, 255, 255, 0))
                continue

            # All other pixels are "whitened" by TO_GRAY_INTENSITY
            # (given that 0 is white and 1 is original intensity)

            converted_pixel = self.__calc_new_intensity(item)

            new_data.append(converted_pixel)

        image.putdata(new_data)
        default.engine.write(image, options, thumbnail)
        # It's much cheaper to set the size here
        size = default.engine.get_image_size(image)
        thumbnail.set_size(size)


    def _get_thumbnail_filename(self, source, geometry_string, options):
        """
        Computes the destination filename.
        """
        key = tokey(source.key, geometry_string, serialize(options), 'gray')
        # make some subdirs
        path = '%s/%s/%s' % (key[:2], key[2:4], key)
        return '%s%s.%s' % (settings.THUMBNAIL_PREFIX, path,
                            EXTENSIONS[options['format']])

backend = GrayBackend()


class GrayThumbnailNode(ThumbnailNode):
    def _render(self, context):
        file_ = self.file_.resolve(context)
        geometry = self.geometry.resolve(context)
        options = {}
        for key, expr in self.options:
            noresolve = {u'True': True, u'False': False, u'None': None}
            value = noresolve.get(unicode(expr), expr.resolve(context))
            if key == 'options':
                options.update(value)
            else:
                options[key] = value
        if settings.THUMBNAIL_DUMMY:
            thumbnail = DummyImageFile(geometry)
        elif file_:
            thumbnail = backend.get_thumbnail(
                file_, geometry, **options
                )
        else:
            return self.nodelist_empty.render(context)
        context.push()
        context[self.as_var] = thumbnail
        output = self.nodelist_file.render(context)
        context.pop()
        return output


@register.tag
def gray_thumbnail(parser, token):
    return GrayThumbnailNode(parser, token)
