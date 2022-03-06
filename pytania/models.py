from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

QUESTION_TYPE_OF_EXAM = [
    ("matura", "matura"),
    ("zawodowy", "zawodowy"),
]

QUESTION_TYPE = [
    ("zamkniete", "zamkniete"),
    ("otwarte", "otwarte"),
]


class TextToQuestion(models.Model):
	text_to_question = models.TextField()

	def __str__(self):
		return self.text_to_question


class ExamsInfo(models.Model):
	exam_name = models.CharField(max_length=200)
	exam_year = models.DateField(null=True, blank=True)
	length_of_test = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(40), MinValueValidator(1)]
     )

	def __str__(self):
		return self.exam_name


class Question(models.Model):
	text_question= models.ForeignKey(TextToQuestion, on_delete=models.CASCADE, blank=True, null=True)
	exam_date = models.ForeignKey(ExamsInfo, on_delete=models.CASCADE, blank=True, null=True)
	question_text = models.TextField()
	group = models.CharField(max_length=100)
	question_type = models.CharField(max_length=50, choices=QUESTION_TYPE, blank=False, null=False)
	exam = models.CharField(max_length=50, choices=QUESTION_TYPE_OF_EXAM, blank=False, null=False)
	question_image = models.ImageField(upload_to='exam_image', blank=True)
	correct_answer = models.CharField(max_length=200)
	wrong_answer1 = models.CharField(max_length=200, blank=True)
	wrong_answer2 = models.CharField(max_length=200, blank=True)
	wrong_answer3 = models.CharField(max_length=200, blank=True)
	example_answer = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.question_text
