from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import TweetForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"


class TweetCreateView(LoginRequiredMixin, CreateView):
    form_class = TweetForm
    template_name = "tweets/tweet_create.html"
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        return super().form_valid(form)

    # Tweetモデルのusernameに今ログインしているusernameを格納し、フォームに渡している。
    def get_form_kwargs(self):
        kwgs = super().get_form_kwargs()
        kwgs["username"] = self.request.user
        return kwgs
