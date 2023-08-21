from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import TweetForm
from .models import Tweet


class HomeView(LoginRequiredMixin, ListView):
    template_name = "tweets/home.html"
    model = Tweet
    queryset = Tweet.objects.select_related("user")
    context_object_name = "tweet_list"


class TweetCreateView(LoginRequiredMixin, CreateView):
    form_class = TweetForm
    template_name = "tweets/tweet_create.html"
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        return super().form_valid(form)

    # Tweetモデルのuserに今ログインしているusernameを格納し、フォームに渡している。
    def get_form_kwargs(self):
        kwgs = super().get_form_kwargs()
        kwgs["user"] = self.request.user
        return kwgs


class TweetDetailView(DetailView):
    template_name = "tweets/tweet_detail.html"
    model = Tweet

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Tweet.objects.filter(id=pk)


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
