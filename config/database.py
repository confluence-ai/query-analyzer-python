# Import necessary libraries
import os
import psycopg2
from dotenv import load_dotenv
from typing import List, Any, Dict
import threading
from datetime import timedelta
import logging

# Import constants and mappings
from config.constants import BRAND_TABLE, PRODUCT_TABLE

# Configure logging
logger = logging.getLogger(__name__)

class DatabaseManager:
    """ A class to manage PostgreSQL database connections and operations with optimization. """
    
    # Class-level cache
    _cache = {}
    _cache_timestamps = {}
    _cache_ttl = timedelta(hours=1)  # Cache validity: 1 hour
    _cache_lock = threading.Lock()
    
    # Connection pool (shared across instances)
    _connection_pool = None
    _pool_lock = threading.Lock()
    
    def __init__(self, use_connection_pool: bool = True):
        """
            Initialize the DatabaseManager with configuration from environment variables.
            
            Args:
                use_cache (bool): Enable in-memory caching of frequently accessed data
                use_connection_pool (bool): Use connection pooling for better performance
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Set database configuration
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT", 5432))
        self.user = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")
        self.dbname = os.getenv("DB_DATABASE")

        self.use_connection_pool = use_connection_pool
        
        # Initialize connection pool if enabled
        if self.use_connection_pool:
            self._initializeConnectionPool()
    
    def _initializeConnectionPool(self):
        """
            Initialize a connection pool for reusing database connections.
            Connection pooling significantly reduces overhead for repeated queries.
        """
        with self._pool_lock:
            if self._connection_pool is None:
                try:
                    self._connection_pool = psycopg2.pool.ThreadedConnectionPool(
                        minconn=2,      # Minimum connections in pool
                        maxconn=10,     # Maximum connections in pool
                        host=self.host,
                        port=self.port,
                        user=self.user,
                        password=self.password,
                        dbname=self.dbname
                    )
                    logger.info("Database connection pool initialized")
                except Exception as e:
                    logger.error(f"Failed to initialize connection pool: {e}")
                    self._connection_pool = None
    
    def _getConnection(self) -> psycopg2.extensions.connection:
        """
            Create and return a database connection (from pool if available).
            
            Returns:
                psycopg2.extensions.connection: Active database connection
        """
        if self.use_connection_pool and self._connection_pool:
            try:
                return self._connection_pool.getconn()
            except Exception as e:
                logger.warning(f"Failed to get pooled connection, falling back: {e}")
        
        # Fallback to regular connection
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.dbname,
        )
    
    def _releaseConnection(self, conn: psycopg2.extensions.connection):
        """
            Release connection back to pool or close it.
            
            Args:
                conn: Database connection to release
        """
        if self.use_connection_pool and self._connection_pool:
            try:
                self._connection_pool.putconn(conn)
                return
            except Exception as e:
                logger.warning(f"Failed to return connection to pool: {e}")
        
        # Fallback to closing connection
        try:
            conn.close()
        except Exception as e:
            logger.error(f"Error closing connection: {e}")
    
    def _fetchData(self, table: str, text: str) -> List[Any]:
        """
            Fetch data from a specified table in the database.
            Implements caching and optimized queries.
            
            Args:
                table (str): The table name to query
                text (str): Text from user
            
            Returns:
                List[Any]: List of values from the specified column. Returns empty list on error.
        """
        conn = None
        try:
            # Establish database connection
            conn = self._getConnection()
            cur = conn.cursor()
            search_term = f"{text}%"
            
            # Build optimized SQL query
            if table == PRODUCT_TABLE:
                query = f'SELECT DISTINCT id, name FROM {table} WHERE name ILIKE %s and "isPublished" = True LIMIT 10;'
            else:
                query = f'SELECT DISTINCT id, name FROM {table} WHERE name ILIKE %s LIMIT 10;'
            
            # Execute query
            logger.debug(f"Executing query: {query}")
            cur.execute(query, (search_term,))
            
            # Fetch all results
            rows = cur.fetchall()
            
            # Close cursor
            cur.close()
            
            # Extract column values (filter out None values)
            result = [{'id': row[0], 'name': row[1]} for row in rows if row[0] is not None]
            
            logger.info(f"Fetched {len(result)} items from {table}")
            return result
            
        except psycopg2.Error as e:
            logger.error(f"Database error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return []
        finally:
            if conn:
                self._releaseConnection(conn)

    def fetchBrandNames(self, text: str) -> List[str]:
        """
            Fetch brand names from the Brand table.
            
            Args:
                text (str): Users input text
            
            Returns:
                List[str]: List of brand names
        """
        return self._fetchData(BRAND_TABLE, text)
    
    def fetchProductNames(self, text: str) -> List[str]:
        """
            Fetch all product names from the product table.
            
            Args:
                text (str): Users input text
            Returns:
                List[str]: List of product names
        """
        return self._fetchData(PRODUCT_TABLE, text)
    
    def closeConnectionPool(self):
        """
            Close all connections in the pool.
            Call this when shutting down the application.
        """
        with self._pool_lock:
            if self._connection_pool:
                self._connection_pool.closeall()
                self._connection_pool = None
                logger.info("Connection pool closed")
    
    def getStats(self) -> Dict[str, Any]:
        """
            Get statistics about cache and connection pool.
            
            Returns:
                Dict with cache size, hit rate, and pool info
        """
        with self._cache_lock:
            return {
                'cache_entries': len(self._cache),
                'cache_tables': list(set(k.split(':')[0] for k in self._cache.keys())),
                'connection_pool_active': self._connection_pool is not None,
            }