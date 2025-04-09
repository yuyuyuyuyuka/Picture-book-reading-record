from django import forms
from .models import Child

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