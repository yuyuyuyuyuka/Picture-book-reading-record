from django.core.exceptions import ValidationError
import re

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.search('[0-9]', password):
            raise ValidationError('パスワードには数字：0～9を必ず含めてください')
        if not re.search('[a-z]', password):
            raise ValidationError('パスワードには英小文字：a～zを必ず含めてください')
        if not re.search('[A-Z]', password):
            raise ValidationError('パスワードには英大文字：A～Zを必ず含めてください')
        if not re.match(r'^[a-zA-Z0-9]+$', password):
            raise ValidationError('パスワードに使える文字は半角英数になります')
        return password
    
    def get_help_text(self):
        return (
            '使える文字は半角英数になります。\n' #改行コードを入れた状態で値を返す
            '英大文字・小文字・数字を必ず含んでください。'
        )