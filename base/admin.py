from django.contrib import admin
from .models import User, Room, Topic, Message, Post, Contact, FriendRequest



admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)



class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created']


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'accepted', 'created']



admin.site.register(Post, PostAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)