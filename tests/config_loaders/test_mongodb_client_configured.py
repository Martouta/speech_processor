from app.config_loaders.mongodb_client_configured import mongodb_client_configured
import pymongo


class TestMongoDBClientConfigured:
    def test_mongodb_client_configured(self):
        config = mongodb_client_configured()
        assert type(config['client']) == pymongo.mongo_client.MongoClient
        assert type(config['database']) == pymongo.database.Database
        assert type(config['collection']) == pymongo.collection.Collection
