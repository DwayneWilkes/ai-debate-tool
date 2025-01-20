from backend.app.api_clients.base import APIClient
import backend.app.prompts.consultant_prompt as consultant


class Consultant(APIClient):
    """
    A class to represent a consultant that interacts with an API to generate arguments for consultancy.

    Attributes:
        api_key (str): The API key for authentication.
        provider (str): The provider of the API service. "openai" or "anthropic".
        model (str): The model used by the API.
        name (str): The name of the consultant.
        word_limit (int): The word limit for the arguments. Default is 100.
        _protocol: The protocol used for generating arguments.
        _system: The system message template.
        _thinking_advice: The thinking advice template.
        _current_round (int): The current round of the consultancy.
        _question (str): The consultancy question.
        _answer_defending (str): The answer that the consultant is defending.
        _answer_opposing (str): The answer that the consultant is opposing.
        _current_argument (str): The current argument being constructed.

    Methods:
        initial_position(question: str, answer_defending: str, answer_opposing: str):
            Sets the initial position for the consultancy and returns the user question template.
        initial_response():
            Returns the assistant response template for the initial position.
        construct_argument(story: str, transcript: str):
            Constructs an argument based on the current round and returns the argument template.
    """

    def __init__(self, api_key: str, provider: str, model: str, name: str, word_limit: int = 100):
        super().__init__(api_key, provider, model)

        self._protocol = consultant
        self._name = name
        self._word_limit = word_limit
        self._system = self._protocol.system.substitute(name=self._name, word_limit=self._word_limit)
        self._thinking_advice = self._protocol.thinking_advice
        self._current_round = 0

    def initial_position(self, question: str, answer_defending: str, answer_opposing: str) -> str:
        """
        Sets the initial position for the debate by storing the question and the answers for defending and opposing positions.

        Args:
            question (str): The debate question.
            answer_defending (str): The answer or position that will be defended.
            answer_opposing (str): The answer or position that will be opposed.

        Returns:
            str: A formatted string with the user's question and the provided answers.
        """
        self._question = question
        self._answer_defending = answer_defending
        self._answer_opposing = answer_opposing
        return self._protocol.user_question.substitute(
            question=self._question, answer_defending=self._answer_defending, answer_opposing=self._answer_opposing
        )

    def initial_response(self) -> str:
        """
        Generates the initial response from the assistant based on the provided question
        and answers.

        Returns:
            str: The formatted initial response from the assistant.
        """
        return self._protocol.assistant_response.substitute(
            question=self._question, answer_defending=self._answer_defending, answer_opposing=self._answer_opposing
        )

    def construct_argument(self, story: str, transcript: str) -> str:
        """
        Constructs an argument based on the provided story and transcript.
        This method increments the current round counter and constructs an argument
        using the protocol's user request template. The constructed argument varies
        depending on whether it is the first round or a subsequent round.
        Args:
            story (str): The story to be included in the argument.
            transcript (str): The transcript to be included in the argument.
        Returns:
            str: The constructed argument.
        """
        if self._current_round == 0:
            self._current_argument = self._protocol.user_request.substitute(
                story=story,
                transcript=transcript,
                new_argument_request=self._protocol.new_argument["opening_argument_request"].substitute(
                    question=self._question, answer_defending=self._answer_defending
                ),
                thinking_advice=self._thinking_advice["first_round_thinking"],
                word_limit=self._word_limit,
            )
        else:
            self._current_argument = self._protocol.user_request.substitute(
                story=story,
                transcript=transcript,
                new_argument_request=self._protocol.new_argument["nth_argument_request"].substitute(
                    question=self._question, answer_defending=self._answer_defending
                ),
                thinking_advice=self._thinking_advice["nth_round_thinking"],
                word_limit=self._word_limit,
            )
        self._current_round += 1

        return self._current_argument
