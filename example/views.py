# example/views.py
from datetime import datetime

from django.http import HttpResponse
from django.contrib import messages
from .sender.send_email import send_email_to
from django.shortcuts import render, redirect
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


def send_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        content = request.POST.get('content')

        # Example usage:
        load_dotenv()
        sender_email = os.environ.get('EMAIL')  # Your Gmail email address
        sender_password = os.environ.get('PWD')  # Your Gmail password or app password
        recipient_email = email  # Recipient's email address
        body = content

        success = send_email_to(sender_email, sender_password, recipient_email, subject, body)


        if success:
            messages.success(request, 'Email sent successfully')
            return redirect('home')
        else:
            messages.error(request, 'Failed to send email')
            return redirect('home')


def home(request):

    
    # Open the JSON file
    with open('me.json', 'r') as f:
        json_data = json.loads(f.read())

    load_dotenv()
    sender_email = os.environ.get('EMAIL')  # Your Gmail email address
    sender_password = os.environ.get('PWD')  # Your Gmail password or app password
    print("EMAIL",sender_email)
    print("PWD",sender_password)

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
