import re
from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def upload_image(filename, image_request):
	img_dict = re.match("data:(?P<type>.*?);(?P<encoding>.*?),(?P<data>.*)", image_request).groupdict()
	blob = img_dict['data'].decode(img_dict['encoding'], 'strict')
	image = StringIO(blob)
	image = InMemoryUploadedFile(image, None, filename, 'image/jpeg', image.len, None)

	return image