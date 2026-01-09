import redis
from rq import Worker, Queue

if __name__ == "__main__":
    redis_conn = redis.Redis(host="redis", port=6379)
    q = Queue("default", connection=redis_conn)
    worker = Worker([q], connection=redis_conn)
    worker.work()
