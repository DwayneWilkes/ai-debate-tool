import openai
import anthropic
import logging


class APIClient:
    def __init__(self, api_key: str, provider: str, model: str = ""):
        """
        Initialize the API client.

        :param api_key: API key for the provider.
        :param provider: "openai" or "anthropic".
        :param model: Default model to use for requests.
        """
        self.api_key = api_key
        self.provider = provider
        self.model = model
        self.session = self._initialize_client()

    def _initialize_client(self):
        """
        Initialize the appropriate API client.
        """
        if self.provider == "openai":
            return openai.OpenAI(api_key=self.api_key)
        elif self.provider == "anthropic":
            return anthropic.Anthropic(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def call_api(self, prompt: str, model: str = "", **kwargs):
        """
        Call the appropriate API based on the provider.

        :param prompt: Input prompt for the API.
        :param model: Model to use for this request (overrides default).
        :param kwargs: Additional arguments for the API call.
        :return: Response from the API.
        """
        model = model or self.model

        try:
            if self.provider == "openai":
                return self._call_openai(prompt, model, **kwargs)
            elif self.provider == "anthropic":
                return self._call_anthropic(prompt, model, **kwargs)
        except Exception as e:
            logging.error(f"Error during API call: {e}")
            raise

    def _call_openai(self, prompt: str, model: str, max_tokens: int = 150, **kwargs):
        """
        Call OpenAI API with a prompt.

        :param prompt: Input prompt.
        :param model: OpenAI model to use.
        :param max_tokens: Maximum number of tokens to generate. Default is 150.
        :return: Response from OpenAI.
        """
        if not isinstance(self.session, openai.OpenAI):
            raise ValueError("OpenAI API client not initialized correctly.")
        response = self.session.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=max_tokens,
            **kwargs,
        )
        return response.choices[0].message

    def _call_anthropic(self, prompt: str, model: str, max_tokens: int = 150, **kwargs):
        """
        Call Anthropic API with a prompt.

        :param prompt: Input prompt.
        :param model: Anthropic model to use.
        :param max_tokens: Maximum number of tokens to generate. Default is 150.
        :return: Response from Anthropic.
        """
        if not isinstance(self.session, anthropic.Anthropic):
            raise ValueError("Anthropic API client not initialized correctly.")
        response = self.session.messages.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=max_tokens,
            **kwargs,
        )
        return response
