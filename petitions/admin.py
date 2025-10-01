from django.contrib import admin
from .models import MoviePetition, PetitionVote

@admin.register(MoviePetition)
class MoviePetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'votes', 'posted_by', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('votes', 'posted_by', 'created_at')

@admin.register(PetitionVote)
class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ('petition', 'user')
    list_filter = ('petition',)
    search_fields = ('user__username', 'petition__title')