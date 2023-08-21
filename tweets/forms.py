from django import forms

from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ("content",)

    # Tweetモデルのusernameに今ログインしているusernameを適用させている
    def __init__(self, username=None, *args, **kwargs):
        self.username = username
        super().__init__(*args, **kwargs)

    # ログインしているusernameをデータベースに保存する
    def save(self, commit=True):
        tweet_obj = super().save(commit=False)
        if self.username:
            tweet_obj.username = self.username
        if commit:
            tweet_obj.save()
        return tweet_obj
