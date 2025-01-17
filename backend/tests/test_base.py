import unittest
from unittest.mock import patch
from backend.app.api_clients.base import APIClient

OPENAI_PATCH = "backend.app.api_clients.base.openai.OpenAI"
ANTHROPIC_PATCH = "backend.app.api_clients.base.anthropic.Anthropic"
APICLIENT_PATCH = "backend.app.api_clients.base.APIClient"


class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.openai_provider = "openai"
        self.anthropic_provider = "anthropic"
        self.model = "test_model"
        self.prompt = "test_prompt"
        self.response = "test_response"

    @patch(OPENAI_PATCH, autospec=True)
    def test_initialize_openai_client(self, MockOpenAI):
        client = APIClient(api_key=self.api_key, provider=self.openai_provider)
        MockOpenAI.assert_called_once_with(api_key=self.api_key)
        self.assertIsInstance(client.session, MockOpenAI._spec_class)

    @patch(ANTHROPIC_PATCH, autospec=True)
    def test_initialize_anthropic_client(self, MockAnthropic):
        client = APIClient(api_key=self.api_key, provider=self.anthropic_provider)
        MockAnthropic.assert_called_once_with(api_key=self.api_key)
        self.assertIsInstance(client.session, MockAnthropic._spec_class)

    def test_initialize_client_invalid_provider(self):
        provider = "invalid_provider"
        with self.assertRaises(ValueError):
            APIClient(api_key=self.api_key, provider=provider)

    @patch(APICLIENT_PATCH + "._call_openai")
    def test_call_openai_api(self, MockAPIClient):
        MockAPIClient.return_value = self.response
        client = APIClient(api_key=self.api_key, provider=self.openai_provider)
        response = client.call_api(prompt=self.prompt, model=self.model)
        self.assertEqual(response, self.response)

    @patch(APICLIENT_PATCH + "._call_anthropic")
    def test_call_anthropic_api(self, MockAPIClient):
        MockAPIClient.return_value = self.response
        client = APIClient(api_key=self.api_key, provider=self.anthropic_provider)
        response = client.call_api(prompt=self.prompt, model=self.model)
        self.assertEqual(response, self.response)

    @patch(OPENAI_PATCH)
    def test_call_api_error_handling(self, MockOpenAI):
        MockOpenAI().chat.completions.create.side_effect = Exception("API error")
        client = APIClient(api_key=self.api_key, provider=self.openai_provider)
        with self.assertRaises(Exception):
            client.call_api(prompt=self.prompt, model=self.model)


if __name__ == "__main__":
    unittest.main()
