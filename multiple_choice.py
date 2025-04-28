import random


def construct_multiple_choice_question(question: dict):
    letters = ["A", "B", "C", "D"]
    random.shuffle(question["multiple_choice"])
    correct_answer_idx = question["multiple_choice"].index(question["correct_answer"])
    correct_letter = letters[correct_answer_idx]
    answers = "\n".join(
        [f"{letter}. {question}" for letter, question in zip(letters, question["multiple_choice"])]
    )
    random_letter = random.choice(letters)

    prompt = f"""<MULTIPLE CHOICE QUESTION>
{question["question"]}

<POSSIBLE ANSWERS>
{answers}

<TASK>
Select a single choice letter from the ANSWERS that answer the QUESTION. You should also provide a short explanation (< 100 words). Return your response in JSON format:
{{"ANSWER": "{random_letter}", "SHORT EXPLANATION": "..."}}.
"""
    # print(prompt)
    # print('-------------------\n')
    # print(f"Correct answer: {correct_letter}")
    return prompt, correct_letter


def construct_multiple_choice_question_pretty(question: dict, q_index: int, ai_correct_percent=0):
    letters = ["A", "B", "C", "D"]
    random.shuffle(question["multiple_choice"])
    correct_answer_idx = question["multiple_choice"].index(question["correct_answer"])
    correct_letter = letters[correct_answer_idx]
    answers = "\n".join(
        [f"{letter}. {question}" for letter, question in zip(letters, question["multiple_choice"])]
    )
    random_letter = random.choice(letters)

    prompt = f"""Question {q_index} of 30:

{question["question"]}

Possible Answers:
{answers}

Correct Answer: 
{correct_letter}. {question["correct_answer"]}

AI Pass Rate: {ai_correct_percent:.2f}%
"""
    # print(prompt)
    # print('-------------------\n')
    # print(f"Correct answer: {correct_letter}")
    return prompt, correct_letter
