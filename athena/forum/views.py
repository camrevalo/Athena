from django.shortcuts import render, get_object_or_404
from forum.models import Question, Answer
from groups.models import Group
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from json import dumps, loads

def index(request):
    #get all questions that don't belong to a group
    latest_question_list = Question.objects.filter(group__isnull=True).order_by('-pub_date')
    my_groups = Group.objects.all()
    context = {
    	'latest_question_list': latest_question_list, 
        'my_groups' : my_groups, 
        'subject_choices' : [subject[0] for subject in Question.SUBJECT_CHOICES], 
        'selected' : "All"
	}
    return render(request, 'forum/index.html', context)

def filter_index(request):
    subject_name = request.POST.get('subject')
    if subject_name == "All": return HttpResponseRedirect(reverse('forum:index'))
    #take subject filter from POSTS and return all questions that correspond to subject
    latest_question_list = Question.objects.filter(group__isnull=True).filter(subject=subject_name).order_by('-pub_date')
    my_groups = Group.objects.all()
    context = {
    	'latest_question_list': latest_question_list, 
	'my_groups' : my_groups,
	'subject_choices' : [subject[0] for subject in Question.SUBJECT_CHOICES], 
    'selected': subject_name
	}
    return render(request, 'forum/index.html', context)

def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question no exist :(")
	return render(request, 'forum/detail.html', {'question':question})

#deprecated, here for testing
def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(respone % question_id)

#all csrf_exempt tags used for functions called by client side AJAX
@csrf_exempt
def upvote(request, question_id = 0):
    #take voter, answer, and call vote method in model
    if request.method == 'POST':
        answer_id = request.POST.get('a_id')
        voter_id = request.POST.get('v_id')
        answer=Answer.objects.get(pk=answer_id)
        response_data = {}
        color_arrow = answer.upvote(voter_id)
        response_data['answerpk'] = answer.pk
        response_data['upvotes'] = answer.upvotes
        response_data['arrow_color'] = "gray-glyph"
        if color_arrow:
            response_data['arrow_color'] = "voted"

        return HttpResponse(
            dumps(response_data),
            content_type = "application/json"
        )

@csrf_exempt
def downvote(request, question_id = 0):
    if request.method == 'POST':
        answer_id = request.POST.get('a_id')
        voter_id = request.POST.get('v_id')
        answer=Answer.objects.get(pk=answer_id)
        response_data = {}
        color_arrow = answer.downvote(voter_id)
        response_data['answerpk'] = answer.pk
        response_data['upvotes'] = answer.upvotes
        response_data['arrow_color'] = "gray-glyph"
        if color_arrow:
            response_data['arrow_color'] = "voted"

        return HttpResponse(
            dumps(response_data),
            content_type = "application/json"
        )

@csrf_exempt
def answer(request, question_id = 0):
    if request.method == 'POST':
        #create Answer objects given parameters in POST
        answer_text = request.POST.get('answer_text')
        answer_text = answer_text.replace("\n", "<br/>")
        question_id = request.POST.get('q_id')
        original_question=Question.objects.get(pk=question_id)
        response_data = {}
        answer=Answer(
           question=original_question, 
           answer_text=answer_text,
           user=request.user
        )
        answer.save()
        response_data['answer_id'] = answer.pk
        response_data['votes'] = answer.upvotes
        response_data['answer_text'] = answer.answer_text
        response_data['answer_username'] = answer.user.username
        response_data['answer_user_id'] = answer.user.id
        response_data['is_teacher'] = "Student"
        response_data['name_style'] = ""
        if answer.user.userprofile.isTeacher:
            response_data['is_teacher'] = "Teacher"
            response_data['name_style'] = "color: #FF6600"

        return HttpResponse(
            dumps(response_data),
            content_type = "application/json"
        )

@login_required
def add_question(request):
    group_id = request.POST.get('group_id', False);
    #attempt to create question using parameters from POST
    try:
        q = Question(
            question_text=request.POST['question'], 
			body = request.POST['body'],
			pub_date=timezone.now(),
			user=request.user,
			subject=request.POST['subject']
            )
        if group_id:
            q.group = Group.objects.get(pk=group_id)
    except(KeyError, Question.DoesNotExist):
        return render(request, 'forum/index', {'error_message': "Question must not be empty!"})
    else:
	#allow for insertion of HTML in questions
        q.body = q.body.replace("\n", "<br/>")
        q.body = q.body.replace(" ", "&nbsp;")
        q.save()
        if group_id:
            return HttpResponseRedirect(reverse('groups:detail', args=(group_id)))
        return HttpResponseRedirect(reverse('forum:index'))
