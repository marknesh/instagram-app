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

    def findprofile(cls,name):
        foundprofile=cls.objects.filter(username__icontains=name).all()
        return foundprofile



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
    likes = models.PositiveIntegerField(default=0)



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

    @classmethod
    def get_followers(cls, profile_id):
        profile = Profile.objects.filter(id=profile_id)
        followers = cls.objects.filter(user=profile.user.id)
        return len(followers)


class Like(models.Model):
    '''
    Class defines the structure of a like on a an posted Image
    '''
    user = models.ForeignKey(User,on_delete=models.CASCADE, null= True)

    image = models.ForeignKey(Image,on_delete=models.CASCADE, null = True)

    def __int__(self):
        return self.user.username

    def save_like(self):
        self.save()

    def unlike(self):
        self.delete()

    def like(self):
        self.likes_number = 2
        self.save()

    @classmethod
    def get_likes(cls,image_id):
        '''
        Function that get likes belonging to a paticular posts
        '''
        likes = cls.objects.filter(image = image_id)
        return likes



# Create your models here.
