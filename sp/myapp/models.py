from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SubTopic(models.Model):
    topic = models.ForeignKey(Topic, related_name='subtopics', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    CORRECT_ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]
    
    question_text = models.CharField(max_length=200)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=CORRECT_ANSWER_CHOICES)
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES)
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    score = models.IntegerField()
    time_taken = models.FloatField()
    date_taken = models.DateTimeField(auto_now_add=True)
    weak_topics = models.ManyToManyField(SubTopic, related_name='weak_topics')

    def __str__(self):
        return f'{self.user.username} - {self.sub_topic.name} - {self.score}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weak_topics = models.ManyToManyField(SubTopic, related_name='weak_profiles', blank=True)
    completed_topics = models.ManyToManyField(SubTopic, related_name='completed_profiles', blank=True)


    def __str__(self):
        return self.user.username  # Display the username as the profile name


class Resource(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
