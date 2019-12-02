import redis


class myRedis:

    def __init__(self):
        self.conn = redis.StrictRedis(host='10.144.5.128', port=6379, decode_responses=True)


