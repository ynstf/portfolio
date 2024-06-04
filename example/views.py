# example/views.py
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
import json
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

def home(request):

    
    # Open the JSON file
    with open('me.json', 'r') as f:
        json_data = json.loads(f.read())

    
    username = json_data['repo']

    # Replace 'YOUR_TOKEN' with your personal access token
    token = os.getenv('GITHUB_TOKEN')

    # GitHub API endpoint for listing user repositories
    url = f'https://api.github.com/users/{username}/repos'

    # Send GET request to GitHub API with authentication
    response = requests.get(url, headers={'Authorization': f'token {token}'})


    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        repos = response.json()

        # Dictionary to store language counts
        languages = []
        
        # Count languages in each repository
        for repo in repos:
            language = repo['language']
            if language:
                if language not in languages:
                    languages.append(language)




        # Count the number of repositories
        num_repos = len(repos)
        print(f'You have {num_repos} repositories on GitHub.')
    else:
        print('Failed to retrieve repository information.')






    # GitHub API endpoint for getting user's contributions
    url_contributions = f'https://api.github.com/users/{username}/contributions'
    # Send GET request to GitHub API to get contributions
    response_contributions = requests.get(url_contributions, headers={'Authorization': f'token {token}'})
    print(response_contributions.content)
    # Check if request for contributions was successful (status code 200)
    if response_contributions.status_code == 200:
        # Parse JSON response to get contributions data
        contributions_data = response_contributions.json()
        # Extract total contributions from the response
        total_contributions = contributions_data['total']
        # Print total number of contributions
        print(f'Total number of contributions across all repositories: {total_contributions}')
    else:
        print('Failed to retrieve contributions information.')


    def get_contributions(username, token):
        # Construct the GraphQL query
        query = '''
        query {
        user(login: "%s") {
            contributionsCollection {
            contributionCalendar {
                totalContributions
            }
            }
        }
        }
        ''' % username
        
        # Send a POST request to the GraphQL API
        response = requests.post(
            'https://api.github.com/graphql',
            json={'query': query},
            headers={'Authorization': 'Bearer ' + token}
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            total_contributions = data['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']
            print(f"Total contributions for {username}: {total_contributions}")
        else:
            print("Failed to retrieve contributions.")

        return total_contributions


    





        
    context = {
        "me":json_data,
        "repos_numbers":num_repos,
        "languages":len(languages),
        "contributions":get_contributions(username, token),
    }
    return render(request, 'index.html', context)
