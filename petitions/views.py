from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from django.http import JsonResponse
from .models import MoviePetition, PetitionVote
from .forms import MoviePetitionForm

# View to list all petitions
def petition_list(request):
    petitions = MoviePetition.objects.all().order_by('-votes', '-created_at')
    
    # Check which petitions the user has already voted on
    user_voted_petitions = set()
    if request.user.is_authenticated:
        user_voted_petitions = set(
            PetitionVote.objects.filter(user=request.user)
            .values_list('petition_id', flat=True)
        )
    
    # Add voted status to each petition
    for petition in petitions:
        petition.user_has_voted = petition.id in user_voted_petitions
    
    return render(request, 'petitions/petition_list.html', {'petitions': petitions})

# View to create a new petition
@login_required
def create_petition(request):
    if request.method == 'POST':
        form = MoviePetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.posted_by = request.user
            petition.save()
            messages.success(request, f'Your petition for "{petition.title}" has been created successfully!')
            return redirect('petitions:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MoviePetitionForm()
    return render(request, 'petitions/create_petition.html', {'form': form})

# View to handle voting on a petition
@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(MoviePetition, id=petition_id)

    # Check if the user has already voted
    has_voted = PetitionVote.objects.filter(petition=petition, user=request.user).exists()

    if not has_voted:
        # Atomically increment the vote count and create a vote record
        MoviePetition.objects.filter(id=petition_id).update(votes=F('votes') + 1)
        PetitionVote.objects.create(petition=petition, user=request.user)
        messages.success(request, f'Thank you for voting on "{petition.title}"!')
    else:
        messages.info(request, f'You have already voted on "{petition.title}".')

    # Redirect back to the list
    return redirect('petitions:index')

# Alias for index view to fix URL error
index = petition_list