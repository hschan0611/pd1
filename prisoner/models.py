# prisoner/models.py

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import numpy as np
import time

def calculate_rounds(num_matches, delta):
    # Calculate match duration, last rounds, and first rounds
    match_duration = np.random.geometric(p=(1 - delta), size=num_matches).astype(int)
    last_rounds = list(np.cumsum(match_duration))
    first_rounds = [1] + [int(last_rounds[k - 1] + 1) for k in range(1, len(match_duration))]
    last_round = last_rounds[-1] if last_rounds else 1  # Set last_round to at least 1
    return match_duration, last_rounds, first_rounds, last_round

class Constants(BaseConstants):
    name_in_url = 'prisoner'
    players_per_group = 2
    conversion_rate = 1 / 100  # $0.01 for every point scored in Dal Bo and Frechette AER 2011

    instructions_template = 'prisoner/instructions.html'
    time_limit = False
    time_limit_seconds = 3600  # time limit for session (in seconds)

    # Define payoffs for Game 1 and Game 2
    betray_payoff_1 = 50
    betrayed_payoff_1 = 12
    both_cooperate_payoff_1 = 48
    both_defect_payoff_1 = 25

    betray_payoff_2 = 98
    betrayed_payoff_2 = 21
    both_cooperate_payoff_2 = 49
    both_defect_payoff_2 = 42

    # Parameters for games
    delta = 0.75
    num_matches_game1 = 2
    num_matches_game2 = 2

    # Calculate rounds for each game separately
    match_duration_game1, last_rounds_game1, first_rounds_game1, last_round_game1 = calculate_rounds(num_matches_game1,
                                                                                                     delta)
    match_duration_game2, last_rounds_game2, first_rounds_game2, last_round_game2 = calculate_rounds(num_matches_game2,
                                                                                                     delta)

    # Total rounds
    num_rounds_game1 = int(np.sum(match_duration_game1))
    num_rounds_game2 = int(np.sum(match_duration_game2))
    num_rounds = num_rounds_game1 + num_rounds_game2


class Subsession(BaseSubsession):
    match_number = models.IntegerField()
    round_in_match_number = models.IntegerField()
    active_game = models.IntegerField(initial=1)  # Default to Game 1

    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['start_time'] = time.time()
            self.session.vars['alive'] = True

        # Set active_game based on round number
        if self.round_number <= Constants.num_rounds_game1:
            self.active_game = 1
            # Determine the match number within Game 1 rounds
            for k, last_round in enumerate(Constants.last_rounds_game1):
                if self.round_number <= last_round:
                    self.match_number = k + 1
                    break
            # Calculate the round within the current match
            self.round_in_match_number = (
                    self.round_number - Constants.first_rounds_game1[self.match_number - 1] + 1
            )
        else:
            self.active_game = 2
            game2_round_number = self.round_number - Constants.num_rounds_game1
            # Determine the match number within Game 2 rounds
            for k, last_round in enumerate(Constants.last_rounds_game2):
                if game2_round_number <= last_round:
                    self.match_number = k + 1
                    break
            # Calculate the round within the current match
            self.round_in_match_number = (
                    game2_round_number - Constants.first_rounds_game2[self.match_number - 1] + 1
            )

        # Randomly group players at the start of each match
        if (self.active_game == 1 and self.round_number in Constants.first_rounds_game1) or \
                (
                        self.active_game == 2 and self.round_number - Constants.num_rounds_game1 in Constants.first_rounds_game2):
            self.group_randomly()
        else:
            self.group_like_round(self.round_number - 1)

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    quiz_Q1_response = models.BooleanField(
        label="True/False: Referring to the payoff table, the first entry in each cell represents your payoff, while the second entry represents the payoff of the person you are matched with.",
        choices=[(True, 'True'), (False, 'False')],
        initial=None
    )
    quiz_Q1_correct = models.BooleanField()

    quiz_Q2_response = models.BooleanField(
        label="True/False: The length of a match depends on your actions.",
        choices=[(True, 'True'), (False, 'False')],
        initial=None
    )
    quiz_Q2_correct = models.BooleanField()

    quiz_Q3_response = models.IntegerField(
        label="If you choose Action 1 and the other person chooses Action 2, you will receive. . .",
        choices=[('48'), ('12'), ('25'), ('50')],
        widget=widgets.RadioSelect,
        initial=0
    )
    quiz_Q3_correct = models.BooleanField()

    quiz_Q4_response = models.StringField(
        label="If you have already played 2 rounds, the probability that there will be another round in your supergame is...",
        choices=[
            ('0%', '0%'),
            ('25%', '25%'),
            ('75%', '75%'),
            ('100%', '100%')
        ],
        widget=widgets.RadioSelect,
        initial=None
    )
    quiz_Q4_correct = models.BooleanField()

    # Fields specific to the prisoner app
    decision = models.StringField(
        choices=['Action 1', 'Action 2'],
        doc="This player's decision",
        widget=widgets.RadioSelect
    )

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):
        # Determine which game's payoff matrix to use
        if self.subsession.active_game == 1:
            # Payoff matrix for Game 1
            payoff_matrix = {
                'Action 1': {
                    'Action 1': Constants.both_cooperate_payoff_1,
                    'Action 2': Constants.betrayed_payoff_1
                },
                'Action 2': {
                    'Action 1': Constants.betray_payoff_1,
                    'Action 2': Constants.both_defect_payoff_1
                }
            }
        else:
            # Payoff matrix for Game 2
            payoff_matrix = {
                'Action 1': {
                    'Action 1': Constants.both_cooperate_payoff_2,
                    'Action 2': Constants.betrayed_payoff_2
                },
                'Action 2': {
                    'Action 1': Constants.betray_payoff_2,
                    'Action 2': Constants.both_defect_payoff_2
                }
            }

        # Set the player's payoff based on the selected matrix
        self.payoff = payoff_matrix[self.decision][self.other_player().decision]