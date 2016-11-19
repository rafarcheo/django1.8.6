from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

from django.shortcuts import render, get_object_or_404

from .models import Post
from .forms import EmailPostForm


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            clear_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) zachecam do przeczytania "{}"'.format(clear_data['name'],
                                                                     clear_data['email'],
                                                                     post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez {}: {}'.format(post.title,
                                                                                                    post_url,
                                                                                                    clear_data['name'],
                                                                                                    clear_data['comments'])
            send_mail(subject, message, 'admin@myblog.com', [clear_data['to']])
            sent = True
    else:
        form = EmailPostForm()
        sent = False
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 1)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.post(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
