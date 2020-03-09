from django.test import TestCase
from .models import Image


class ImageTest(TestCase):

    def setUp(self):
        self.image=Image(title="fff",caption="VV",pub_date="DD",image="mm",comments="FF",profile=3,comments_number=3,likes=4)


    def test_instance(self):
        self.assertTrue(isinstance(self.image,Image))

    def test_save_method(self):
        self.image.save_image()
        IMage = Image.objects.all()
        self.assertTrue(len(IMage) > 0)



# Create your tests here.
