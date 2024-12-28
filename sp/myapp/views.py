# views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import  Topic, SubTopic, QuizResult, Profile, Question, Resource
from django.contrib.auth.forms import AuthenticationForm

import json

def home(request):
    return render(request, 'myapp/home.html')

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'myapp/signup.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'myapp/signup.html', {'error': 'Email already exists'})
        
        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            Profile.objects.create(user=user)  # Create profile for the new user
            login(request, user)
            return redirect('select_topic')
        else:
            # Handle password mismatch
            return render(request, 'myapp/signup.html', {'error': 'Passwords do not match'})
    
    return render(request, 'myapp/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        # Check if user authentication is successful
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Handle invalid login
            return render(request, 'myapp/login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'myapp/login.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile, QuizResult, Resource
import json

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    

    # Get completed topics from Profile
    completed_topics = profile.completed_topics.all()

    # Get weak topics from Profile
    weak_topics = profile.weak_topics.all()

    # Fetch progress data
    completed_results = QuizResult.objects.filter(user=request.user)
    progress_data = completed_results.values('score', 'date_taken')
    progress_dates = [entry['date_taken'].strftime('%Y-%m-%d') for entry in progress_data]
    progress_scores = [entry['score'] for entry in progress_data]

    # Fetch completion dates for notifications
    
    

    # Fetch resources
    resources = Resource.objects.filter(sub_topic__in=profile.weak_topics.all())

    context = {
        'weak_topics': weak_topics,
        'completed_topics': completed_topics,
        'progress_dates': json.dumps(progress_dates),  # Convert lists to JSON strings
        'progress_scores': json.dumps(progress_scores),  # Convert lists to JSON strings
        'notifications': notifications,
        'resources': resources,
        

    }

    return render(request, 'myapp/dashboard.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, SubTopic, Profile, QuizResult
import json

@login_required
@login_required
def select_topic(request):
    if request.method == 'POST':
        selected_topic_id = request.POST.get('topic_id')
        if selected_topic_id:
            return redirect('main_quiz', topic_id=selected_topic_id)
    
    topics = Topic.objects.all()
    
    context = {
        'topics': topics,
    }
    
    return render(request, 'myapp/select_topic.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, SubTopic, QuizResult, Profile, Question

@login_required
def main_quiz(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    subtopics = topic.subtopics.all()
    questions = Question.objects.filter(sub_topic__in=subtopics)

    if request.method == 'POST':
        correct_answers = 0
        total_questions = len(questions)
        weak_topics = []
        
        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            if selected_answer == question.correct_answer:
                correct_answers += 1
            else:
                weak_topics.append(question.sub_topic)
        
        time_taken = request.POST.get('time_taken')
        weak_topics = list(set(weak_topics))  # Remove duplicates
        
        result = QuizResult.objects.create(
            user=request.user,
            score=correct_answers,
            time_taken=time_taken,
            sub_topic=subtopics.first()  # Assuming sub_topic here is for the first subtopic
        )
        result.weak_topics.set(weak_topics)
        result.save()
        
        profile = Profile.objects.get(user=request.user)
        profile.weak_topics.add(*weak_topics)
        profile.completed_topics.add(*subtopics)
        profile.save()
        
        return redirect('result', result_id=result.id)
    
    context = {
        'topic': topic,
        'questions': questions,
    }
    return render(request, 'myapp/main_quiz.html', context)

@login_required
def reattempt_quiz(request, sub_topic_id):
    sub_topic = get_object_or_404(SubTopic, pk=sub_topic_id)
    questions = sub_topic.question_set.all()

    if request.method == 'POST':
        correct_answers = 0
        total_questions = len(questions)
        weak_topics = []

        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            if selected_answer == question.correct_answer:
                correct_answers += 1
            else:
                weak_topics.append(question.sub_topic)

        time_taken = request.POST.get('time_taken')
        weak_topics = list(set(weak_topics))  # Remove duplicates

        result = QuizResult.objects.create(
            user=request.user,
            score=correct_answers,
            time_taken=time_taken,
            sub_topic=sub_topic
        )
        result.weak_topics.set(weak_topics)
        result.save()

        profile = Profile.objects.get(user=request.user)

        if correct_answers == total_questions:
            # Remove sub_topic from weak_topics and add to completed_topics with date
            profile.weak_topics.remove(sub_topic)
          
        else:
            # Add sub_topic to weak_topics
            profile.weak_topics.add(sub_topic)

        profile.save()

        return redirect('result', result_id=result.id)

    context = {
        'sub_topic': sub_topic,
        'questions': questions,
    }
    return render(request, 'myapp/reattempt_quiz.html', context)


@login_required
@login_required
def result(request, result_id):
    result = get_object_or_404(QuizResult, pk=result_id)
    weak_topics = result.weak_topics.all()
    username = request.user.username

    context = {
        'result': result,
        'weak_topics': weak_topics,
        'username': username,
    }

    return render(request, 'myapp/result.html', context)


@login_required
def resources(request):
    profile = Profile.objects.get(user=request.user)
    weak_topics = profile.weak_topics.all()
    resources = Resource.objects.filter(topic__in=weak_topics)
    return render(request, 'myapp/resources.html', {'resources': resources})

@login_required
def track_progress(request):
    profile = Profile.objects.get(user=request.user)
    progress_data = QuizResult.objects.filter(user=request.user).values('score', 'time_taken', 'date_taken')
    progress_dates = [entry['date_taken'].strftime('%Y-%m-%d') for entry in progress_data]
    progress_scores = [entry['score'] for entry in progress_data]
    return JsonResponse({'dates': progress_dates, 'scores': progress_scores})

def notifications(request):
    # Placeholder notifications for demonstration
    notifications = ["Complete your Algebra quiz!", "New resources added for Trigonometry."]
    return JsonResponse({'notifications': notifications})

def logout(request):
    logout(request)
    return redirect('home')
