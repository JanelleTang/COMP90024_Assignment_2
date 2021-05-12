'''
Create Couch DB database util according to this API
https://couchdb-python.readthedocs.io/en/latest/client.html
'''
import couchdb
import logging
from backend.config.couchDBConfig import CouchDBConfig
logger = logging.getLogger("django.info")

class CouchDBDriver:
    connected = False
    def __init__(self, domain=CouchDBConfig.domain, 
                        port=CouchDBConfig.port, 
                        password=CouchDBConfig.password, 
                        username=CouchDBConfig.username):
        self.domain = domain
        self.port = port
        self.password = password
        self.username = username
        url = "http://" + self.username + ":" + self.password + "@" + self.domain + ":" + self.port
        logger.info("Connect to %s@%s:%s" % (self.username, self.domain, self.port))

        try:
            # connect to the couchdb
            self.server = couchdb.Server(url)
            self.connected = True
            logger.info("Connect succesfully")
        except Exception:
            logger.info("Connect unsuccesfully")

    def get_database(self, name):
        if not self.connected:
            return None

        if not name in self.server:
            logger.info("create database of name " + name)
            db = self.server.create(name)
            db.save(CouchDBConfig.views)
            return db
        else:
            try:
                return self.server[name]
            except Exception as e:
                logger.error(e)

# round robin load balancer technique
class CouchDBLoadBalancer:

    balance_factor = 0

    def __init__(self, CouchDBConfig=CouchDBConfig):
        self.servers = []
        for domain in CouchDBConfig.domains:
            self.servers.append(CouchDBDriver(domain=domain))

        self.cluster_size = len(self.servers)

    def next(self):
        self.balance_factor += 1
        self.balance_factor %= self.cluster_size
        return self.servers[self.balance_factor]

   
    def getById(self, database, id):
        return self.next().get_database(database).get(id=id)
    
    def findByQuery(self, database, mango_query):
        return self.next().get_database(database).find(mango_query)
    
    def iterview(self, database, name, batch, wrapper):
        return self.next().get_database(database).iterview(name, batch, wrapper)

    def compact(self, database):
        return self.next().get_database(database).compact()
    
    def getDatabase(self, database):
        return self.next().get_database(database)
couch_db = CouchDBLoadBalancer()