from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import random
from .models import Quiz, Question, Result

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def random_quiz(request):
    # Get all quizzes that have at least 5 questions
    quizzes = Quiz.objects.annotate(question_count=Count('question')).filter(question_count__gte=5)
    
    if not quizzes.exists():
        return render(request, 'quiz/no_quiz.html')
    
    # Select a random quiz
    random_quiz = random.choice(quizzes)
    
    # Record start time and quiz ID in session
    request.session['quiz_start_time'] = timezone.now().isoformat()
    request.session['quiz_id'] = random_quiz.id
    
    return redirect('quiz_question', question_number=1)

@login_required
def start_quiz(request, quiz_id):
    # Record start time in session
    request.session['quiz_start_time'] = timezone.now().isoformat()
    request.session['quiz_id'] = quiz_id
    return redirect('quiz_question', question_number=1)

@login_required
def quiz_question(request, question_number):
    quiz_id = request.session.get('quiz_id')
    if not quiz_id:
        return redirect('quiz_list')
    
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz).order_by('id')[:5]  # Only 5 questions
    
    # Check if time is up
    start_time_str = request.session.get('quiz_start_time')
    if start_time_str:
        start_time = timezone.datetime.fromisoformat(start_time_str)
        elapsed = (timezone.now() - start_time).total_seconds()
        if elapsed > quiz.time_limit:
            return redirect('quiz_timeout')
    
    # Get current question
    if question_number > len(questions):
        return redirect('submit_quiz')
    
    current_question = questions[question_number - 1]
    
    return render(request, 'quiz/quiz_question.html', {
        'quiz': quiz,
        'question': current_question,
        'question_number': question_number,
        'total_questions': len(questions),
        'time_left': max(0, quiz.time_limit - elapsed)
    })

@login_required
def submit_quiz(request):
    quiz_id = request.session.get('quiz_id')
    if not quiz_id:
        return redirect('quiz_list')
    
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz).order_by('id')[:5]  # Only 5 questions
    
    # Calculate score
    score = 0
    for question in questions:
        user_answer = request.POST.get(f'question_{question.id}')
        if user_answer == question.correct_answer:
            score += 1
    
    # Calculate time taken
    start_time_str = request.session.get('quiz_start_time')
    if start_time_str:
        start_time = timezone.datetime.fromisoformat(start_time_str)
        time_taken = (timezone.now() - start_time).total_seconds()
    else:
        time_taken = 0
    
    # Save result
    Result.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        time_taken=time_taken
    )
    
    # Clear session
    if 'quiz_start_time' in request.session:
        del request.session['quiz_start_time']
    if 'quiz_id' in request.session:
        del request.session['quiz_id']
    
    return redirect('quiz_result', quiz_id=quiz_id)

@login_required
def quiz_timeout(request):
    # Clear session
    if 'quiz_start_time' in request.session:
        del request.session['quiz_start_time']
    if 'quiz_id' in request.session:
        del request.session['quiz_id']
    
    return render(request, 'quiz/quiz_timeout.html')

@login_required
def quiz_result(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    # Get the most recent result for this user and quiz
    result = Result.objects.filter(user=request.user, quiz=quiz).order_by('-id').first()
    
    # If no result exists, redirect to quiz list
    if not result:
        return redirect('quiz_list')
    
    return render(request, 'quiz/quiz_result.html', {
        'quiz': quiz,
        'result': result
    })