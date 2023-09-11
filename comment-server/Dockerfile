FROM jpcapurro/comment-server-base

# copy all the files to the container
COPY --chown=nonroot:nonroot . .
ENV CONTENT_DIR='output/'
ENV COMMENT_DIR='comments/'

EXPOSE 5000

CMD ["poetry", "run", "gunicorn", "-b" ,"0.0.0.0:5000", "app:app"]
