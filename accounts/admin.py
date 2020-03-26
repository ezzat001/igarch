from django.contrib import admin
from .models import *

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user','id', 'following', 'followers','unfollowed_you','mutual','time')
    fields = ('user', 'password','following', 'followers'
    ,'mutual','dont_follow_you_back','you_dont_follow_back','unfollowed_you'
    ,'followers_list','following_list'
    ,'mutual_list','dont_follow_you_back_list','you_dont_follow_back_list'
    ,'unfollowed_you_list','private_account','time')
    readonly_fields = ('id','time')

@admin.register(Stalked)
class StalkedAdmin(admin.ModelAdmin):

    list_display = ('user', 'stalked_account', 'followers','following')
    fields = ('user', 'stalked_account', 'followers','following','followers_list','following_list')
    readonly_fields = ('id',)

@admin.register(StalkedAction)
class StalkedActionAdmin(admin.ModelAdmin):

    list_display = ('user', 'stalked_account', 'action','on_user', )
    fields = ('user', 'stalked_account', 'action','on_user', 'pic','time')
    readonly_fields = ('id','time')


@admin.register(PrivateUncoveredacc)
class PrivateUncoveredAdmin(admin.ModelAdmin):
    list_display = ("user", "username","uncovered", 'time',"id")
    fields = ('user','username', 'uncovered','id', 'time')
    readonly_fields = ('id','time')

@admin.register(PrivateUncoveredPhoto)
class PrivateUncoveredPhotosAdmin(admin.ModelAdmin):
    fields = ('user','img', 'id',)
    list_display = ("user", "id",'time')

    readonly_fields = ('id','time')

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
        list_display = ('user', 'action', 'on', 'time')
        fields = ('user', 'action', 'on', 'time')
        readonly_fields = ('id','time')

@admin.register(AccountArchive)
class AccountArchiveAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'join_date')
    field = ('username', 'password', 'join_date')
    readonly_fields = ('join_date',)
