from django.db import models


class BaseMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Company(BaseMixin):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'companies'


class Profile(BaseMixin):
    img_url = models.URLField(max_length=400)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    tel = models.CharField(max_length=20)
    rank = models.CharField(max_length=100)
    address = models.CharField(max_length=500, null=True, default=None)
    birthday = models.DateField(null=True, default=None)
    web_site = models.URLField(max_length=400, null=True, default=None)
    memo = models.TextField(null=True, default=None)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, related_name='profiles')
    
    class Meta:
        db_table = 'profiles'
    

class Label(BaseMixin):
    name = models.CharField(max_length=50)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='labels')
    
    class Meta:
        db_table = 'labels'