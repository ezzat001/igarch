from django.db import models
from django.contrib.auth.models import User


class AccountArchive(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    join_date = models.DateTimeField(blank=True,auto_now=True)


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)

    followers = models.IntegerField(blank=True,null=True)
    following = models.IntegerField(blank=True,null=True)
    mutual = models.IntegerField(blank=True,null=True)
    dont_follow_you_back = models.IntegerField(blank=True,null=True)
    you_dont_follow_back = models.IntegerField(blank=True,null=True)
    unfollowed_you = models.IntegerField(blank=True,null=True)

    followers_list = models.TextField(blank=True,null=True)
    following_list = models.TextField(blank=True,null=True)
    mutual_list = models.TextField(blank=True,null=True)
    dont_follow_you_back_list = models.TextField(blank=True,null=True)
    you_dont_follow_back_list = models.TextField(blank=True,null=True)

    unfollowed_you_list = models.TextField(blank=True,null=True)

    private_account = models.BooleanField(default=False)
    time = models.DateTimeField(blank=True,auto_now=True)

    def __str__(self):
        return str(self.user)+"#"+str(self.id)

class Stalked(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stalked_account = models.CharField(max_length=50)
    followers = models.IntegerField(blank=True, null=True)
    following = models.IntegerField(blank=True, null=True)
    followers_list = models.TextField(blank=True)
    following_list = models.TextField(blank=True)

    def __str__(self):
        return(self.stalked_account)

class StalkedAction(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    on_user = models.CharField(max_length=100)

    action = models.CharField(max_length=100)
    stalked_account = models.CharField(max_length=50)

    on_user = models.CharField(max_length=100)
    pic = models.TextField()
    time = models.DateTimeField(blank=True,auto_now=True)

    def __str__(self):
        return str(self.user)+"#"+str(self.id)

class PrivateUncoveredacc(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    uncovered = models.BooleanField(default=False)
    time = models.DateTimeField(blank=True,auto_now=True)

    def __str__(self):
        return self.username

def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return '{0}/{1}'.format(instance.user, filename)

class PrivateUncoveredPhoto(models.Model):
     id = models.AutoField(primary_key=True)
     user = models.ForeignKey(PrivateUncoveredacc, on_delete=models.CASCADE)
     caption = models.CharField(blank=True, max_length=100)
     likes = models.IntegerField(blank=True, null=True)
     img = models.ImageField(upload_to=user_directory_path)
     time = models.DateTimeField(blank=True,auto_now=True)



     def __str__(self):
         return str(self.user)

class PhotosArchive(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(blank=True, max_length=100)
    img_link = models.CharField(blank=True,max_length=1000)
    time = models.DateTimeField(blank=True,auto_now=True)

    def __str__(self):
        return self.username

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(blank=True, max_length=100)
    on = models.CharField(blank=True, max_length=100)
    time = models.DateTimeField(blank=True,auto_now=True)

    def __str__(self):
        return self.user
