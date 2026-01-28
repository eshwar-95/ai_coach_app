"""Azure OpenAI integration module."""
import os
from typing import Optional
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from src.config import (
    AZURE_ENDPOINT,
    AZURE_API_KEY,
    AZURE_DEPLOYMENT_NAME,
    AZURE_API_VERSION,
    TEMPERATURE,
    MAX_TOKENS,
)


class AzureOpenAIClient:
    """Client for Azure OpenAI services."""

    def __init__(self):
        """Initialize Azure OpenAI client."""
        if not AZURE_ENDPOINT or not AZURE_API_KEY:
            raise ValueError(
                "Azure endpoint and API key must be configured in .env file"
            )

        self.client = ChatCompletionsClient(
            endpoint=AZURE_ENDPOINT,
            credential=AzureKeyCredential(AZURE_API_KEY),
        )
        self.deployment_name = AZURE_DEPLOYMENT_NAME

    def get_response(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
    ) -> str:
        """
        Get response from Azure OpenAI model.

        Args:
            system_prompt: System prompt for the model
            user_message: User message/query
            temperature: Temperature for response generation
            max_tokens: Maximum tokens in response

        Returns:
            Model response text
        """
        try:
            response = self.client.complete(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                model=self.deployment_name,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Error getting response from Azure OpenAI: {str(e)}")

    def get_response_with_context(
        self,
        system_prompt: str,
        user_context: dict,
        user_query: str,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
    ) -> str:
        """
        Get response with embedded user context in the prompt.

        Args:
            system_prompt: System prompt template
            user_context: Dictionary containing user information
            user_query: User's specific query
            temperature: Temperature for response generation
            max_tokens: Maximum tokens in response

        Returns:
            Model response text
        """
        # Embed user context into the prompt
        context_str = self._format_user_context(user_context)
        enhanced_system_prompt = f"{system_prompt}\n\n## User Context:\n{context_str}"

        return self.get_response(
            enhanced_system_prompt, user_query, temperature, max_tokens
        )

    @staticmethod
    def _format_user_context(context: dict) -> str:
        """Format user context for embedding in prompts."""
        formatted_lines = []
        for key, value in context.items():
            if value is not None:
                formatted_lines.append(f"- {key}: {value}")
        return "\n".join(formatted_lines)
