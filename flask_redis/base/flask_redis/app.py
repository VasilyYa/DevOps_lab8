import redis
from flask import Flask, make_response
import socket
import os

DB_HOST = os.getenv('REDIS_HOST', 'redis')
MY_ENV = os.getenv('ENV', 'unknown')

app = Flask(__name__)
cache = redis.Redis(host=DB_HOST, port=6379)

def get_hit_count() -> int:
    return int(cache.get('hits') or 0)
    
def incr_hit_count() -> int:
    return cache.incr('hits')

@app.route('/metrics')
def metrics():
    metrics = f'''
    # HELP view_count Flask-Redis-App visit counter
    # TYPE view_count counter
    view_count{{service="Flask-Redis-App"}} {get_hit_count()}
    ''' # sic double quotes in label
    response = make_response(metrics, 200)
    response.mimetype = "text/plain"
    return response
    
@app.route('/')
def hello():
    incr_hit_count()
    count = get_hit_count()
    return 'Hello World! I have been seen {} times. My name is: {} My env: {}\n'.format(count, socket.gethostname(), MY_ENV)

