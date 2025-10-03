from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, MovieRequest, Petition, PetitionVote
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def top_comments(request):
    # order by most recent date
    top_reviews = Review.objects.select_related("user", "movie").order_by("-date")[:10]

    context = {
        "top_reviews": top_reviews
    }
    return render(request, "movies/top_comments.html", context)

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie =  Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    top_reviews = Review.objects.select_related("user", "movie").order_by("-date")[:5]


    template_data = {}
    template_data['title'] =  movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
                  {'template_data': template_data,})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)



# Create your views here.

@login_required
def movie_requests(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        if name and description:
            MovieRequest.objects.create(
                name=name,
                description=description,
                user=request.user
            )
        return redirect('movies.requests')

    user_requests = MovieRequest.objects.filter(user=request.user).order_by('-created_at')
    template_data = {
        'title': 'My Movie Requests',
        'requests': user_requests,
    }
    return render(request, 'movies/requests.html', {'template_data': template_data})


@login_required
def delete_movie_request(request, request_id):
    req = get_object_or_404(MovieRequest, id=request_id, user=request.user)
    req.delete()
    return redirect('movies.requests')

# Petition views
@login_required
def petitions(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name', '').strip()
        description = request.POST.get('description', '').strip()
        if movie_name and description:
            Petition.objects.create(
                movie_name=movie_name,
                description=description,
                created_by=request.user
            )
            messages.success(request, 'Petition created successfully!')
        else:
            messages.error(request, 'Please fill in all fields.')
        return redirect('movies.petitions')

    # Get all petitions with vote counts
    petitions_list = Petition.objects.all().order_by('-created_at')
    for petition in petitions_list:
        petition.vote_count = petition.get_vote_count()
        petition.user_has_voted = request.user in petition.voters.all()

    template_data = {
        'title': 'Movie Petitions',
        'petitions': petitions_list,
    }
    return render(request, 'movies/petitions.html', {'template_data': template_data})

@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    
    # Check if user already voted
    if request.user in petition.voters.all():
        messages.warning(request, 'You have already voted on this petition.')
    else:
        PetitionVote.objects.create(petition=petition, user=request.user)
        messages.success(request, f'You voted for "{petition.movie_name}"!')
    
    return redirect('movies.petitions')

@login_required
def delete_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id, created_by=request.user)
    petition.delete()
    messages.success(request, 'Petition deleted successfully.')
    return redirect('movies.petitions')
