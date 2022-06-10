import app
import pymongo
import pytest


class TestMongoDBClientConfigured:
    def test_mongodb_client_configured(self):
        config = app.mongodb_client_configured()
        assert type(config['client']) == pymongo.mongo_client.MongoClient
        assert type(config['database']) == pymongo.database.Database
        assert type(config['collection']) == pymongo.collection.Collection
