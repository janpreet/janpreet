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
    composition = {lang: round(count / total * 100, 1) for lang, count in language_data.items()}
    return dict(sorted(composition.items(), key=lambda x: (-x[1], x[0])))

def create_language_table(lang_composition):
    table = "| Language | Percentage |\n|----------|------------|\n"
    for lang, percentage in lang_composition.items():
        table += f"| {lang} | {percentage}% |\n"
    return table

def get_blog_posts(blog_url, max_posts=5):
    feed = feedparser.parse(blog_url)
    return [{'title': e.get('title', ''), 'link': e.get('link', '')} 
            for e in feed['entries'][:max_posts]]

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
    
    print('Creating language table...')
    language_table = create_language_table(lang_composition)
    
    print('Fetching blog posts...')
    blog_posts = get_blog_posts(blog_url)
    
    print('Generating README content...')
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    readme_content = generate_readme_content(
        template_path,
        username=username,
        language_table=language_table,
        blog_posts='\n'.join([f"- [{post['title']}]({post['link']})" for post in blog_posts]),
        current_time=current_time
    )
    
    print('Writing README.md...')
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print('Finished!')

if __name__ == "__main__":
    main()