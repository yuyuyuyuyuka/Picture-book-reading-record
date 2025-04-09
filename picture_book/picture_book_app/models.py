from django.db import models

# 子どもモデル
class Child(models.Model):
    family_id = models.ForeignKey('accounts.Family', on_delete=models.CASCADE, null=False, blank=False, related_name='children')
    name = models.CharField(max_length=225)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 絵本モデル
class Book(models.Model):
    title = models.CharField(max_length=225)
    author = models.CharField(max_length=225)
    publisher = models.CharField (max_length=225)
    cover_image = models.ImageField(upload_to='book_covers/')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
