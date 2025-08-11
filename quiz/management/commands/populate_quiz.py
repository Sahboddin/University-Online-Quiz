from django.core.management.base import BaseCommand
from quiz.models import Quiz, Question

class Command(BaseCommand):
    help = 'Populates the database with sample quiz data'
    
    def handle(self, *args, **options):
        # Create 3 quizzes
        quizzes_data = [
            {"title": "Geography Quiz", "time_limit": 30},
            {"title": "Science Quiz", "time_limit": 30},
            {"title": "History Quiz", "time_limit": 30}
        ]
        
        # Questions for each quiz
        all_questions = [
            # Geography Quiz Questions
            [
                {
                    "text": "What is the capital of Bangladesh?",
                    "correct_answer": "Dhaka",
                    "options": "Dhaka,Noagaon,Borisal,Dili"
                },
                {
                    "text": "Which is the largest ocean?",
                    "correct_answer": "Pacific Ocean",
                    "options": "Atlantic Ocean,Indian Ocean,Arctic Ocean,Pacific Ocean"
                },
                {
                    "text": "How many continents are there?",
                    "correct_answer": "7",
                    "options": "5,6,7,8"
                },
                {
                    "text": "What is the longest river in the world?",
                    "correct_answer": "Nile",
                    "options": "Amazon,Nile,Yangtze,Mississippi"
                },
                {
                    "text": "Which country has the largest population?",
                    "correct_answer": "China",
                    "options": "India,USA,China,Indonesia"
                }
            ],
            # Science Quiz Questions
            [
                {
                    "text": "Which planet is known as the Red Planet?",
                    "correct_answer": "Mars",
                    "options": "Venus,Mars,Jupiter,Saturn"
                },
                {
                    "text": "What is the chemical symbol for gold?",
                    "correct_answer": "Au",
                    "options": "Au,Ag,Cu,Fe"
                },
                {
                    "text": "Which element has the atomic number 1?",
                    "correct_answer": "Hydrogen",
                    "options": "Helium,Lithium,Hydrogen,Oxygen"
                },
                {
                    "text": "What is the speed of light?",
                    "correct_answer": "299,792 km/s",
                    "options": "150,000 km/s,299,792 km/s,500,000 km/s,1,000,000 km/s"
                },
                {
                    "text": "What is the hardest natural substance on Earth?",
                    "correct_answer": "Diamond",
                    "options": "Gold,Iron,Diamond,Platinum"
                }
            ],
            # History Quiz Questions
            [
                {
                    "text": "Who painted the Mona Lisa?",
                    "correct_answer": "Leonardo da Vinci",
                    "options": "Vincent van Gogh,Pablo Picasso,Leonardo da Vinci,Michelangelo"
                },
                {
                    "text": "In which year did World War II end?",
                    "correct_answer": "1945",
                    "options": "1918,1939,1945,1950"
                },
                {
                    "text": "Who was the first President of the United States?",
                    "correct_answer": "George Washington",
                    "options": "Thomas Jefferson,Abraham Lincoln,George Washington,John Adams"
                },
                {
                    "text": "Which ancient civilization built the pyramids?",
                    "correct_answer": "Egyptians",
                    "options": "Greeks,Romans,Egyptians,Mayans"
                },
                {
                    "text": "Who invented the telephone?",
                    "correct_answer": "Alexander Graham Bell",
                    "options": "Thomas Edison,Nikola Tesla,Alexander Graham Bell,Albert Einstein"
                }
            ]
        ]
        
        # Create quizzes and questions
        for i, quiz_data in enumerate(quizzes_data):
            quiz = Quiz.objects.create(title=quiz_data["title"], time_limit=quiz_data["time_limit"])
            
            for q_data in all_questions[i]:
                Question.objects.create(
                    quiz=quiz,
                    text=q_data["text"],
                    correct_answer=q_data["correct_answer"],
                    options=q_data["options"]
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated sample quiz data'))