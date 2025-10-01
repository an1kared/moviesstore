from django.db import models
from django.contrib.auth.models import User # Assuming standard Django User model

class MoviePetition(models.Model):
    """Model to store movie suggestions and track votes."""
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-votes', 'title']

    def __str__(self):
        return self.title

class PetitionVote(models.Model):
    """Model to prevent a user from voting on the same petition multiple times."""
    petition = models.ForeignKey(MoviePetition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        # Ensures a user can only vote once per petition
        unique_together = ('petition', 'user')

    def __str__(self):
        return f"{self.user.username} voted on {self.petition.title}"