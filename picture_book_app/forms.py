from django import forms
from .models import Child, Book, ReadingRecord
from django.utils import timezone

# 子どもの登録画面
class ChildForm(forms.ModelForm):

    class Meta:
        model = Child
        fields = ['name', 'birthday']
        labels = {
            'name':'名前／ニックネーム',
            'birthday':'誕生日',
        }
        # 誕生日入力をカレンダー表示
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }


# 絵本新規登録画面
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'cover_image']
        labels = {
            'title': 'タイトル',
            'author': '著者名',
            'publisher': '出版社名',
            'cover_image': '絵本の写真',
        }


# 絵本の読み聞かせ記録登録画面
class ReadingRecordForm(forms.ModelForm):

    class Meta:
        model = ReadingRecord
        fields = [
            'book', 'date', 'child', 'read_count', 'book_status',
            'photo', 'video', 'reading_comments', 'review'
        ]
        labels = {
            'book': '絵本：',
            'date': '日付：',
            'child': '子ども：',
            'read_count': '読んだ回数：',
            'book_status': '所有状況：',
            'photo': '写真：',
            'video': '動画：',
            'reading_comments': '簡単記録：',
            'review': '絵本の感想や子の様子・反応記入：'
        }
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'},
            ),
            'review': forms.Textarea(attrs={'rows': 2}),
            'reading_comments': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'multiple': 'multiple',
                'aria-label': '簡単記録を選択',
                'style': 'height: 200px; font-size: 1rem; padding: 8px;',
            }),
            'book_status': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()