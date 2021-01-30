from django import forms

class NewPlaylistForm(forms.Form):
    movie_name = forms.CharField()
    listening_history = forms.ChoiceField(help_text="Select a period of your Spotify listening history for consideration.", choices=[(1, "Last 4 Weeks"), (2,"Last 6 Months"), (3,"All Time"), (4,"Don't Use My Listening History")])
