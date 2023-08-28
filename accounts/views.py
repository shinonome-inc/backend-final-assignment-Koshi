from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, RedirectView

from tweets.models import Tweet

from .forms import SignupForm
from .models import FriendShip

User = get_user_model()


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = "accounts/user_profile.html"
    model = Tweet
    context_object_name = "tweet_list"

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs["username"])
        self.user = user
        return Tweet.objects.select_related("user").filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        if FriendShip.objects.filter(following=self.user, follower=self.request.user).exists():
            context["is_follow"] = True
        else:
            context["is_follow"] = False
        context["follow_number"] = FriendShip.objects.filter(follower=self.user).count()
        context["follower_number"] = FriendShip.objects.filter(following=self.user).count()
        return context


class FollowView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("tweets:home")

    def post(self, request, *args, **kwargs):
        try:
            follower = User.objects.get(username=self.request.user)
            following = User.objects.get(username=self.kwargs["username"])
        except User.DoesNotExist:
            messages.warning(request, "そのユーザーは存在しません")
            return HttpResponseNotFound("that user doesn't exist")
        if follower == following:
            messages.warning(request, "自分自身をフォローできません")
            return HttpResponseBadRequest("you can't follow yourself")
        if FriendShip.objects.filter(following=following, follower=follower):
            messages.warning(request, "既にフォローしています")
        else:
            FriendShip.objects.create(following=following, follower=follower)
            messages.warning(request, "フォローしました")
        return super().post(request, *args, **kwargs)


class UnFollowView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("tweets:home")

    def post(self, request, *args, **kwargs):
        try:
            follower = User.objects.get(username=self.request.user)
            following = User.objects.get(username=self.kwargs["username"])
        except User.DoesNotExist:
            messages.warning(request, "そのユーザーは存在しません")
            return HttpResponseNotFound("that user doesn't exist")
        if follower == following:
            messages.warning(request, "自分自身はアンフォローできません")
            return HttpResponseBadRequest("you can't unfollow yourself")
        elif FriendShip.objects.filter(following=following, follower=follower).exists():
            unfollow = FriendShip.objects.get(following=following, follower=follower)
            unfollow.delete()
            messages.success(request, "{}のフォローを外しました", kwargs["username"])
            return super().post(request, *args, **kwargs)
        else:
            messages.warning(request, "あなたは{}をフォローしていません", kwargs["username"])
            return HttpResponseBadRequest("you don't follow that username")


class FollowingListView(LoginRequiredMixin, ListView):
    template_name = "accounts/following_list.html"
    model = FriendShip
    context_object_name = "following_list"

    def get_queryset(self):
        following_user = User.objects.get(username=self.kwargs["username"])
        self.user = following_user
        return FriendShip.objects.filter(follower=following_user).select_related("following").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return super().get_context_data(**kwargs)


class FollowerListView(LoginRequiredMixin, ListView):
    template_name = "accounts/follower_list.html"
    model = FriendShip
    context_object_name = "follower_list"

    def get_queryset(self):
        follower_user = User.objects.get(username=self.kwargs["username"])
        self.user = follower_user
        return FriendShip.objects.filter(following=follower_user).select_related("follower").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return super().get_context_data(**kwargs)
