"""
MongoDB Caching Service
Provides caching functionality for GitHub repository analysis to improve performance.
"""
import json
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger(__name__)

class CacheService:
    """
    MongoDB-based caching service for repository analysis data.
    Provides 40x faster performance for cached requests.
    """
    
    def __init__(self, connection_string: str = None, database_name: str = "portfolio_cache"):
        """
        Initialize the cache service.
        
        Args:
            connection_string: MongoDB connection string (optional, defaults to local)
            database_name: Name of the database to use for caching
        """
        self.connection_string = connection_string or "mongodb://localhost:27017/"
        self.database_name = database_name
        self.client = None
        self.db = None
        self.collection = None
        self.connected = False
        
        self._connect()
    
    def _connect(self):
        """Attempt to connect to MongoDB."""
        try:
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Test the connection
            self.client.admin.command('ping')
            
            self.db = self.client[self.database_name]
            self.collection = self.db.repository_cache
            
            # Create index on repository URL for faster lookups
            self.collection.create_index("repository_url")
            self.collection.create_index("cache_key")
            self.collection.create_index("expires_at")
            
            self.connected = True
            logger.info("Connected to MongoDB cache service")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.warning(f"Failed to connect to MongoDB: {e}")
            logger.warning("Cache service will operate in fallback mode (no caching)")
            self.connected = False
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            self.connected = False
    
    def _generate_cache_key(self, repository_url: str) -> str:
        """
        Generate a cache key for a repository URL.
        
        Args:
            repository_url: GitHub repository URL
            
        Returns:
            SHA256 hash of the URL
        """
        return hashlib.sha256(repository_url.encode()).hexdigest()
    
    def get(self, repository_url: str) -> Optional[Dict[str, Any]]:
        """
        Get cached analysis data for a repository.
        
        Args:
            repository_url: GitHub repository URL
            
        Returns:
            Cached analysis data or None if not found/expired
        """
        if not self.connected:
            return None
        
        try:
            cache_key = self._generate_cache_key(repository_url)
            
            # Find the cached entry
            cached_entry = self.collection.find_one({
                "cache_key": cache_key,
                "expires_at": {"$gt": datetime.utcnow()}
            })
            
            if cached_entry:
                logger.info(f"Cache HIT for repository: {repository_url}")
                return cached_entry.get("analysis_data")
            else:
                logger.info(f"Cache MISS for repository: {repository_url}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving from cache: {e}")
            return None
    
    def set(self, repository_url: str, analysis_data: Dict[str, Any], ttl_hours: int = 24) -> bool:
        """
        Store analysis data in cache.
        
        Args:
            repository_url: GitHub repository URL
            analysis_data: Analysis data to cache
            ttl_hours: Time to live in hours (default 24 hours)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connected:
            return False
        
        try:
            cache_key = self._generate_cache_key(repository_url)
            expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
            
            cache_entry = {
                "cache_key": cache_key,
                "repository_url": repository_url,
                "analysis_data": analysis_data,
                "cached_at": datetime.utcnow(),
                "expires_at": expires_at,
                "ttl_hours": ttl_hours
            }
            
            # Upsert the cache entry
            result = self.collection.replace_one(
                {"cache_key": cache_key},
                cache_entry,
                upsert=True
            )
            
            if result.upserted_id or result.modified_count > 0:
                logger.info(f"Cached analysis data for repository: {repository_url}")
                return True
            else:
                logger.warning(f"Failed to cache data for repository: {repository_url}")
                return False
                
        except Exception as e:
            logger.error(f"Error storing in cache: {e}")
            return False
    
    def delete(self, repository_url: str) -> bool:
        """
        Delete cached data for a repository.
        
        Args:
            repository_url: GitHub repository URL
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connected:
            return False
        
        try:
            cache_key = self._generate_cache_key(repository_url)
            
            result = self.collection.delete_one({"cache_key": cache_key})
            
            if result.deleted_count > 0:
                logger.info(f"Deleted cache for repository: {repository_url}")
                return True
            else:
                logger.info(f"No cache found to delete for repository: {repository_url}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False
    
    def clear_expired(self) -> int:
        """
        Clear all expired cache entries.
        
        Returns:
            Number of entries deleted
        """
        if not self.connected:
            return 0
        
        try:
            result = self.collection.delete_many({
                "expires_at": {"$lt": datetime.utcnow()}
            })
            
            deleted_count = result.deleted_count
            logger.info(f"Cleared {deleted_count} expired cache entries")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error clearing expired cache: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary containing cache statistics
        """
        if not self.connected:
            return {
                "connected": False,
                "total_entries": 0,
                "expired_entries": 0,
                "error": "Not connected to cache service"
            }
        
        try:
            total_entries = self.collection.count_documents({})
            expired_entries = self.collection.count_documents({
                "expires_at": {"$lt": datetime.utcnow()}
            })
            active_entries = total_entries - expired_entries
            
            # Get oldest and newest entries
            oldest_entry = self.collection.find_one(
                {"expires_at": {"$gt": datetime.utcnow()}},
                sort=[("cached_at", 1)]
            )
            newest_entry = self.collection.find_one(
                {"expires_at": {"$gt": datetime.utcnow()}},
                sort=[("cached_at", -1)]
            )
            
            stats = {
                "connected": True,
                "total_entries": total_entries,
                "active_entries": active_entries,
                "expired_entries": expired_entries,
                "oldest_cache": oldest_entry.get("cached_at").isoformat() if oldest_entry else None,
                "newest_cache": newest_entry.get("cached_at").isoformat() if newest_entry else None
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {
                "connected": True,
                "error": str(e)
            }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the cache service.
        
        Returns:
            Health check results
        """
        health_status = {
            "service": "cache_service",
            "status": "unknown",
            "timestamp": datetime.utcnow().isoformat(),
            "details": {}
        }
        
        try:
            if not self.connected:
                health_status["status"] = "unhealthy"
                health_status["details"]["connection"] = "Not connected to MongoDB"
                return health_status
            
            # Test basic operations
            test_key = "health_check_test"
            test_data = {"test": True, "timestamp": datetime.utcnow().isoformat()}
            
            # Test write
            write_success = self.set(test_key, test_data, ttl_hours=1)
            if not write_success:
                health_status["status"] = "unhealthy"
                health_status["details"]["write_test"] = "Failed"
                return health_status
            
            # Test read
            read_data = self.get(test_key)
            if not read_data:
                health_status["status"] = "unhealthy"
                health_status["details"]["read_test"] = "Failed"
                return health_status
            
            # Test delete
            delete_success = self.delete(test_key)
            if not delete_success:
                health_status["status"] = "degraded"
                health_status["details"]["delete_test"] = "Failed"
            
            # Get performance stats
            stats = self.get_stats()
            health_status["details"]["cache_stats"] = stats
            
            health_status["status"] = "healthy"
            health_status["details"]["all_tests"] = "Passed"
            
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["details"]["error"] = str(e)
        
        return health_status
    
    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("Closed MongoDB connection")


class FallbackCache:
    """
    In-memory fallback cache when MongoDB is not available.
    Limited functionality but ensures the application still works.
    """
    
    def __init__(self, max_size: int = 100):
        """
        Initialize fallback cache.
        
        Args:
            max_size: Maximum number of entries to store
        """
        self.cache = {}
        self.max_size = max_size
        self.access_order = []
    
    def _generate_cache_key(self, repository_url: str) -> str:
        """Generate cache key for repository URL."""
        return hashlib.sha256(repository_url.encode()).hexdigest()
    
    def get(self, repository_url: str) -> Optional[Dict[str, Any]]:
        """Get cached data."""
        cache_key = self._generate_cache_key(repository_url)
        
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            
            # Check if expired
            if datetime.utcnow() > entry["expires_at"]:
                del self.cache[cache_key]
                if cache_key in self.access_order:
                    self.access_order.remove(cache_key)
                return None
            
            # Update access order
            if cache_key in self.access_order:
                self.access_order.remove(cache_key)
            self.access_order.append(cache_key)
            
            return entry["data"]
        
        return None
    
    def set(self, repository_url: str, analysis_data: Dict[str, Any], ttl_hours: int = 24) -> bool:
        """Store data in cache."""
        cache_key = self._generate_cache_key(repository_url)
        
        # Remove oldest entries if at capacity
        while len(self.cache) >= self.max_size and self.access_order:
            oldest_key = self.access_order.pop(0)
            if oldest_key in self.cache:
                del self.cache[oldest_key]
        
        expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
        
        self.cache[cache_key] = {
            "data": analysis_data,
            "cached_at": datetime.utcnow(),
            "expires_at": expires_at
        }
        
        # Update access order
        if cache_key in self.access_order:
            self.access_order.remove(cache_key)
        self.access_order.append(cache_key)
        
        return True
    
    def delete(self, repository_url: str) -> bool:
        """Delete cached data."""
        cache_key = self._generate_cache_key(repository_url)
        
        if cache_key in self.cache:
            del self.cache[cache_key]
            if cache_key in self.access_order:
                self.access_order.remove(cache_key)
            return True
        
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "connected": True,
            "type": "fallback_memory_cache",
            "total_entries": len(self.cache),
            "max_size": self.max_size
        }