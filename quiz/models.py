from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    time_limit = models.IntegerField(default=30)  # Time limit in seconds
    
    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.CharField(max_length=200)
    options = models.TextField()  # Store options as comma-separated values
    
    def get_options(self):
        return self.options.split(',')
    
    def __str__(self):
        return self.text

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    time_taken = models.FloatField()  # Time taken in seconds
    
    def get_feedback(self):
        # Since we're always taking 5 questions per quiz
        percentage = (self.score / 5) * 100
        if percentage >= 80:
            return "Excellent! You did really well!"
        elif percentage >= 60:
            return "Good job! You passed the quiz."
        elif percentage >= 40:
            return "Not bad, but there's room for improvement."
        else:
            return "You might want to try again after studying more."
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"