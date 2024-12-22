# combined_sequence.py

from Quiz import QuizInstructions, Q1, Q1Result, Q2, Q2Result, Q3, Q3Result, Q4, Q4Result, WaitQuiz
from prisoner.pages import Instructions_1, Instructions_2, Instructions_3, Decision, ResultsWaitPage, Results, EndRound, End

page_sequence = [
    Instructions_1,
    Instructions_2,
    Instructions_3,
    QuizInstructions,
    Q1, Q1Result,
    Q2, Q2Result,
    Q3, Q3Result,
    Q4, Q4Result,
    WaitQuiz,
    Decision,
    ResultsWaitPage,
    Results,
    EndRound,
    End
]
