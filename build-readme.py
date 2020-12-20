import json
import requests
import feedparser
import os
from collections import Counter

# Language Composition

print('Collecting Language Data...')
username='janpreet'
response = requests.get("https://api.github.com/users/"+username+"/repos")
userData = json.loads(response.text)

allLanguages=[]

for obj in userData:
    if 'language' in obj or len(obj['language']) != 0:
        if obj["language"] != None:
            allLanguages.extend([obj["language"]])

langCount=Counter(allLanguages)

langComposition=[]
for key, size in sorted(langCount.items()):
    langComposition.append('{}: {:0.2f}'.format('- '+key, ((size/len(allLanguages))*100))+'% <br />')

# Blog Feed

print('Collecting Blog Feed...')
blogUrl='https://janpreet.com/feed.xml'

f = feedparser.parse(blogUrl)

postList=[]
for e in f['entries']:
    postList.append('{}{}{}'.format('- <a href="'+e.get('link', '')+'" target="_blank">', e.get('title', ''),'</a><br />'))    

# Readme Content

print('Processing Readme Data...')

readmeContent=[]
readmeContent.insert(0, "![Build README](https://github.com/janpreet/janpreet/workflows/Build%20README/badge.svg) <br />")
readmeContent.insert(1, "### Hi there 👋  <br />")
readmeContent.insert(2, "Thank you for visiting my GitHub. Reach out to me at [singh@janpreet.com](mailto:singh@janpreet.com), read my [blog](https://janpreet.com) or follow [@SinghJanpreet](https://twitter.com/singhjanpreet) on Twitter. <br />")
readmeContent.insert(3, "<table style='float:right' markdown='1'><tr><th>Language Composition</th><th>Blog</th></tr><tr><td style='vertical-align:top'>")
readmeContent.extend(langComposition)
readmeContent.insert(len(readmeContent),"</td><td style='vertical-align:top'>")
readmeContent.extend(postList)
readmeContent.insert(len(readmeContent),"</td></tr></table>")
readmeContent.insert(len(readmeContent), "<small><i>NOTE: Language composition is a list of most used languages in my repositories. It is not a direct indication of my skill level.</i></small>")

# Create Readme.md

print('Writing Readme.md...')

readmeFile='./README.md'

if not os.path.exists(readmeFile):
    open(readmeFile, 'w').close()

with open(readmeFile, mode='wt', encoding='utf-8') as f:
    try:
        f.write('\n'.join(readmeContent))  
    finally:
        f.close()    

print('Finished!')        