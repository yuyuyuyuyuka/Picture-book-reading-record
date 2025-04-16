from django.core.exceptions import ValidationError
import re

class RequireAlnumOnlyValidator:
    def validate(self, password, user=None):
        if not re.fullmatch(r'[a-zA-Z0-9]+', password):
            raise ValidationError('使える文字は半角英数になります')

    def get_help_text(self):
        return '使える文字は半角英数になります'

class RequireMixedCaseAndDigitValidator:
    def validate(self, password, user=None):
        if not (re.search(r'[A-Z]', password) and
                re.search(r'[a-z]', password) and
                re.search(r'[0-9]', password)):
            raise ValidationError('英大文字・小文字・数字を必ず含んでください')

    def get_help_text(self):
        return '英大文字・小文字・数字を必ず含んでください'