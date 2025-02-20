from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class MySQLQueryToolInput(BaseModel):
    """Input schema for MySQL Query Tool."""
    user_name: str = Field(..., description="The username for whom KYC compliance is being checked")
    query: str = Field(..., description="The SQL query to execute (SELECT statements only)")

class MySQLQueryTool(BaseTool):
    name: str = "MySQLQueryTool"
    description: str = "Executes MySQL queries securely and fetches results."
    args_schema: Type[BaseModel] = MySQLQueryToolInput

    def _run(self, user_name: str, query: str) -> str:
        # # Establish connection to MySQL using mysql.connector module - currently this is dummy code

        print("Query passed to custom tool:", query)
        print("User name passed to custom tool:", user_name)

        if(user_name.lower() == 'vaibhav'):
            print("Sending True from custom tool...")
            return "True"
        else:
            print("Sending False from custom tool...")
            return "False"
