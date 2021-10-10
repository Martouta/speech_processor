<%!
    import os

    def mongodb_host():
        return os.getenv('MONGO_URL', 'localhost:27017')

    def mongodb_database():
        return os.environ['MONGO_DB']
%>

development:
  database: ${ mongodb_database() }
  host_with_port: ${ mongodb_host() }

production:
  database: ${ mongodb_database() }
  host_with_port: ${ mongodb_host() }

test:
  database: ${ mongodb_database() }
  host_with_port: ${ mongodb_host() }
