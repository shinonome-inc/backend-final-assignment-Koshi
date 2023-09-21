from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import TweetForm
from .models import Like, Tweet


class HomeView(LoginRequiredMixin, ListView):
    template_name = "tweets/home.html"
    model = Tweet
    queryset = Tweet.objects.select_related("user").prefetch_related("like_tweet")
    context_object_name = "tweet_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["like_list"] = Like.objects.filter(user=self.request.user).values_list("tweet__pk", flat=True)
        return context


class TweetCreateView(LoginRequiredMixin, CreateView):
    form_class = TweetForm
    template_name = "tweets/tweet_create.html"
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name = "tweets/tweet_detail.html"
    model = Tweet
    queryset = Tweet.objects.select_related("user").prefetch_related("like_tweet")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["like_list"] = Like.objects.filter(user=self.request.user).values_list("tweet__pk", flat=True)
        return context


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "tweets/tweet_delete.html"
    model = Tweet
    queryset = Tweet.objects.select_related("user")
    success_url = reverse_lazy("tweets:home")

    def get(self, request, *args, **kwargs):
        # test_funcの方が先に呼ばれるので、getメソッド内でself.objectにアクセス可能
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def test_func(self):
        self.object = self.get_object()
        return self.object.user == self.request.user


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        tweet = get_object_or_404(Tweet, pk=self.kwargs["pk"])
        Like.objects.get_or_create(user=user, tweet=tweet)
        context = {"like_count": tweet.like_tweet.count()}
        return JsonResponse(context)


class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        tweet = get_object_or_404(Tweet, pk=self.kwargs["pk"])
        Like.objects.filter(user=user, tweet=tweet).delete()
        context = {"like_count": tweet.like_tweet.count()}
        return JsonResponse(context)
