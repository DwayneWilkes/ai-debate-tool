from backend.app.experts.consultant import Consultant
import pandas as pd
import os


def setup():
    # load data
    data = pd.read_json("data/QuALITY.v1.0.1/QuALITY.v1.0.1.dev", lines=True)
    consultant = Consultant(
        api_key=os.getenv("OPENAI_API_KEY"),
        provider="openai",
        model="gpt-4o-mini",
        name="Consultant",
        word_limit=100,
    )
    return consultant, data


def get_article_info(data, article_id, include_article=False):
    article_data = data[data["article_id"] == article_id].iloc[0]
    questions = [q.get("question") for q in article_data.questions]
    options = [q.get("options") for q in article_data.questions]
    gold_labels = [q.get("gold_label") for q in article_data.questions]
    best_distraction = [
        max(
            set([annotator.get("untimed_best_distractor") for annotator in q.get("validation")]),
            key=[annotator.get("untimed_best_distractor") for annotator in q.get("validation")].count,
        )
        for q in article_data.questions
    ]

    result = []
    for i in range(len(questions)):
        result.append(
            {
                "question": questions[i],
                "options": options[i],
                "gold_label": gold_labels[i],
                "best_distraction": best_distraction[i],
            }
        )

    if include_article:
        result.append({"article": article_data.article})

    return result


def add_to_transcript(transcript, response):
    return transcript + response + "\n\n"


def set_initial_position(consultant, question, answer_defending, answer_opposing):
    ip = consultant.initial_position(question, answer_defending, answer_opposing)
    response = consultant.call_api(ip, max_tokens=1000)
    return response


def construct_argument(consultant, story, transcript):
    argument = consultant.construct_argument(story, transcript)
    response = consultant.call_api(argument, max_tokens=1000)
    return response


# cli to interact with the consultant
def main():
    consultant, data = setup()

    article_id = 52845  # First article in the dataset
    article_info = get_article_info(data, article_id, include_article=True)

    question_id = 0
    question_info = article_info[question_id]

    options = question_info.get("options")
    gold_label = question_info.get("gold_label")
    best_distraction = question_info.get("best_distraction")

    question = question_info.get("question")
    # Arguing the truth
    answer_defending = options[gold_label - 1]
    answer_opposing = options[best_distraction - 1]

    # Arguing the distraction
    # answer_defending = options[best_distraction - 1]
    # answer_opposing = options[gold_label - 1]

    transcript = ""

    response = f"Consultant: {set_initial_position(consultant, question, answer_defending, answer_opposing).content}"
    transcript = add_to_transcript(transcript, response)

    story = article_info[-1].get("article")
    for round in range(3):
        response = f"Consultant: {construct_argument(consultant, story, transcript).content}"
        transcript = add_to_transcript(transcript, response)
    print(transcript)


if __name__ == "__main__":
    main()
