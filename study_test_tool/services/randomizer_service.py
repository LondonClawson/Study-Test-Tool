"""Randomization service for shuffling questions and options."""

import copy
import random
from typing import List

from models.question import Question


class RandomizerService:
    """Provides shuffling for questions and their options."""

    @staticmethod
    def shuffle_questions(questions: List[Question]) -> List[Question]:
        """Return a new list of questions in random order.

        Does not mutate the original list.
        """
        shuffled = list(questions)
        random.shuffle(shuffled)
        return shuffled

    @staticmethod
    def shuffle_options(question: Question) -> Question:
        """Return a deep copy of the question with shuffled options.

        Does not mutate the original question.
        """
        new_question = copy.deepcopy(question)
        random.shuffle(new_question.options)
        return new_question

    @staticmethod
    def shuffle_all(questions: List[Question]) -> List[Question]:
        """Shuffle question order and option order within each question.

        Returns new objects; originals are not mutated.
        """
        shuffled = RandomizerService.shuffle_questions(questions)
        return [RandomizerService.shuffle_options(q) for q in shuffled]
