from __future__ import unicode_literals
import os.path

from django.core.files.storage import default_storage as storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.six import StringIO
from django.utils.encoding import smart_text

try:
    import Image
except ImportError:
    try:
        from PIL import Image
    except ImportError:
        raise ImportError('Cannot import Python Image Library')


class ImageManipulator():

    def __init__(self, format="PNG", extension="png", quality=75):
        self.format = format
        self.extension = extension
        self.quality = quality

    # define the path for the resized image
    def resized_path(self, path, size, method):
        directory, name = os.path.split(path)
        image_name, ext = name.rsplit('.', 1)

        return os.path.join(directory,
                            smart_text('{}_{}_{}.{}').format(image_name,
                                                             method,
                                                             size,
                                                             self.extension))


    # take an image, create a copy and scale the copied image
    def scale(self, image_field, size):

        image_path = self.resized_path(image_field.name, size, 'scale')
        image_dir, image_filename = os.path.split(image_path)

        if not storage.exists(image_path):
            f = storage.open(image_field.name, 'r')
            image = Image.open(f)

            if image.mode != 'RGB':
                image = image.convert('RGB')

            width, height = [int(i) for i in size.split('x')]

            image.thumbnail((width, height), Image.ANTIALIAS)
            f_scale = StringIO()

            image.save(f_scale, self.format, quality=self.quality)
            f_scale.seek(0)
            suf = SimpleUploadedFile(os.path.split(image_path)[-1].split('.')[0],
                                     f_scale.read(),
                                     content_type='image/{}'.format(
                                         self.format.lower()))

            return image_filename, suf

        return image_filename, None

