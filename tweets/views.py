from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import TweetForm
from .models import Tweet


class HomeView(LoginRequiredMixin, ListView):
    template_name = "tweets/home.html"
    model = Tweet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ツイートを投稿日時の降順に並び替える
        context["tweet_list"] = Tweet.objects.order_by("-create_date")
        return context


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
