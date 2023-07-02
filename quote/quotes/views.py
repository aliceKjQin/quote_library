from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Quote
from .forms import TopicForm, QuoteForm

# Create your views here.
def index(request):
    """The home page for Quotes"""
    return render(request, 'quotes/index.html')

@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user)

    return render(request, 'quotes/topics.html', {
        'topics': topics
    })

@login_required
def topic(request, topic_id):
    """Show a single topic and all its quotes."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user
    check_topic_owner(topic, request.user)

    quotes = topic.quote_set.all()

    return render(request, 'quotes/topic.html', {

        'topic': topic,
        'quotes':quotes

    })

@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        #No data submitted; create a blank form
        form = TopicForm()
    else:
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('quotes:topics')
        
    #Display a blank or invalid form.
    return render(request, 'quotes/new_topic.html', {
        'form':form
    })

@login_required
def new_quote(request, topic_id):
    """Add a new quote for a particular topic"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request.user)

    if request.method != 'POST':
        form = QuoteForm()
    else:
        form = QuoteForm(data=request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.topic = topic
            new_quote.save()
            return redirect('quotes:topic', topic_id=topic_id)
        
    return render(request, 'quotes/new_quote.html', {
        'form': form,
        'topic': topic
    })

@login_required
def edit_quote(request, quote_id):
    """Edit an existing quote"""
    quote = Quote.objects.get(id=quote_id)
    topic = quote.topic
    check_topic_owner(topic, request.user)

    if request.method != 'POST':
        form = QuoteForm(instance=quote)
    else:
        form = QuoteForm(instance=quote, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:topic', topic_id=topic.id)
    
    return render(request, 'quotes/edit_quote.html', {
        'quote': quote,
        'topic': topic,
        'form': form
    })

@login_required
def delete_topic(request, topic_id):
    # Get the topic that needs to delete
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(topic, request.user)

    if request.method == 'POST':
        topic.delete()
        return redirect('quotes:topics')
    
    # Render a delete confirmation template
    return render(request, 'quotes/delete_topic.html', {
        'topic': topic,
    })


def check_topic_owner(topic, user):
    """Make sure the currently logged-in user owns the topic that's being
    requested.
    Raised Http404 if the user does not own the topic.    
    """
    if topic.owner != user:
        raise Http404
    