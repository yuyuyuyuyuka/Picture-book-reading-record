from django.db import models
from accounts.models import Family

# 子どもモデル
class Child(models.Model):
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, null=False, blank=False, related_name='children')
    name = models.CharField(max_length=225)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 絵本モデル
class Book(models.Model):
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='books',null=False, blank=False)
    title = models.CharField(max_length=225)
    author = models.CharField(max_length=225)
    publisher = models.CharField (max_length=225)
    cover_image = models.ImageField(upload_to='book_covers/')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


#簡単記録モデル
class ReadingComment(models.Model):
    # 16項目ほど選択を作りたい
    comment = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.comment


# 読み聞かせ記録モデル
class ReadingRecord(models.Model):
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='reading_records', null=False, blank=False)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='reading_records')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_records')
    reading_comments =models.ManyToManyField(ReadingComment, blank=True)
    date = models.DateField()
    read_count = models.PositiveIntegerField()
    
    BOOK_STATUS_CHOICES = (
        (0, '持ってる'),
        (1, '借りた')
    )
    
    book_status = models.IntegerField(choices=BOOK_STATUS_CHOICES, default=0, null=False)  #0:絵本持っている1:図書館等で借りた
    photo = models.ImageField(upload_to='reading_photos/', null=True, blank=True)  #子どもの写真
    video = models.FileField(upload_to='reading_videos/', null=True, blank=True)  #子どもの動画
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.child.name} - {self.read_count}回読まれた"
    

