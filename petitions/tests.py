from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import MoviePetition, PetitionVote
from .forms import MoviePetitionForm

class MoviePetitionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_create_petition(self):
        petition = MoviePetition.objects.create(
            title='Test Movie',
            release_year=2023,
            description='A great test movie',
            posted_by=self.user
        )
        self.assertEqual(petition.title, 'Test Movie')
        self.assertEqual(petition.votes, 0)
        self.assertEqual(petition.posted_by, self.user)

    def test_petition_vote(self):
        petition = MoviePetition.objects.create(
            title='Test Movie',
            posted_by=self.user
        )
        
        # Create a vote
        vote = PetitionVote.objects.create(
            petition=petition,
            user=self.user
        )
        
        self.assertEqual(vote.petition, petition)
        self.assertEqual(vote.user, self.user)

class MoviePetitionFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'title': 'Test Movie',
            'release_year': 2023,
            'description': 'A great movie'
        }
        form = MoviePetitionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_title(self):
        form_data = {
            'title': 'A',  # Too short
            'release_year': 2023,
            'description': 'A great movie'
        }
        form = MoviePetitionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_release_year(self):
        form_data = {
            'title': 'Test Movie',
            'release_year': 1800,  # Too old
            'description': 'A great movie'
        }
        form = MoviePetitionForm(data=form_data)
        self.assertFalse(form.is_valid())

class MoviePetitionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_petition_list_view(self):
        response = self.client.get(reverse('petitions:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Movie Petitions')

    def test_create_petition_requires_login(self):
        response = self.client.get(reverse('petitions:create_petition'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_create_petition_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('petitions:create_petition'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Start a New Movie Petition')

    def test_vote_petition_requires_login(self):
        petition = MoviePetition.objects.create(
            title='Test Movie',
            posted_by=self.user
        )
        response = self.client.post(reverse('petitions:vote_petition', args=[petition.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_complete_petition_workflow(self):
        """Test the complete user story: create petition, vote on it, verify vote count"""
        self.client.login(username='testuser', password='testpass123')
        
        # Step 1: Create a petition
        response = self.client.post(reverse('petitions:create_petition'), {
            'title': 'The Matrix',
            'release_year': 1999,
            'description': 'A groundbreaking sci-fi movie that should be in our catalog!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Verify petition was created
        petition = MoviePetition.objects.get(title='The Matrix')
        self.assertEqual(petition.votes, 0)
        self.assertEqual(petition.posted_by, self.user)
        
        # Step 2: Vote on the petition
        response = self.client.post(reverse('petitions:vote_petition', args=[petition.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after voting
        
        # Verify vote was recorded
        petition.refresh_from_db()
        self.assertEqual(petition.votes, 1)
        self.assertTrue(PetitionVote.objects.filter(petition=petition, user=self.user).exists())
        
        # Step 3: Try to vote again (should not increase vote count)
        response = self.client.post(reverse('petitions:vote_petition', args=[petition.id]))
        self.assertEqual(response.status_code, 302)
        
        petition.refresh_from_db()
        self.assertEqual(petition.votes, 1)  # Should still be 1
        
        # Step 4: Verify petition appears in list with correct vote count
        response = self.client.get(reverse('petitions:index'))
        self.assertContains(response, 'The Matrix')
        self.assertContains(response, '1')  # Vote count
