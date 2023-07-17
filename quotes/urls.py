from django.urls import path 
from . import views

app_name = 'quotes'

urlpatterns = [
    #Home page
    path('', views.index, name='index'),
    #Page that shows all topics
    path('topics/', views.topics, name='topics'),
    #Detail page for a single topic
    path('topics/<int:topic_id>', views.topic, name='topic'),
    #Page for adding a new topic
    path('new_topic/', views.new_topic, name='new_topic'),
    #Page for adding a new quote
    path('new_quote/<int:topic_id>', views.new_quote, name='new_quote'),
    #Page for editing a quote
    path('edit_quote/<int:quote_id>', views.edit_quote, name='edit_quote'),
    #page for editing a topic
    path('edit_topic/<int:topic_id>', views.edit_topic, name='edit_topic'),
    #Page for deleting a topic
    path('delete_topic/<int:topic_id>', views.delete_topic, name='delete_topic'),
    #Page for deleting an entry
    path('delete_quote/<int:quote_id>', views.delete_quote, name='delete_quote'),
]