import csv

QUESTIONS: list[str] = [
    "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10",
    "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "N10",
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10",
    "O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8",	"O9", "O10"
]


def predict_answer_vector(answer_map: dict[str, int]) -> list[int]:
    """
    Given a partially answered Five-Personality-Test, i.e. 5 answers each of which is for one E, one N, one A, one C,
    and one O type question, predicts the remaining 45 answers.

    The prediction first finds the top 10 most similar answers from data.csv records. The for each of the 50 questions,
    compute the most frequent answers for each question in this 10 records. The most frequent answer will be the
    predicted answer for that particular question.

    Example usage::

        predict_answer_vector({
            "E1": 1,
            "N1": 2,
            "A1": 3,
            "C1": 4,
            "O1": 5
        })

    :param answer_map:  The provided partially answered question. The map key is the question tag (E1 ~ O10) and value
    is the answer choice (1 ~ 5) for that question. This map only contains 5 kv pairs
    :return: a list of 50 numbers, each of which represents the most frequent choice among the 10 most similar record
    """
    training_data: list[dict[str, int]]= _load_training_data()
    most_similar_records: list[dict[str, int]] = _find_most_similar_records(answer_map, training_data)

    return _get_frequency_based_answer(most_similar_records)


def _load_training_data() -> list[dict[str, int]]:
    """
    Reads CSV (./data.csv), ONLY consumes columns from E1 ~ O10 and returns, without CSV header, a list with each
    element being a map whose key is question E1, E2, ..., O10 and value is the choice (converted to integer) selected
    for that question

    :return: question answers
    """
    with open('data.csv') as file:
        return [{k: int(v) for k, v in row.items() if k in QUESTIONS}
            for row in csv.DictReader(file, skipinitialspace=True, delimiter="\t")]


def _find_most_similar_records(answer_map: dict[str, int], training_data: list[dict[str, int]]) -> list[dict[str, int]]:
    """
    Given 5 questions with defined answers, each of which belongs to a set of [E, N, A, C, O], searches data.csv to
    find the top 10 most recent records.

    The similarity is calculated by modeling each record as vector of 5 elements, computing the difference pair-wise,
    and summing them up

    :param answer_map: a map of 5 pairs
    :param training_data: data.csv with only question columns

    :return: 10 most similar records
    """
    provided_questions = answer_map.keys()

    deviation_map: dict[int, int] = {}
    for idx, record in enumerate(training_data):
        deviation_score = 0
        for question in provided_questions:

            deviation_score += abs(int(record[question]) - int(answer_map[question]))
        deviation_map[idx] = deviation_score

    sorted_deviation_map = dict(sorted(deviation_map.items(), key=lambda item: item[1]))
    most_similar_records = []
    counter = 0
    for key, value in sorted_deviation_map.items():
        if counter < 10:
            counter = counter + 1
            most_similar_records.append(training_data[key])

    return most_similar_records


def _get_frequency_based_answer(most_similar_records: list[dict[str, int]]) -> list[int]:
    """
    Given 10 most similar records, calculates the most frequent choice of each question among them; the most frequent
    choice will be chosen to be the predicted answer to that un-presented question

    :param most_similar_records: a list of mapping from question to choice

    :return: a predicted and complete five-personality-test answer
    """
    frequency_based_answer = []

    for question in QUESTIONS:
        answers: list[int] = _extract_answers_by_question(question, most_similar_records)
        print(answers)
        most_frequent_choice = max(set(answers), key=answers.count)
        frequency_based_answer.append(most_frequent_choice)

    return frequency_based_answer


def _extract_answers_by_question(question: str, most_similar_records: list[dict[str, int]]) -> list[int]:
    """
    Returns the answer of a specific question from the list of most similar records found

    :param question: one question tag from [E1 ~ O10]
    :param most_similar_records: the list of complete answer sets to extract the target question answer from

    :return: a list of numbers each of which represents a choice of a particular column in data.csv
    """
    return [record[question] for record in most_similar_records]
