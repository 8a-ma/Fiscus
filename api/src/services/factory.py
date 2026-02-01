import logging
from src.config.config import Config
from src.persistence.Postgresql import PostgresqlDatabase

class ServicesFactory:
    def __init__(self):
        self._services = {}
        self.logger = logger.getLogger(__name__)

    def init_app(self, logger: logging.Logger):
        self.logger = logger

    @property
    def db(self):
        if 'db' not in self._services:
            self._services['db'] = PostgresqlDatabase(
                postgre_host=Config.POSTGERSQL_HOST,
                postgre_database=Config.POSTGERSQL_DB,
                postgre_user=Config.POSTGERSQL_USER,
                postgre_password=Config.POSTGERSQL_PASSWORD,
                postgre_port=Config.POSTGERSQL_PORT,
                root_path=Config.ROOT_PATH,
                query_timeout=Config.POSTGERSQL_QUERY_TIMEOUT,
                num_conn=[Config.POSTGRESQL_POOL_MIN, Config.POSTGRESQL_POOL_MAX],
                logger=self.logger,
            )

        return self._services.get('db')

services = ServicesFactory()
