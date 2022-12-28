#!/usr/bin/env python3
from pathlib import Path
from os import environ
from time import time
from datetime import date
from flask import Flask, request

app = Flask(__name__)

class RequestCounter():
    def __init__(self):
        self.counter={}
        self.lastClear=time()

    def checkClear(self):
        if time() > self.lastClear + 6969:
            self.counter={}

    # to those fans who all open my post in the same office at once: I'm sorry
    def isSpamming(self, ip):
        self.checkClear()
        self.counter[ip] = self.counter[ip]+1 if ip in self.counter else 1
        return self.counter[ip] > 10

content_dir=environ['CONTENT_DIR']
comment_dir=environ['COMMENT_DIR']

successful_response="""
<p>
    Thanks for your comment ✨
</p>
<p>
    This won't be added immediately, but be reviewed first, so it could take a while
</p>
    Feel free to bug me via IM/email if you think I forgot about it
</p>
"""
ratelimit_response="""
<p>
    I have reason to believe you're spamming me, so please chill.
</p>
"""
invalid_slug_response="""
<p>
    You sneaky boi. Yes, that'd enable you to write to any file on my filesystem, but I checked against valid article slugs
</p>
"""
wrong_nonce_response="""
<p>
    Please use a valid comment nonce. For now I don't have proper PoW checks so 420 and 69 are hardcoded to work
</p>
"""
request_counter = RequestCounter()

@app.post("/newcomment")
def newcomment():
    slug=request.form['slug']
    comment=request.form['comment']
    email=request.form['email']
    name=request.form['name']
    nonce=request.form['nonce']

    valid_slugs = [p.stem for p in Path(content_dir).glob('*.html')]
    if slug not in valid_slugs:
        app.logger.warning(f'invalid slug used: {slug}')
        return invalid_slug_response, 400
    if nonce not in ['420', '69']:
        app.logger.info(f'invalid nonce used: {nonce}')
        return wrong_nonce_response, 400
    if request_counter.isSpamming(request.remote_addr):
        app.logger.warning(f'possible spammer')
        return ratelimit_response, 429

    with open(comment_dir+slug+'.md', 'a', encoding="utf8") as file:
        text = f'''
<div class="comment-entry">
<header>
<div class="name">{name} ({email})</div> <div class="date">{date.today().isoformat()}</div>
</header>
<div class="comment-body">
{comment}
</div>
</div>

        '''
        print(text, file=file)

    app.logger.info(f'wrote a comment on post {slug}')
    return successful_response

