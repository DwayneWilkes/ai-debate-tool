import backend.app.prompts.debater_prompt as debater
import backend.app.prompts.interactive_debater_prompt as interactive_debater
from backend.app.api_clients.base import APIClient


class Debater(APIClient):
    """
    A class to represent a debater that interacts with an API to generate debate arguments.
    Attributes:
        api_key (str): The API key for authentication.
        provider (str): The provider of the API service. "openai" or "anthropic".
        model (str): The model used by the API.
        name (str): The name of the debater.
        word_limit (int): The word limit for the arguments. Default is 100.
        _protocol: The protocol used for generating arguments.
        _system: The system message template.
        _thinking_advice: The thinking advice template.
        _current_round (int): The current round of the debate.
        _question (str): The debate question.
        _answer_defending (str): The answer that the debater is defending.
        _answer_opposing (str): The answer that the debater is opposing.
        _current_argument (str): The current argument being constructed.
    Methods:
        initial_position(question: str, answer_defending: str, answer_opposing: str):
            Sets the initial position for the debate and returns the user question template.
        initial_response():
            Returns the assistant response template for the initial position.
        construct_argument(story: str, transcript: str):
            Constructs an argument based on the current round and returns the argument template.
    """

    def __init__(self, api_key: str, provider: str, model: str, name: str, word_limit: int = 100):
        super().__init__(api_key, provider, model)

        self._protocol = debater
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
                thinking_advice=self._thinking_advice[
                    "second_round_thinking" if self._current_round == 1 else "nth_round_thinking"
                ],
                word_limit=self._word_limit,
            )
        self._current_round += 1

        return self._current_argument


class IDebater(Debater):
    """
    A class to represent an interactive debater that interacts with an API to generate debate arguments.

    Attributes:
        api_key (str): The API key for authentication.
        provider (str): The provider of the API service. "openai" or "anthropic".
        model (str): The model used by the API.
        name (str): The name of the debater.
        word_limit (int): The word limit for the arguments. Default is 100.
        _protocol: The protocol used for generating arguments.
        _system: The system message template.
        _thinking_advice: The thinking advice template.
        _current_round (int): The current round of the debate.
        _question (str): The debate question.
        _opponent_name (str): The name of the opponent.
        _answer_a (str): The text of answer A.
        _answer_b (str): The text of answer B.
        _answer_defending_letter (str): The letter of the answer being defended.
        _answer_defending (str): The text of the answer being defended.
        _answer_opposing_letter (str): The letter of the answer being opposed.
        _answer_opposing (str): The text of the answer being opposed.

    Methods:
        initial_position(question: str, answer_defending: dict[str, str], answer_opposing: dict[str, str], opponent_name: str):
            Initializes the initial position for a debate and returns the user question template.
        initial_response():
            Returns the assistant response template for the initial position.
        construct_argument(story: str, transcript: str):
            Constructs an argument based on the current round and returns the argument template.
    """

    def __init__(self, api_key: str, provider: str, model: str, name: str, word_limit: int = 100):
        super().__init__(api_key, provider, model, name, word_limit)

        self._protocol = interactive_debater
        self._system = self._protocol.system.substitute(name=self._name, word_limit=self._word_limit)
        self._thinking_advice = self._protocol.thinking_advice
        self._current_round = 0

    def initial_position(
        self, question: str, answer_defending: dict[str, str], answer_opposing: dict[str, str], opponent_name: str
    ) -> str:
        """
        Initializes the initial position for a debate.
        Args:
            question (str): The debate question.
            answer_defending (dict[str, str]): The answer letter and answer text that the debater is defending.
            answer_opposing (dict[str, str]): The answer letter and answer text that the debater is opposing.
            opponent_name (str): The name of the opponent.
        Returns:
            str: A formatted string with the debate question and answers.
        """
        self._question = question
        self._opponent_name = opponent_name

        self._answer_a = answer_defending.get("A") or answer_opposing.get("A")
        self._answer_b = answer_defending.get("B") or answer_opposing.get("B")
        self._answer_defending_letter = "A" if self._answer_a == answer_defending.get("A") else "B"
        self._answer_defending = answer_defending[self._answer_defending_letter]
        self._answer_opposing_letter = "A" if self._answer_a == answer_opposing.get("A") else "B"
        self._answer_opposing = answer_opposing[self._answer_opposing_letter]
        return self._protocol.user_question.substitute(
            question=self._question,
            answer_a=self._answer_a,
            answer_b=self._answer_b,
            answer_defending_letter=self._answer_defending_letter,
            answer_opposing_letter=self._answer_opposing_letter,
            opponent_name=self._opponent_name,
        )
