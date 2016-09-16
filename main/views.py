from django.shortcuts import render, redirect
from main.models import Candidate
from main.forms import SubmissionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


@login_required(login_url='/login')
def index(request):
    form = SubmissionForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            spl = Candidate.objects.get(name=form.cleaned_data["spl_candidates"])
            spl.votes += 1
            spl.save()
            aspl = Candidate.objects.get(name=form.cleaned_data["aspl_candidates"])
            aspl.votes += 1
            aspl.save()
            return redirect('aftermath')
    return render(request, 'index.html', {'form':form})

@login_required(login_url='/login')
def aftermath(request):
    return render(request, 'aftermath.html')

@login_required(login_url='/login')
def leaderboard(request):
    spl_candidates = Candidate.objects.filter(category="SPL").order_by('-votes')
    aspl_candidates = Candidate.objects.filter(category="ASPL").order_by('-votes')
    return render(request, 'leaderboard.html', {
        'spl_candidates':spl_candidates,
        'aspl_candidates':aspl_candidates,
    })

def login_user(request):
    if 'username' not in request.POST:
        return render(request, 'login.html', {})

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'login.html')

@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('index')