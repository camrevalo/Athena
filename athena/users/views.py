from django.shortcuts import render
from users.forms import UserForm, UserProfileForm, EditProfileForm
from users.models import UserProfile
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from models import User
from sets import Set

def register(request):
    context = RequestContext(request)

    # Set boolean to false
    registered = False

    # if request is post
    if request.method == 'POST':
        # Initialize forms to collect user data
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # create user and userprofile classes to add data
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()
          
            profile = profile_form.save(commit=False)
            profile.user = user

            # retrieve profile registration information
            if 'first name' in request.FILES:
            	profile.fistName = request.FILES['first name']

            if 'last name' in request.FILES:
            	profile.lastName = request.FILES['last name']

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            if 'school' in request.FILES:
            	profile.school = request.FILES['school']

            if 'are you a teacher?' in request.FILES:
            	profile.isTeacher = request.FILES['are you a teacher?']

            profile.save()
            registered = True
            
            # logs you in if your registration details check out
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return HttpResponseRedirect('/forum/')
        else:
            print user_form.errors, profile_form.errors

    # if request is not post
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'users/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        # fetches credentials information and attempts to authenticate
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        # logs in if active user
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/forum/')
            else:
                return HttpResponse("Your Athena account is disabled.")
        else:
            # Bad login details provided
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('users/login.html', {}, context)

@login_required
def user_profile(request, user_id=0):
    try:
	    if user_id==0:
            # if own profile, brings up own profile
	        user = User.objects.get(pk=request.user.id)
	        profile = user.userprofile
	    else:
            # if another profile, brings up that user's profile
	        user = User.objects.get(pk=user_id)
	        profile = user.userprofile
    except User.DoesNotExist:
	raise Http404("Profile does not exist!")

    # sorts answers chronologically
    answer_list = user.answer_set.all()
    answered_questions = Set([])
    for answer in answer_list:
        answered_questions.add(answer.question)

    sorted_answered_questions = sorted(answered_questions, key=lambda x: x.pub_date, reverse=True)

    return render(request, 'users/profile.html', {'user': user, 'profile': profile, 'self': user_id, 'answered_questions': sorted_answered_questions})
    
@login_required
def edit_user_profile(request, user_id=0):
    # if own profile, allows edit profile option
    if user_id==0:
        user = User.objects.get(pk=request.user.id)
        profile = user.userprofile

        # brings up EditPrfileForm option and saves data
        if request.method == 'POST':
            form = EditProfileForm(data=request.POST, instance=request.user, profile=profile)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/users/profile')
        else:
            form = EditProfileForm(profile=profile)

        return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def user_logout(request):
    # logs out user
	logout(request)
	return HttpResponseRedirect('/forum/')