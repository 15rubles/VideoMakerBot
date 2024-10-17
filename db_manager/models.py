from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Users(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(blank=False, null=False, max_length=100)
    client_type = models.CharField(blank=True, null=False, max_length=100)
    registered_at = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return self.user_id


class SocialMediaAccounts(models.Model):
    account_id = models.AutoField(primary_key=True, unique=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, unique=True)
    account_type = models.CharField(blank=True, null=False, max_length=100)
    account_username = models.CharField(blank=False, null=False, max_length=100)
    auth_key = models.CharField(blank=True, null=False, max_length=100)

    def __str__(self):
        return self.account_id


class GeneratedVideos(models.Model):
    video_id = models.AutoField(primary_key=True, unique=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, unique=True)
    creation_date = models.DateTimeField(blank=False, null=False)
    uploaded_date = models.DateTimeField(blank=False, null=False)
    is_uploaded = models.BooleanField(default=False)
    is_uploaded_manually_by_user = models.BooleanField(default=False)

    def __str__(self):
        return self.video_id

class OrderTypesDBNames(models.Model):
    order_type_id = models.AutoField(primary_key=True, unique=True)
    order_name = models.CharField(blank=False, null=False, max_length=100)

    def __str__(self):
        return self.order_type_id


# TODO: Scheduling
class Orders(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    order_id = models.AutoField(primary_key=True, unique=True)
    order_type_id = models.ForeignKey(OrderTypesDBNames, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(blank=False, null=False)
    order_status = models.CharField(blank=True, null=False, max_length=100)
    completion_date = models.DateTimeField(blank=False, null=False)
    desired_video_quantity = models.IntegerField(blank=False, null=False)
    uploaded_video_quantity = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.order_id


class YouTubeTwoVideosOrders(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    youtube_primary_link = models.CharField(blank=False, null=False, max_length=1000)
    youtube_secondary_link = models.CharField(blank=False, null=False, max_length=1000)
    description = models.CharField(blank=False, null=False, max_length=5000)
    hashtags = models.CharField(blank=False, null=False, max_length=5000)



class UserVideoOrders(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    video_id = models.ForeignKey(GeneratedVideos, on_delete=models.CASCADE)
    description = models.CharField(blank=False, null=False, max_length=5000)
    hashtags = models.CharField(blank=False, null=False, max_length=5000)



class RedditVideoOrders(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    reddit_link = models.CharField(blank=False, null=False, max_length=1000)
    youtube_video_link = models.CharField(blank=False, null=False, max_length=1000)
    description = models.CharField(blank=False, null=False, max_length=5000)
    hashtags = models.CharField(blank=False, null=False, max_length=5000)


