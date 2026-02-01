import time
import logging
import pandas as pd
import psycopg2.pool
from os import path, listdir
from datetime import datetime
from psycopg2.extras import execute_batch


class PostgresqlDatabase:
    """
        Postgresql database that opens/closes the connection for each operation.
        It keeps credentials in the instance for reuse of the object.
    """

    def __init__(
        self,
        postgre_host: str,
        postgre_database: str,
        postgre_user: str,
        postgre_password: str,
        postgre_port: str,
        root_path: str,
        query_timeout: float = 10.0,
        num_conn: list=[2, 4],
        logger: logging.Logger=None,
    ):
        self.host = postgre_host
        self.database = postgre_database
        self.user = postgre_user
        self.password = postgre_password
        self.port = postgre_port
        self.executor = executor
        self.root_path = root_path
        self.query_timeout = query_timeout
        self.minconn = min(num_conn)
        self.maxconn = max(num_conn)
        self.logger = logger

        self.pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=self.minconn,
            maxconn=self.maxconn,
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port,
        )

    def _read_sql(self, folder: str, filename: str) -> str:
        try:
            full_path = path.join(self.root_path, 'persistence', 'sql', folder, filename)

            with open(full_path, 'r', encoding='utf-8') as f:
                sql_query = f.read()

            return sql_query

        except Exception as e:
            raise e

    def _execute_fetchone(self, query: str, query_params: tuple):
        """
            Execute a fetchone query (threaded if executor provided).
            Returns single value or None.
        """

        conn = None

        try:
            conn = self.pool.getconn()

            with conn.cursor() as cur:
                cur.execute(query, query_params)
                data = cur.fetchone()

                return data[0] if data else None

        except Exception as e:
            if conn: conn.rollback()
            raise e

        finally:
            if conn: self.pool.putconn(conn)

    def _execute_simple_query(self, query: str, query_params: tuple):
        """
            Execute an select query and return any fetched results as DataFrame.
        """

        conn = None

        try:
            conn = self.pool.getconn()

            with conn.cursor() as cur:
                cur.itersize = 5000
                cur.execute(query, query_params)
                data = cur.fetchall()

                if not data: return pd.DataFrame()

                return pd.DataFrame(data, columns=[d[0] for d in cur.description])

        except Exception as e:
            if conn: conn.rollback()
            raise e

        finally:
            if conn: self.pool.putconn(conn)

    def _execute_insert_query(self, query: str, query_params: tuple):
        """
            Execute an insert/update/delete query and return any fetched results as DataFrame.
        """

        conn = None

        try:
            conn = self.pool.getconn()

            with conn.cursor() as cur:
                cur.itersize = 5000
                cur.execute(query, query_params)

                if cur.description:
                    data = cur.fetchall()
                    colnames = [desc[0] for desc in cur.description]

                    conn.commit()

                    return pd.DataFrame(data, columns=colnames)

                conn.commit()
                return None

        except Exception as e:
            if conn: conn.rollback()
            raise e

        finally:
            if conn: self.pool.putconn(conn)

    def _execute_insert_query_many(self, query: str, query_params: list):
        """
            Execute an insert/update/delete query to many values.
        """

        conn = None

        try:
            conn = self.pool.getconn()

            with conn.cursor() as cur:
                execute_batch(cur, query, query_params, page_size=1000)

            conn.commit()

            return True

        except Exception as e:
            if conn: conn.rollback()
            raise e

        finally:
            if conn: self.pool.putconn(conn)

    def _simple_query(self, query_params: tuple, filepath: str, step: str):
        self.start_time = time.time()
        file = filepath.split("/")
        filename = file[1]

        try:
            query = self._read_sql(file[0], file[1])

            if query is None:
                self._log_info(f"Execute {step}, {filename} don't exist")
                return None

            response = self._execute_simple_query(query, query_params=query_params)
            self._log_info(f"Execute simple query {step}")

            return response

        except Exception as e:
            self._log_exception(f"Execute simple query {step}", e)
            raise

    def _fetchone_query(self, query_params: tuple, filepath: str, step: str):
        self.start_time = time.time()
        file = filepath.split("/")
        filename = file[1]

        try:
            query = self._read_sql(file[0], file[1])

            if query is None:
                self._log_info(f"Execute {step}, {filename} don't exist")
                return None

            response = self._execute_fetchone(query, query_params=query_params)
            self._log_info(f"Execute {step}")

            return response

        except Exception as e:
            self._log_exception(f"Execute {step}", e)
            raise

    def _insert_query(self, query_params: tuple, filepath: str, step: str):
        self.start_time = time.time()
        file = filepath.split("/")
        filename = file[1]

        try:
            query = self._read_sql(file[0], file[1])

            if query is None:
                self._log_info(f"Execute insert query {step}, {filename} don't exist")
                return None

            response = self._execute_insert_query(query, query_params=query_params)
            self._log_info(f"Execute insert query {step}")
            return response

        except Exception as e:
            self._log_exception(f"Execute insert query {step}", e)
            raise

    def _insert_query_many_values(self, query_params: list, filepath: str, step: str):
        self.start_time = time.time()
        file = filepath.split("/")
        filename = file[1]

        try:
            query = self._read_sql(file[0], file[1])

            if query is None:
                self._log_info(f"Execute insert query many {step}, {filename} doesn't exist")
                return None

            response = self._execute_insert_query_many(query, query_params=query_params)

            self._log_info(f"Execute insert query many {step} - Rows: {len(query_params)}")
            return response

        except Exception as e:
            self._log_exception(f"Execute insert query many {step} failed", e)
            raise

    def _log_info(self, step: str):
        duration = time.time() - self.start_time
        extra = {"duration_ms": round(duration * 1000, 2)}

        self.logger.info(f"[{self.__class__.__name__}] - {step}, duration(ms): {extra.get('duration_ms')}", extra=extra)

    def _log_exception(self, step: str, exc: Exception):
        duration = time.time() - self.start_time
        extra = {"duration_ms": round(duration * 1000, 2), "error": str(exc)}

        self.logger.exception(f"[{self.__class__.__name__}] - {step}, duration(ms): {extra.get('duration_ms')}, error: {extra.get('error')}", extra=extra)

    # ...
