import unittest
from unittest.mock import MagicMock
from backend.app.experts.consultant import Consultant
from backend.app.experts.debater import Debater, IDebater


class BaseExpert:
    """
    Test fixture that provides common setup for testing expert classes.

    Handles initialization of mock objects and common test data used across different expert test cases.

    Attributes:
        api_key (str): The API key for testing.
        provider (str): The provider of the API service. Default is "openai".
        model (str): The model used by the API.
        name (str): The name of the expert.
        word_limit (int): The word limit for the expert's arguments.
        expert (type): The expert instance to test.
        AST_RES (str): The expected assistant response text.
        USR_Q (str): The expected user question text.
        USR_REQ (str): The expected user request text.
        OA_REQ_KEY (str): The key for the opening argument request template.
        NA_REQ_KEY (str): The key for the nth argument request template.
        OA_REQ_VAL (str): The opening argument request text.
        NA_REQ_VAL (str): The nth argument request text.
        RT1_KEY (str): The key for the first round thinking advice template.
        RT2_KEY (str): The key for the second round thinking advice template.
        RTN_KEY (str): The key for the nth round thinking advice template.
        RT1_VAL (str): The first round thinking advice text.
        RT2_VAL (str): The second round thinking advice text.
        RTN_VAL (str): The nth round thinking advice text.
        SYS_MESSAGE (str): The expected system message text.
        STORY (str): The story text for constructing arguments.
        TRANSCRIPT (str): The transcript text for constructing arguments.

    Methods:
        __init__(name: str, expert: type, provider: str = "openai"):
            Initialize the base test fixture with the specified expert type.
    """

    def __init__(self, name: str, expert: type, provider: str = "openai"):
        """
        Initialize the base test fixture with the specified expert type.

        Args:
            name (str): The name of the expert.
            expert (type): The expert class to test.
            provider (str): The provider of the API service. Default is "openai".
        """
        # Initialize the expert
        self.api_key = "test_api_key"
        self.provider = provider
        self.model = "test_model"
        self.name = name
        self.word_limit = 100
        self.expert = expert(self.api_key, self.provider, self.model, self.name, self.word_limit)

        # Define text constants
        self.AST_RES = "assistant response"
        self.USR_Q = "user question"
        self.USR_REQ = "user request"
        self.OA_REQ_KEY = "opening_argument_request"
        self.NA_REQ_KEY = "nth_argument_request"
        self.OA_REQ_VAL = "opening argument request"
        self.NA_REQ_VAL = "nth argument request"
        self.RT1_KEY = "first_round_thinking"
        self.RT2_KEY = "second_round_thinking"
        self.RTN_KEY = "nth_round_thinking"
        self.RT1_VAL = "first round thinking"
        self.RT2_VAL = "second round thinking"
        self.RTN_VAL = "nth round thinking"
        self.SYS_MESSAGE = "system message"
        self.STORY = "Once upon a time..."
        self.TRANSCRIPT = "In the beginning..."

        # Define text for the question and answers
        self.expert._question = "What is the best programming language?"
        self.expert._answer_defending = "Python"
        self.expert._answer_opposing = "JavaScript"

        # Mock the protocol prompt templates
        self.expert._protocol.system = MagicMock(substitute=MagicMock(return_value=self.SYS_MESSAGE))
        self.expert._protocol.thinking_advice = {
            self.RT1_KEY: MagicMock(return_value=self.RT1_VAL),
            self.RT2_KEY: MagicMock(return_value=self.RT2_VAL),
            self.RTN_KEY: MagicMock(return_value=self.RTN_VAL),
        }
        self.expert._protocol.user_question = MagicMock(substitute=MagicMock(return_value=self.USR_Q))
        self.expert._protocol.assistant_response = MagicMock(substitute=MagicMock(return_value=self.AST_RES))
        self.expert._protocol.user_request = MagicMock(substitute=MagicMock(return_value=self.USR_REQ))
        self.expert._protocol.new_argument = {
            self.OA_REQ_KEY: MagicMock(substitute=MagicMock(return_value=self.OA_REQ_VAL)),
            self.NA_REQ_KEY: MagicMock(substitute=MagicMock(return_value=self.NA_REQ_VAL)),
        }


