"""Databricks LLM integration module."""
import requests
from src.config import DATABRICKS_TOKEN, DATABRICKS_LLM_ENDPOINT, DATABRICKS_MODEL


class DatabricksLLMClient:
    """Client for Databricks LLM serving endpoints."""

    def __init__(self):
        """Initialize Databricks LLM client."""
        if not DATABRICKS_TOKEN:
            raise ValueError("DATABRICKS_TOKEN is not configured in .env file")
        
        if not DATABRICKS_LLM_ENDPOINT:
            raise ValueError("DATABRICKS_LLM_ENDPOINT is not configured in .env file")

        self.endpoint = DATABRICKS_LLM_ENDPOINT
        self.token = DATABRICKS_TOKEN
        self.model = DATABRICKS_MODEL or "databricks-claude-sonnet-4-5"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def get_response(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 2000,
    ) -> str:
        """
        Get response from Databricks LLM.

        Args:
            system_prompt: System prompt for the model
            user_message: User message/query
            max_tokens: Maximum tokens in response

        Returns:
            Model response text
        """
        try:
            payload = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
            }
            
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Handle different response formats
            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            elif "message" in result:
                return result["message"]["content"]
            else:
                raise ValueError(f"Unexpected response format: {result}")
                
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error getting response from Databricks LLM: {str(e)}")
        except (KeyError, IndexError, ValueError) as e:
            raise RuntimeError(f"Error parsing Databricks LLM response: {str(e)}")

    def get_response_with_context(
        self,
        system_prompt: str,
        user_context: dict,
        user_query: str,
        max_tokens: int = 2000,
    ) -> str:
        """
        Get response with embedded user context.

        Args:
            system_prompt: System prompt template
            user_context: Dictionary containing user information
            user_query: User's specific query
            max_tokens: Maximum tokens in response

        Returns:
            Model response text
        """
        # Embed context into the prompt
        context_str = "\n".join([f"- {k}: {v}" for k, v in user_context.items()])
        full_prompt = f"{user_query}\n\nUser Context:\n{context_str}"

        return self.get_response(system_prompt, full_prompt, max_tokens)