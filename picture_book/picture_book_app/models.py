from django.db import models

# 子どもモデル
class Child(models.Model):
    family = models.ForeignKey('accounts.Family', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=225)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name