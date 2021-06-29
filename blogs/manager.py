from django.db.models import manager
from django.db.models.manager import Manager

class ManagerCustom(Manager):
    
    def all(self):
        return super().get_queryset().filter(in_archive=False).order_by('-created_at')
    
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs).order_by('-created_at')
    
class CommentManager(Manager):

    def all(self):
        return super().get_queryset().order_by('-sent_at')
    
    def filter(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).order_by('-sent_at')
    