from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from encrypted_model_fields.fields import EncryptedCharField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    openai_api_key = EncryptedCharField(max_length=100)


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=User)

# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return "user_{0}/chat_documents/{1}".format(instance.user.id, filename)


# class Chat(models.Model):
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
#     title = models.CharField(max_length=60)
#     document = models.FileField(upload_to=user_directory_path)
#     agent = models.CharField(max_length=60)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title


# class ChatMessage(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.message
