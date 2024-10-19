from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client_type = models.CharField(blank=False, null=False, max_length=100)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class SocialMediaAccounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(blank=True, null=False, max_length=100)
    account_username = models.CharField(blank=False, null=False, max_length=100)
    auth_key = models.CharField(blank=True, null=False, max_length=100)

    def __str__(self):
        return self.account_username


class GeneratedVideos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_ref_id = models.CharField(blank=False, null=False, max_length=1000, default='')
    creation_date = models.DateTimeField(auto_now_add=True)
    uploaded_date = models.DateTimeField(blank=False, null=False)
    is_uploaded = models.BooleanField(default=False)
    is_uploaded_manually_by_user = models.BooleanField(default=False)

    def __str__(self):
        return f'Video {self.id} by {self.user.username}'

class OrderTypesDBNames(models.Model):
    order_type_db_name = models.CharField(blank=False, null=False, max_length=100)

    def __str__(self):
        return self.order_type_db_name


# TODO: Scheduling
class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_type = models.ForeignKey(OrderTypesDBNames, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(blank=True, null=True, max_length=100)
    completion_date = models.DateTimeField(blank=True, null=True)
    desired_video_quantity = models.IntegerField(blank=False, null=False)
    uploaded_video_quantity = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'


class YouTubeTwoVideosOrders(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    youtube_primary_link = models.CharField(blank=False, null=False, max_length=1000)
    youtube_secondary_link = models.CharField(blank=False, null=False, max_length=1000)
    description = models.CharField(blank=True, null=True, max_length=5000)
    hashtags = models.CharField(blank=True, null=True, max_length=5000)



class UserVideoOrders(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    video = models.ForeignKey(GeneratedVideos, on_delete=models.CASCADE)
    description = models.CharField(blank=False, null=False, max_length=5000)
    hashtags = models.CharField(blank=False, null=False, max_length=5000)



class RedditVideoOrders(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    reddit_link = models.CharField(blank=False, null=False, max_length=1000)
    youtube_video_link = models.CharField(blank=False, null=False, max_length=1000)
    description = models.CharField(blank=False, null=False, max_length=5000)
    hashtags = models.CharField(blank=False, null=False, max_length=5000)


