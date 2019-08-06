from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Show all topics"""
    all_topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':all_topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show a topic"""
    a_topic = get_object_or_404(Topic, id=topic_id)
    if not is_user_authorised_access_topic(request, a_topic):
        raise Http404
    entries = a_topic.entry_set.order_by('date_added')
    context = {'topic': a_topic, 'entries': entries}

    return render(request, 'learning_logs/topic.html', context)


@login_required
def create_topic(request):
    if request.method == 'GET':
        # topic form request
        form = TopicForm()
    elif request.method == 'POST':
        # form submitted
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    context = {'form': form}
    return render(request, 'learning_logs/create_topic.html', context)


@login_required
def create_entry(request, topic_id):
    """Add new Entry to a particular Topic"""
    entry_topic = get_object_or_404(Topic, id=topic_id)

    if not is_user_authorised_access_topic(request, entry_topic):
        raise Http404

    if request.method == 'GET':
        # entry form request
        form = EntryForm()
    elif request.method == 'POST':
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = entry_topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=entry_topic.id)
    context = {'topic': entry_topic, 'form': form}
    return render(request, 'learning_logs/create_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry_to_edit = get_object_or_404(Entry, id=entry_id)
    entry_topic = entry_to_edit.topic
    if not is_user_authorised_access_topic(request, entry_topic):
        raise Http404

    if request.method == 'GET':
        # Edit form request
        form = EntryForm(instance=entry_to_edit)
    elif request.method == 'POST':
        # Edited form submitted
        form = EntryForm(instance=entry_to_edit, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=entry_topic.id)
    context = {'entry': entry_to_edit, 'topic': entry_topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def is_user_authorised_access_topic(request, the_topic):
    """Check if currently authenticated user owns the Topic resource"""
    return the_topic.owner == request.user
