# blog
okay I'm officially that kind of person

## Development

### Blog content
If power is plentiful: `make devserver`

If every joule has to be accounted for:
- `python -m http.server 8000`
- `make html` to rebuild when wanted

### Comment server

    cd comment-server
    poetry install
    CONTENT_DIR=../output/ COMMENT_DIR=../comments/ poetry run gunicorn -b 0.0.0.0:5000 app:app


# """"infrastructure""""

## html comments form
always submits to `/newcomment`, with the article slug in its url-encoded payload (via an `<input type="hidden" />`)

## comments """server"""
dockerized flask server, running with gunicorn on my 4-year-uptime vps, port 5000

build images

    cd comment-server
    docker build -t jpcapurro/comment-server-base -f base.Dockerfile .
    docker build -t jpcapurro/comment-server .

push image:
```
docker save comment-server:latest |xz|pv | ssh selfhost docker load
```

run it:
```
docker run -v $HOME/comments:/home/app/comments -v /var/www/blog.capu.tech:/home/app/output -p 5000:5000 -d --restart always comment-server:latest 
```

writes comments to a directory on the host, one file per valid article slug.

What I do is pull the files with a good ol' `rsync -av selfhost:comments .`

And then `git add -p comments` to review them before rebuilding

## web server
good ol' nginx running on my 4-year-uptime vps.

serves static files for the blog itself, which are updated with `make rsync_upload`

requests for `/newcomment` are reverse-proxied to port 5000
