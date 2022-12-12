import json
import requests
import feedparser
import os
from collections import Counter
import write2list

# Language Composition

print('Collecting Language Data...')
username='janpreet'
response = requests.get("https://api.github.com/users/"+username+"/repos")
userData = json.loads(response.text)

allLanguages=[]

for obj in userData:
    if 'language' in obj:
        if obj["language"] != None:
            allLanguages.extend([obj["language"]])

langCount=Counter(allLanguages)

langComposition=[]
for key, size in sorted(langCount.items(), key=lambda x: x[1], reverse=True):
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

fixedContent=["![Build README](https://github.com/janpreet/janpreet/workflows/Build%20README/badge.svg) <br />" \
            "<h3>Hi there 👋 </h3> <br />" \
            "Thank you for visiting my GitHub. Reach out to me at [singh@janpreet.com](mailto:singh@janpreet.com), " \
            "read my [blog](https://janpreet.com) or follow [@SinghJanpreet](https://twitter.com/singhjanpreet) on Twitter. <br />" \
            "<table style='float:right' markdown='1'><tr><th>Language Composition</th><th>Blog</th></tr><tr><td style='vertical-align:top' markdown='1'> "]

separator=["</td><td style='vertical-align:top' markdown='1'>"]

endNote=["</td></tr></table>" \
            "<small><i>NOTE: Language composition is a list of most used languages in my repositories." \
            "It is not a direct indication of my skill level.</i></small>"]

readmeTuple=(fixedContent, langComposition, separator, postList, endNote)

readmeContent=write2list.create(readmeTuple)

# Create Readme.md

print('Writing Readme.md...')

readmeFile='./README.md'

if not os.path.exists(readmeFile):
    open(readmeFile, 'w').close()

with open(readmeFile, mode='wt', encoding='utf-8') as f:
    try:
        f.write('\n'.join(str(v) for v in readmeContent))  
    finally:
        f.close()    

print('Finished!')        
