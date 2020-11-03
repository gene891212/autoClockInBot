from django.db import models
# Create your models here.
class UserInformation(models.Model):
    user_name = models.CharField(max_length=200,blank=True,help_text='It will auto fill from linbot.')
    user_id = models.CharField(max_length=200,help_text='It will auto fill from linbot.')
    email_account = models.EmailField(blank=True)
    email_password = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.user_name