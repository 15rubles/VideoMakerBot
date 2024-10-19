from django.contrib import admin
from db_manager.models import *

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','client_type','registered_at']

class SocialMediaAccountsAdmin(admin.ModelAdmin):
    list_display = ['id','user','account_type','account_username']

class GeneratedVideosAdmin(admin.ModelAdmin):
    list_display = ['id','user','video_ref_id','creation_date','uploaded_date','is_uploaded','is_uploaded_manually_by_user']

class OrderTypesDBNamesAdmin(admin.ModelAdmin):
    list_display = ['order_type_db_name']

class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id','user','order_type_id','creation_date','order_status','completion_date','desired_video_quantity','uploaded_video_quantity']

class YouTubeTwoVideosOrdersAdmin(admin.ModelAdmin):
    list_display = ['order','youtube_primary_link','youtube_secondary_link','description','hashtags']

class UserVideoOrdersAdmin(admin.ModelAdmin):
    list_display = ['order','video_id','description','hashtags']

class RedditVideoOrdersAdmin(admin.ModelAdmin):
    list_display = ['order','reddit_link','youtube_video_link','description','hashtags']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(SocialMediaAccounts, SocialMediaAccountsAdmin)
admin.site.register(GeneratedVideos, GeneratedVideosAdmin)
admin.site.register(OrderTypesDBNames, OrderTypesDBNamesAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(YouTubeTwoVideosOrders, YouTubeTwoVideosOrdersAdmin)
admin.site.register(UserVideoOrders, UserVideoOrdersAdmin)
admin.site.register(RedditVideoOrders, RedditVideoOrdersAdmin)
