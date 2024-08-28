import json
import requests
import feedparser
import os
from collections import Counter
from datetime import datetime, timezone

def get_github_data(username, token=None):
    headers = {'Authorization': f'token {token}'} if token else {}
    all_repos = []
    page = 1
    while True:
        response = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100&page={page}", headers=headers)
        repos = json.loads(response.text)
        if not repos:
            break
        all_repos.extend(repos)
        page += 1
    return all_repos

def get_language_data(username, repos, token=None):
    headers = {'Authorization': f'token {token}'} if token else {}
    language_data = Counter()
    for repo in repos:
        response = requests.get(repo['languages_url'], headers=headers)
        repo_languages = json.loads(response.text)
        language_data.update(repo_languages)
    return language_data

def get_language_composition(language_data):
    total = sum(language_data.values())
    composition = {lang: count / total for lang, count in language_data.items()}
    return dict(sorted(composition.items(), key=lambda x: -x[1]))

def create_language_cloud(language_data):
    cloud = []
    max_count = max(language_data.values())
    for lang, count in sorted(language_data.items(), key=lambda x: -x[1]):
        size = max(1, min(int(count / max_count * 5), 5))
        cloud.append(f'<span style="font-size: {size}em; display: inline-block;">{lang}</span>')
    joined_cloud = ', '.join(cloud)
    return f'<div style="text-align: center; line-height: 1.5;">{joined_cloud}</div>'

def get_blog_posts(blog_url, max_posts=5):
    feed = feedparser.parse(blog_url)
    return [{'title': e.get('title', ''), 'link': e.get('link', '')} 
            for e in feed['entries'][:max_posts]]

def format_blog_posts(blog_posts):
    return '\n'.join([f'<li><a href="{post["link"]}">{post["title"]}</a></li>' for post in blog_posts])


def generate_readme_content(template_path, **kwargs):
    with open(template_path, 'r') as f:
        template = f.read()
    return template.format(**kwargs)

def main():
    username = 'janpreet'
    blog_url = 'https://janpreet.com/feed.xml'
    github_token = os.environ.get('GITHUB_TOKEN')
    template_path = 'readme_template.md'

    print('Collecting GitHub data...')
    repos = get_github_data(username, github_token)
    
    print('Analyzing language composition...')
    language_data = get_language_data(username, repos, github_token)
    lang_composition = get_language_composition(language_data)
    
    print('Creating language cloud...')
    language_cloud = create_language_cloud(lang_composition)
    
    print('Fetching blog posts...')
    blog_posts = get_blog_posts(blog_url)
    formatted_blog_posts = format_blog_posts(blog_posts)
    
    print('Generating README content...')
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    readme_content = generate_readme_content(
        template_path,
        username=username,
        language_cloud=language_cloud,
        blog_posts=formatted_blog_posts,
        current_time=current_time
    )
    
    print('Writing README.md...')
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print('Finished!')

if __name__ == "__main__":
    main()