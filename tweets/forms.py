from django import forms

from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ("content",)

    # Tweetモデルのusernameに今ログインしているusernameを適用させている
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    # ログインしているusernameをデータベースに保存する
    def save(self, commit=True):
        tweet_obj = super().save(commit=False)
        if self.user:
            tweet_obj.user = self.user
        if commit:
            tweet_obj.save()
        return tweet_obj
