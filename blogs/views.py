from django.utils import timezone
from.forms import CommentForm
from blogs.models import Comments, Post
from django.views import generic
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from .decorators import get_query, query_debugger, query_debugger

class HomePage(generic.ListView):
    template_name = 'blogs/home.html'
    model = Post

    def get(self, request):
        context = {}
        all_posts = Post.objects.all()
        paginator = Paginator(all_posts, 2)
        page = request.GET.get('page', 1)
        context["page"] = page
        try:
            context["posts"] = paginator.page(page)
        except PageNotAnInteger:
            context["posts"] = paginator.page(1)
        except EmptyPage:
            context["posts"] = paginator.page(paginator.num_pages)
        return render(request, 'blogs/home.html', context)


class DetailPage(generic.DetailView, generic.CreateView):
    template_name = 'blogs/read.html'
    model = Post
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        del context['object']
        context['reply_to_comments'] = self.reply_to_comments
        context['reply_to_reply'] = self.reply_to_reply
        context.update(self.context_data)
        return context

    @get_query
    # @query_debugger
    def get(self, request, *args, **kwargs):
        context_data = {}
        all_comments = self.comments
        paginator = Paginator(all_comments, 3)
        page = request.GET.get('page', 1)
        context_data["page"] = page
        try:
            context_data["comments"] = paginator.page(page)
        except PageNotAnInteger:
            context_data["comments"] = paginator.page(1)
        except EmptyPage:
            context_data["comments"] = paginator.page(paginator.num_pages)
        self.context_data = context_data
        return super().get(request, *args, **kwargs)

    def post(self, request, pk):
        form = self.form_class(request.POST)
        post = Post.objects.get(pk=pk)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.sent_at = timezone.now()
            comment.save()
            return redirect('home')
        else:
            form = self.form_class()
        return render(request, 'blogs/read.html', locals())

        