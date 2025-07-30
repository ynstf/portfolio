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



import requests
import json
import os
import time
from django.shortcuts import render

def home(request):
    # Open the JSON file
    with open('me.json', 'r') as f:
        json_data = json.loads(f.read())

    username = json_data['repo']
    token = os.getenv('GITHUB_TOKEN')

    def get_fast_repos_count(username, token):
        """Get repos count super fast - no contributions needed"""
        
        start_time = time.time()
        
        # Minimal GraphQL query just for repos count
        query = '''
        query {
            user(login: "%s") {
                repositories(first: 1, ownerAffiliations: OWNER) {
                    totalCount
                }
            }
        }
        ''' % username
        
        response = requests.post(
            'https://api.github.com/graphql',
            json={'query': query},
            headers={'Authorization': 'Bearer ' + token},
            timeout=5
        )
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()['data']['user']
            repos_count = data['repositories']['totalCount']
            print(f"⏱️  REPOS COUNT: {elapsed:.2f}s -> {repos_count} repositories")
            return repos_count
        else:
            print(f"⏱️  REPOS COUNT: {elapsed:.2f}s -> FAILED")
            return 0

    def get_all_time_commits(username, token):
        """Get ALL-TIME commits across all years"""
        
        start_time = time.time()
        
        query_multi_years = '''
        query {
            user(login: "%s") {
                # Current year (default)
                contributionsCollection {
                    totalCommitContributions
                }
                # Previous years explicitly
                commits2024: contributionsCollection(from: "2024-01-01T00:00:00Z", to: "2024-12-31T23:59:59Z") {
                    totalCommitContributions
                }
                commits2023: contributionsCollection(from: "2023-01-01T00:00:00Z", to: "2023-12-31T23:59:59Z") {
                    totalCommitContributions
                }
                commits2022: contributionsCollection(from: "2022-01-01T00:00:00Z", to: "2022-12-31T23:59:59Z") {
                    totalCommitContributions
                }
                commits2021: contributionsCollection(from: "2021-01-01T00:00:00Z", to: "2021-12-31T23:59:59Z") {
                    totalCommitContributions
                }
                commits2020: contributionsCollection(from: "2020-01-01T00:00:00Z", to: "2020-12-31T23:59:59Z") {
                    totalCommitContributions
                }
            }
        }
        ''' % username
        
        response = requests.post(
            'https://api.github.com/graphql',
            json={'query': query_multi_years},
            headers={'Authorization': 'Bearer ' + token},
            timeout=10
        )
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()['data']['user']
            
            # Sum all years
            total_commits = (
                data['contributionsCollection']['totalCommitContributions'] +  # 2025
                data['commits2024']['totalCommitContributions'] +              # 2024
                data['commits2023']['totalCommitContributions'] +              # 2023
                data['commits2022']['totalCommitContributions'] +              # 2022
                data['commits2021']['totalCommitContributions'] +              # 2021
                data['commits2020']['totalCommitContributions']                # 2020
            )
            
            print(f"⏱️  ALL-TIME COMMITS: {elapsed:.2f}s -> {total_commits} commits")
            return total_commits
        else:
            print(f"⏱️  ALL-TIME COMMITS: {elapsed:.2f}s -> FAILED")
            return 0

    def get_languages_count(username, token):
        """Get unique languages count - fast call"""
        
        start_time = time.time()
        
        url = f'https://api.github.com/users/{username}/repos'
        response = requests.get(url, headers={'Authorization': f'token {token}'}, timeout=5)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        if response.status_code == 200:
            repos = response.json()
            languages = set()  # Use set for faster uniqueness check
            
            # Count unique languages
            for repo in repos:
                language = repo['language']
                if language:
                    languages.add(language)
            
            languages_count = len(languages)
            print(f"⏱️  LANGUAGES COUNT: {elapsed:.2f}s -> {languages_count} languages")
            return languages_count
        else:
            print(f"⏱️  LANGUAGES COUNT: {elapsed:.2f}s -> FAILED")
            return 0

    # Get optimized stats with timing measurements
    print("🚀 Starting GitHub stats collection...")
    overall_start = time.time()
    
    repos_count = get_fast_repos_count(username, token)
    all_time_commits = get_all_time_commits(username, token)  # ALL-TIME commits (1065)
    languages_count = get_languages_count(username, token)
    
    overall_end = time.time()
    total_time = overall_end - overall_start

    # Summary timing report
    print("=" * 50)
    print("📊 TIMING SUMMARY")
    print("=" * 50)
    print(f"🏆 TOTAL TIME: {total_time:.2f} seconds")
    print(f"📦 Repositories: {repos_count}")
    print(f"💻 Languages: {languages_count}")
    print(f"📈 All-Time Commits: {all_time_commits}")
    print("=" * 50)

    context = {
        "me": json_data,
        "repos_numbers": repos_count,        # Total repositories (fast)
        "languages": languages_count,        # Total unique languages
        "total_commits": all_time_commits,   # ALL-TIME commits (1065)
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

