import redis
class RedisOperator:
    def __init__(self,host,port,db):
        self.host=host
        self.port=port
        self.db=db
        self.redisPool=redis.ConnectionPool(host=self.host,port=self.port,db=self.db)


    def createRedis(self):
        resultReids=redis.Redis(connection_pool=self.redisPool)
        self.resultReids=resultReids

    
