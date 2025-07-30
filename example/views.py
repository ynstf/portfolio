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

# views.py
from django.shortcuts import render

def error(request, id):
    print(id)
    return render(request, '404.html', {}, status=404)

def error1(request, id1, id2):
    print(id)
    return render(request, '404.html', {}, status=404)


# Load environment variables from .env file
load_dotenv()


def send_email(request):
    if request.method == 'POST':
        recipient_email = request.POST.get('email')
        subject = request.POST.get('subject')
        body = request.POST.get('content')

        # Example usage:
        load_dotenv()
        sender_email = os.environ.get('EMAIL')  # Your Gmail email address
        #key = os.environ.get('KEY')  # Your Gmail email address
        sender_password = os.environ.get('sender_password')  # Your Gmail email address
        email_reciver = os.environ.get('email_reciver')  # Your Gmail email address
        #sender_password = decrypt(sender_password, int(key))


        success = send_email_to(sender_email, sender_password, recipient_email,email_reciver, subject, body)


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


def encrypt(plaintext, key):
    encrypted_text = ''
    for char in plaintext:
        if char.isalpha():
            shift = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - shift + key) % 26 + shift)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(ciphertext, key):
    return encrypt(ciphertext, -key)

