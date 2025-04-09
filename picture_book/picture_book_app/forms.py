from django import forms
from .models import Child, Book

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
