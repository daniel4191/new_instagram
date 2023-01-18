from django import forms
from .models import Post

import re


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # 전체 필드 (이름등 설정된 인스턴스들) 가져오는 명령 __all__
        # fields = '__all__'

        # 하지만 author가 지정되어있고, 그게 보통은 빈값으로 설정되어 있지 않은 상태이다.
        # 그렇기에 author도 함께 노출이 되어야 하는데, 노출이 안되는 필드가 있다면
        # Integrity Error가 생기게 된다.
        fields = ['message', 'photo', 'tag_set', 'is_public']

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            message = re.sub(r'[a-zA-Z]+', '', message)
        return message
