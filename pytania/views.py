from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from pytania.serializers import QuestionSerializer, GroupSerializer

from .models import Question, ExamsInfo
from .forms import GeneratedTest

import random

# Create your views here.

def index(request):
	matura_groups = Question.objects.values('group').filter(exam='matura').distinct().order_by('group')
	context = {
		'matura_groups': matura_groups,
	}
	return render(request, 'pytania/index.html', context)

def contact(request):
	return render(request, 'pytania/contact.html')

def index_zawodowy(request):
	zawodowy_groups = Question.objects.values('group').filter(exam='zawodowy').distinct().order_by('group')
	context = {
		'zawodowy_groups': zawodowy_groups,
	}
	return render(request, 'pytania/index_zawodowy.html', context)

def question_options(request, group_name):
	context = {
		'group_name': group_name,
	}
	return render(request, 'pytania/opcje_pytan.html', context)

def question_display(request, group_name):
	question = Question.objects.filter(group=group_name)
	random_question = random.choice(question)
	correct_answer = random_question.correct_answer
	answers = [random_question.wrong_answer1, random_question.wrong_answer2, random_question.wrong_answer3, correct_answer]
	random.shuffle(answers)
	context = {
		'random_question': random_question,
		'answers': answers,
		'correct_answer': correct_answer,
		'group_name': group_name,
	}
	return render(request, 'pytania/pytanie.html', context)

def next_question_display(request, random_question_id):
	question = get_object_or_404(Question, pk=random_question_id)
	group_name = question.group
	return HttpResponseRedirect(reverse('pytania:question_display', args=(group_name,)))

def generated_test(request, group_name, test_type, number_of_questions):
	if test_type == 'random':
		if number_of_questions > 40:
			number_of_questions = 40
		length_of_test = number_of_questions
		question = list(Question.objects.filter(group=group_name))
	else:
		try:
			test_type_name = ExamsInfo.objects.filter(exam_name=test_type)
			test_type_id = test_type_name[0].id
			question = list(Question.objects.filter(group=group_name, exam_date = test_type_id))
			length_of_test = test_type_name[0].length_of_test
		except:
			length_of_test = 10

	message = ''
	if len(question) < length_of_test:
		length_of_test = len(question)
		if test_type == 'random':
			message = 'Przepraszamy, ale możemy utworzyć test tylko z ' + str(length_of_test) + ' pytań.'

	questions = random.sample(question, length_of_test)
	questions = question_type_sort(questions)

	context = {
		'questions': questions,
		'group_name': group_name,
		'message': message,
	}
	return render(request, 'pytania/generated_test.html', context)

def test_selecting(request, group_name):
	all_questions = Question.objects.select_related('exam_date').filter(group=group_name).order_by('exam_date')
	all_exams = []
	for question in all_questions:
		if question.exam_date in all_exams:
			continue
		all_exams.append(question.exam_date)
	context = {
		'group_name': group_name,
		'all_exams': all_exams,
	}
	return render(request, 'pytania/select_test.html', context)

def random_test_number_selecting(request, group_name):
	context = {
		'group_name': group_name,
	}
	return render(request, 'pytania/select_random_test.html', context)


# API

class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    


# functions

def question_type_sort(questions):
	question_open = []
	question_close = []
	for q in range(len(questions)):
		if questions[q].question_type == 'zamkniete':
			question_close.append(questions[q])
		else:
			question_open.append(questions[q])
	questions = []
	for q in question_close:
		questions.append(q)
	for q in question_open:
		questions.append(q)
	return questions