from django.contrib import admin
from .models import Profile, Topic, SubTopic, Question, QuizResult, Resource

# Register Topic model with Admin
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Register SubTopic model with Admin
class SubTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Adjust 'name' if 'name' is the actual field in your SubTopic model
    list_filter = ('name',)  # Adjust filter if necessary

admin.site.register(SubTopic, SubTopicAdmin)


# Register Question model with Admin
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'sub_topic', 'difficulty')
    search_fields = ('question_text', 'sub_topic__name')
    list_filter = ('sub_topic', 'difficulty')


# Register QuizResult model with Admin
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'sub_topic', 'score', 'date_taken', 'get_weak_topics')

    def get_weak_topics(self, obj):
        return ", ".join([sub_topic.name for sub_topic in obj.weak_topics.all()])
    get_weak_topics.short_description = 'Weak Topics'

admin.site.register(QuizResult, QuizResultAdmin)


# Register Resource model with Admin
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_topic', 'link')  # Ensure these fields exist
    list_filter = ('sub_topic',)


# Inline model for CompletedSubTopic


# Register Profile model with Admin
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_weak_topics')  # Display username and weak topics in the admin

    def display_weak_topics(self, obj):
        return ", ".join([topic.name for topic in obj.weak_topics.all()])
    display_weak_topics.short_description = 'Weak Topics'

admin.site.register(Profile, ProfileAdmin)



# Register CompletedSubTopic model with Admin


# Register Assignment model with Admin

