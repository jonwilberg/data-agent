"""Database connection and schema introspection for Census Data Agent."""

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List, Any, Optional
import logging

from config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and schema introspection."""
    
    def __init__(self, use_read_only: bool = True):
        """Initialize database manager.
        
        Args:
            use_read_only: Whether to use read-only database connection
        """
        self.use_read_only = use_read_only
        self._engine: Optional[Engine] = None
    
    @property
    def engine(self) -> Engine:
        """Get database engine, creating if necessary."""
        if self._engine is None:
            if self.use_read_only:
                user = settings.db_read_only_user
                password = settings.db_read_only_password
            else:
                user = settings.db_user
                password = settings.db_password
            
            db_url = f"postgresql://{user}:{password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
            self._engine = create_engine(db_url)
        return self._engine
    
    def get_table_schema(self, table_name: str = "ny_census_data") -> Dict[str, Any]:
        """Get schema information for a specific table.
        
        Args:
            table_name: Name of the table to inspect
            
        Returns:
            Dictionary with table schema information
        """
        try:
            inspector = inspect(self.engine)
            columns = inspector.get_columns(table_name)
            
            schema = {
                "table_name": table_name,
                "columns": []
            }
            
            for column in columns:
                col_info = {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                    "default": column.get("default"),
                    "primary_key": column.get("primary_key", False)
                }
                schema["columns"].append(col_info)
            
            return schema
            
        except SQLAlchemyError as e:
            logger.error(f"Error getting table schema: {e}")
            raise
    
    def get_all_tables(self) -> List[str]:
        """Get list of all tables in the database."""
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except SQLAlchemyError as e:
            logger.error(f"Error getting table list: {e}")
            raise
    
    def get_database_schema(self, include_sample: bool = True) -> Dict[str, Any]:
        """Get complete database schema information.
        
        Args:
            include_sample: Whether to include sample data for each table
        
        Returns:
            Dictionary with complete schema information
        """
        try:
            tables = self.get_all_tables()
            schema = {
                "database": "data_agent",
                "tables": {}
            }
            
            for table in tables:
                table_schema = self.get_table_schema(table)
                
                if include_sample:
                    try:
                        sample_data = self.get_sample_data(table, limit=3)
                        table_schema["sample_data"] = sample_data
                    except SQLAlchemyError as e:
                        logger.warning(f"Could not get sample data for table {table}: {e}")
                        table_schema["sample_data"] = []
                
                schema["tables"][table] = table_schema
            
            return schema
        except SQLAlchemyError as e:
            logger.error(f"Error getting database schema: {e}")
            raise
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results.
        
        Args:
            query: SQL query to execute
            
        Returns:
            List of dictionaries representing query results
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                
                # Convert to list of dictionaries
                columns = result.keys()
                rows = []
                for row in result:
                    rows.append(dict(zip(columns, row)))
                
                return rows
                
        except SQLAlchemyError as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test database connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def get_sample_data(self, table_name: str = "ny_census_data", limit: int = 5) -> List[Dict[str, Any]]:
        """Get sample data from a table.
        
        Args:
            table_name: Name of the table
            limit: Number of rows to return
            
        Returns:
            List of dictionaries with sample data
        """
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.execute_query(query)
    
    def get_column_info(self, table_name: str = "ny_census_data") -> str:
        """Get formatted column information for prompt context.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Formatted string with column information
        """
        schema = self.get_table_schema(table_name)
        
        column_info = []
        for col in schema["columns"]:
            info = f"- {col['name']} ({col['type']})"
            if col['primary_key']:
                info += " [PRIMARY KEY]"
            if not col['nullable']:
                info += " [NOT NULL]"
            column_info.append(info)
        
        return f"Table: {table_name}\nColumns:\n" + "\n".join(column_info)


# Global database manager instance
db_manager = DatabaseManager(use_read_only=True)