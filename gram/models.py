from django.db import models
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User


class Profile(models.Model):
    profile_photo=models.ImageField(upload_to='profilepics/')
    bio=HTMLField()
    username = models.CharField(max_length=30,default='User')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod



    def profileid(cls,id):
        u = cls.objects.get(pk=id)
        return u

class Image(models.Model):
    title=models.CharField(max_length=20)
    caption=models.CharField(max_length=20)
    image=models.ImageField(upload_to='images/')
    pub_date=models.DateTimeField(auto_now_add=True)
    profile=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    comments_number = models.PositiveIntegerField(default=0)


    class Meta:
        ordering = ['pub_date']


    def save_image(self):
         self.save()

    def delete_image(self):
        self.delete()


    @classmethod
    def allimages(cls):
        images=cls.objects.all().order_by('-pub_date')
        return images


class Comment(models.Model):
    '''
    class that defines the structure of an comment on image
    '''
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, null= True)
    image_id = models.ForeignKey(Image,on_delete=models.CASCADE, null= True)
    comment= models.TextField(blank=True)


    def __str__(self):
        return self.comment

    def save_comment(self):
        '''
        method that save a comment on an image
        '''
        self.save()
    def delete_comment(self):
        '''
        methods that deletes a comment on an image
        '''
        self.delete()


class Follow(models.Model):
    '''
    Class that defines followers of each user
    '''
    follower = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    def __int__(self):
        return self.follower.username

    def save_follower(self):
        self.save()





# Create your models here.