class BaseExpertTest(unittest.TestCase):
    """
    Base test class for expert implementations.

    Contains common test logic shared across different expert types.
    Should not be instantiated directly - use specific expert test classes instead.

    Attributes:
        expert_class (type): The expert class to test.

    Methods:
        setUp():
            Initialize the base test fixture and expert instance.
        test_initial_position():
            Test the initial position setup for standard expert types.
        test_initial_response():
            Test the expert's initial response generation.
        test_construct_argument_first_round():
            Test the construction of an argument in the first round.
        test_construct_argument_nth_round():
            Test the construction of an argument in a subsequent round.
    """

    expert_class = None

    def setUp(self):
        """Initialize the base test fixture and expert instance."""
        if self.__class__ == BaseExpertTest:
            raise unittest.SkipTest("Base class for expert tests - should not run directly")
        self.base = BaseExpert("Test " + self.expert_class.__name__, self.expert_class)

    def test_initial_position(self):
        """
        Test the initial position setup for standard expert types.

        Verifies that the expert correctly processes initial question and answers.
        This implementation is shared by Consultant and Debater, but overridden by IDebater.
        """
        result = self.base.expert.initial_position(
            self.base.expert._question, self.base.expert._answer_defending, self.base.expert._answer_opposing
        )
        self.assertEqual(result, self.base.USR_Q)
        self.base.expert._protocol.user_question.substitute.assert_called_once_with(
            question=self.base.expert._question,
            answer_defending=self.base.expert._answer_defending,
            answer_opposing=self.base.expert._answer_opposing,
        )

    def test_initial_response(self):
        """
        Test the expert's initial response generation.

        Verifies that the expert generates appropriate responses using the configured question and answers.
        """
        result = self.base.expert.initial_response()
        self.assertEqual(result, self.base.AST_RES)
        self.base.expert._protocol.assistant_response.substitute.assert_called_once_with(
            question=self.base.expert._question,
            answer_defending=self.base.expert._answer_defending,
            answer_opposing=self.base.expert._answer_opposing,
        )

    def test_construct_argument_first_round(self):
        """
        Test the construction of an argument in the first round.

        Verifies that the expert constructs an argument correctly during the first round of interaction.
        """
        result = self.base.expert.construct_argument(self.base.STORY, self.base.TRANSCRIPT)
        self.assertEqual(result, self.base.USR_REQ)
        self.assertEqual(self.base.expert._current_round, 1)
        self.base.expert._protocol.new_argument[self.base.OA_REQ_KEY].substitute.assert_called_once_with(
            question=self.base.expert._question,
            answer_defending=self.base.expert._answer_defending,
        )
        self.base.expert._protocol.user_request.substitute.assert_called_once_with(
            story=self.base.STORY,
            transcript=self.base.TRANSCRIPT,
            new_argument_request=self.base.OA_REQ_VAL,
            thinking_advice=self.base.expert._thinking_advice[self.base.RT1_KEY],
            word_limit=self.base.word_limit,
        )

    def test_construct_argument_nth_round(self):
        """
        Test the construction of an argument in a subsequent round.

        Verifies that the expert constructs an argument correctly during a subsequent round of interaction.
        """
        self.base.expert._current_round = 2
        result = self.base.expert.construct_argument(self.base.STORY, self.base.TRANSCRIPT)
        self.assertEqual(result, self.base.USR_REQ)
        self.assertEqual(self.base.expert._current_round, 3)
        self.base.expert._protocol.new_argument[self.base.NA_REQ_KEY].substitute.assert_called_once_with(
            question=self.base.expert._question,
            answer_defending=self.base.expert._answer_defending,
        )
        self.base.expert._protocol.user_request.substitute.assert_called_once_with(
            story=self.base.STORY,
            transcript=self.base.TRANSCRIPT,
            new_argument_request=self.base.NA_REQ_VAL,
            thinking_advice=self.base.expert._thinking_advice[self.base.RTN_KEY],
            word_limit=self.base.word_limit,
        )


class TestConsultant(BaseExpertTest):
    """
    Test cases for the Consultant expert implementation.

    Inherits from BaseExpertTest and provides the expert class to test.

    Attributes:
        expert_class (type): The expert class to test, in this case Consultant.
    """

    expert_class = Consultant


class TestDebater(BaseExpertTest):
    """Test cases for the Debater expert implementation.

    Inherits from BaseExpertTest and provides the expert class to test.

    Attributes:
        expert_class (type): The expert class to test, in this case Debater.
    """

    expert_class = Debater


class TestIDebater(BaseExpertTest):
    """
    Test cases specific to the Interactive Debater implementation.

    Handles the unique aspects of IDebater including letter-based answer mapping and opponent naming.

    Attributes:
        expert_class (type): The expert class to test, in this case IDebater.

    Methods:
        setUp():
            Override the base setup to configure IDebater-specific parameters.
        test_initial_position():
            Test IDebater's specific initial position implementation.
    """

    expert_class = IDebater

    def setUp(self):
        """
        Override the base setup to configure IDebater-specific parameters

        Configures the opponent name and answer letters for the IDebater expert.
        """
        super().setUp()
        self.base.expert._opponent_name = "Opponent"
        self.base.expert._answer_defending_letter = "A"
        self.base.expert._answer_opposing_letter = "B"

    def test_initial_position(self):
        """
        Test IDebater's specific initial position implementation.

        Verifies handling of letter-mapped answers and opponent configuration.
        Overrides the base implementation due to different parameter requirements.
        """
        result = self.base.expert.initial_position(
            self.base.expert._question,
            {self.base.expert._answer_defending_letter: self.base.expert._answer_defending},
            {self.base.expert._answer_opposing_letter: self.base.expert._answer_opposing},
            self.base.expert._opponent_name,
        )
        self.assertEqual(result, self.base.USR_Q)
        self.base.expert._protocol.user_question.substitute.assert_called_once_with(
            question=self.base.expert._question,
            answer_a=self.base.expert._answer_defending,
            answer_b=self.base.expert._answer_opposing,
            answer_defending_letter=self.base.expert._answer_defending_letter,
            answer_opposing_letter=self.base.expert._answer_opposing_letter,
            opponent_name=self.base.expert._opponent_name,
        )


if __name__ == "__main__":
    unittest.main()
