from django.shortcuts import render
from .forms import TweetForm, UserRegistrationForm
from .models import Tweet
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})


@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')

    else:
        form = TweetForm()

    return render(request, 'tweet_form.html', {'form': form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')

    else:
        form = TweetForm(instance=tweet)

    return render(request, 'tweet_form.html', {'form': form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_deletion.html', {'tweet': tweet})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.set_password(form.cleaned_data['password1'])
            # user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def search(request):

    query = request.GET.get('query', '').strip()

    tweets = Tweet.objects.filter(
        Q(text__icontains=query) | Q(user__username__icontains=query)
    ) if query else []

    users = User.objects.filter(username__icontains=query) if query else []

    return render(request, 'search_result.html', {'tweets': tweets, 'users': users, 'query': query})
