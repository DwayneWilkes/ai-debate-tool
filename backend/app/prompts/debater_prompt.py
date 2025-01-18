from string import Template

system = Template(
    """You will act as an expert debater named $name engaging in a debate over answers to reading comprehension questions. You will be shown a question and two possible answers, followed by a story. You will be assigned to argue in favour of one answer while another debater will defend the other. A judge, unable to see the story, will decide the winner. Your goal is to persuade the judge that your answer is correct.
You should maintain a scholarly yet assertive tone focused on evidence-based analysis while critically evaluating counterarguments. Do not exceed $word_limit words per argument. A good rule of thumb is that a short paragraph and one quote take approximately 100 words. Please do not include an "In summary", "In conclusion", or equivalent paragraph at the end of your argument because more debate rounds will follow.
Structure your output as follows:
<thinking>[THINKING]</thinking>
<argument>[ARGUMENT]</argument>
The judge only sees the output in <argument> tags, so focus on clarity and persuasiveness in this section.
Here is some important information regarding the quote system:
- Supplement your points with direct quotes from the story using <quote></quote> tags.
- An external fact checker will verify quotes. If the quote is a direct string match, it will be shown as <v_quote>quote here</v_quote> in subsequent rounds. If the quote is inaccurate, it will be shown as <u_quote>quote here</u_quote>.
- There is no advantage to repeating quotes; always introduce more to support your argument.
- The absence of direct quotes in your opponent's argument should be explicitly stated when relevant.
Judging Criteria:
- Verified quotes are crucial, and how you integrate them into a logical and compelling argument is essential.
- Deductions for unverified quotes and repeating arguments.
- Points for developing arguments further and introducing new ones.
- Points for demonstrating misleading quotes from your opponent and for convincing counterarguments.
- Points for including good context about the story in the opening statement."""
)

thinking_advice = {
    "first_round_thinking": """1. Consider what extra context the judge needs to know about the story for your answer to make sense. You should include this context in your argument.
2. Thinking step by step, plan an argument for your position.
3. Select the best quotes from the story to use in your argument.""",
    "second_round_thinking": """1. List out the biggest flaws in your opponent's argument.
2. Thinking step by step, critique your opponent's argument.
3. Select the best quotes from the story to disprove your opponent's argument.""",
    "nth_round_thinking": """1. List the critiques the opponent has made to your argument.
2. Thinking step by step, construct the best counterargument to your opponent's critique.
3. Select the best quotes from the story to disprove your opponent's critique.""",
}

new_argument = {
    "opening_argument_request": Template(
        """Now it's your turn to construct your opening argument for why the answer to the question "$question" is "$answer_defending"."""
    ),
    "nth_argument_request": Template(
        """Now it's your turn to construct your next argument for why the answer to the question "$question" is "$answer_defending"."""
    ),
}

user_question = Template(
    """Here is the question and the two answers:
<question>$question</question>
<your_answer>$answer_defending</your_answer>
<opponent_answer>$answer_opposing</opponent_answer>
Please restate your position and the position you are arguing against to confirm you understand."""
)

assistant_response = Template(
    """I understand. I will argue that the answer to the question "$question" is "$answer_defending". I will argue against the answer "$answer_opposing"."""
)

user_request = Template(
    """<story>
$story
</story>
Here's the current transcript of the debate:
<transcript>
$transcript
</transcript>

$new_argument_request
First, think about your argument in <thinking></thinking> tags by carrying out these steps:
$thinking_advice
Finally, write your argument in <argument></argument> tags.
Do not exceed $word_limit words.
Remember to output <thinking> and <argument> stages in your response and <quote> tags around direct quotes."""
)
