# prisoner/pages.py

from Quiz import Instructions, Q1, Q1Result, Q2, Q2Result, Q3, Q3Result, Q4, Q4Result
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random
import time

from .models import Constants
from otree.api import Page, WaitPage
import random
import time

class Instructions_1(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

class Instructions_2(Page):
    def vars_for_template(self):
        continuation_chance = int(round(Constants.delta * 100))
        return dict(continuation_chance=continuation_chance, die_threshold_plus_one=continuation_chance + 1)

    def is_displayed(self):
        return self.subsession.round_number == 1

class Instructions_3(Page):
    def vars_for_template(self):
        continuation_chance = int(round(Constants.delta * 100))
        return dict(continuation_chance=continuation_chance, die_threshold_plus_one=continuation_chance + 1)

    def is_displayed(self):
        return self.subsession.round_number == 1

class Instructions_4(Page):
    def vars_for_template(self):
        continuation_chance = int(round(Constants.delta * 100))
        return dict(continuation_chance=continuation_chance, die_threshold_plus_one=continuation_chance + 1)

    def is_displayed(self):
        return self.subsession.round_number == 1

class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    def is_displayed(self):
        # Display only in rounds that correspond to the active game
        if self.subsession.active_game == 1:
            return self.round_number <= Constants.num_rounds_game1
        else:
            return Constants.num_rounds_game1 < self.round_number <= Constants.num_rounds_game1 + Constants.num_rounds_game2


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()

    def is_displayed(self):
        # Display only in rounds that correspond to the active game
        if self.subsession.active_game == 1:
            return self.round_number <= Constants.num_rounds_game1
        else:
            return Constants.num_rounds_game1 < self.round_number <= Constants.num_rounds_game1 + Constants.num_rounds_game2


class Results(Page):
    def vars_for_template(self):
        # Choose the appropriate payoffs based on the active game
        if self.subsession.active_game == 1:
            both_cooperate_payoff = Constants.both_cooperate_payoff_1
            betray_payoff = Constants.betray_payoff_1
            both_defect_payoff = Constants.both_defect_payoff_1
            betrayed_payoff = Constants.betrayed_payoff_1
        else:
            both_cooperate_payoff = Constants.both_cooperate_payoff_2
            betray_payoff = Constants.betray_payoff_2
            both_defect_payoff = Constants.both_defect_payoff_2
            betrayed_payoff = Constants.betrayed_payoff_2

        return {
            'both_cooperate_payoff': both_cooperate_payoff,
            'betray_payoff': betray_payoff,
            'both_defect_payoff': both_defect_payoff,
            'betrayed_payoff': betrayed_payoff,
            'my_decision': self.player.decision,
            'opponent_decision': self.player.other_player().decision,
            'same_choice': self.player.decision == self.player.other_player().decision,
            'both_cooperate': self.player.decision == "Action 1" and self.player.other_player().decision == "Action 1",
            'both_defect': self.player.decision == "Action 2" and self.player.other_player().decision == "Action 2",
            'i_cooperate_he_defects': self.player.decision == "Action 1" and self.player.other_player().decision == "Action 2",
            'i_defect_he_cooperates': self.player.decision == "Action 2" and self.player.other_player().decision == "Action 1",
        }

    def is_displayed(self):
        # Display only in rounds that correspond to the active game
        if self.subsession.active_game == 1:
            return self.round_number <= Constants.num_rounds_game1
        else:
            return Constants.num_rounds_game1 < self.round_number <= Constants.num_rounds_game1 + Constants.num_rounds_game2


class EndRound(Page):
    timeout_seconds = 100

    def vars_for_template(self):
        continuation_chance = int(round(Constants.delta * 100))

        # Determine which game's last rounds to use based on active_game
        if self.subsession.active_game == 1:
            last_rounds = Constants.last_rounds_game1
        else:
            last_rounds = [r + Constants.num_rounds_game1 for r in Constants.last_rounds_game2]

        # Check if the current round is the last round in the match for the active game
        is_last_round = self.subsession.round_number in last_rounds

        # Set the die roll outcome based on whether it’s the last round
        if is_last_round:
            dieroll = random.randint(continuation_chance + 1, 100)  # End the match
        else:
            dieroll = random.randint(1, continuation_chance)  # Continue to next round

        return {
            'dieroll': dieroll,
            'continuation_chance': continuation_chance,
            'die_threshold_plus_one': continuation_chance + 1,
            'is_last_round': is_last_round
        }

    def is_displayed(self):
        # Display only in rounds that correspond to the active game
        if self.subsession.active_game == 1:
            return self.round_number <= Constants.num_rounds_game1
        else:
            return Constants.num_rounds_game1 < self.round_number <= Constants.num_rounds_game1 + Constants.num_rounds_game2


class End(Page):
    def is_displayed(self):
        # Calculate the overall last round in the entire experiment
        total_last_round = Constants.num_rounds_game1 + Constants.num_rounds_game2

        # Display the End page if the session has ended (either time-based or last round)
        return self.session.vars.get('alive', True) == False or self.subsession.round_number == total_last_round

    def vars_for_template(self):
        # Calculate the overall last round in the entire experiment
        total_last_round = Constants.num_rounds_game1 + Constants.num_rounds_game2
        return {
            'total_last_round': total_last_round,
            'num_matches': Constants.num_matches_game1 + Constants.num_matches_game2
        }

class Game1Intro(Page):
    def is_displayed(self):
        # Show this page only once at the start of Game 1
        return self.round_number == 1

class DecisionGame1(Page):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(self):
        return {
            'game_number': 1,
            'match_number': self.subsession.match_number,
            'round_number': self.subsession.round_in_match_number,
        }

    def is_displayed(self):
        # Show only in Game 1 matches
        return self.round_number <= Constants.num_rounds_game1

class ResultsWaitPageGame1(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()

    def is_displayed(self):
        return self.round_number <= Constants.num_rounds_game1

class ResultsGame1(Page):
    def vars_for_template(self):
        other_player = self.player.other_player()

        return {
            'both_cooperate_payoff': Constants.both_cooperate_payoff_1,
            'betray_payoff': Constants.betray_payoff_1,
            'both_defect_payoff': Constants.both_defect_payoff_1,
            'betrayed_payoff': Constants.betrayed_payoff_1,
            'my_decision': self.player.decision,
            'opponent_decision': other_player.decision,
            'same_choice': self.player.decision == other_player.decision,
            'both_cooperate': self.player.decision == "Action 1" and other_player.decision == "Action 1",
            'both_defect': self.player.decision == "Action 2" and other_player.decision == "Action 2",
            'i_cooperate_he_defects': self.player.decision == "Action 1" and other_player.decision == "Action 2",
            'i_defect_he_cooperates': self.player.decision == "Action 2" and other_player.decision == "Action 1",
            'game_number': 1,
            'match_number': self.subsession.match_number,
            'round_number': self.subsession.round_in_match_number,
        }

    def is_displayed(self):
        return self.round_number <= Constants.num_rounds_game1


class EndRoundGame1(Page):
    def vars_for_template(self):
        continuation_chance = int(round(Constants.delta * 100))

        # Check if the current round is the last round in Game 1
        is_last_round = self.round_number in Constants.last_rounds_game1

        # Set the die roll outcome based on whether it’s the last round
        if is_last_round:
            dieroll = random.randint(continuation_chance + 1, 100)  # End the match
        else:
            dieroll = random.randint(1, continuation_chance)  # Continue to next round

        return {
            'dieroll': dieroll,
            'continuation_chance': continuation_chance,
            'die_threshold_plus_one': continuation_chance + 1,
            'is_last_round': is_last_round,
            'match_number': self.subsession.match_number,  # Display match number
        }

    def is_displayed(self):
        return self.round_number <= Constants.num_rounds_game1


class Game2Intro(Page):
    def is_displayed(self):
        # Show this page only once, at the start of Game 2
        return self.round_number == Constants.num_rounds_game1 + 1

class DecisionGame2(Page):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(self):
        return {
            'game_number': 2,
            'match_number': self.subsession.match_number,
            'round_number': self.subsession.round_in_match_number,
        }

    def is_displayed(self):
        # Show only in Game 2 matches
        return Constants.num_rounds_game1 < self.round_number <= Constants.num_rounds_game1 + Constants.num_rounds_game2

class ResultsWaitPageGame2(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()

    def is_displayed(self):
        return Constants.num_rounds_game1 < self.round_number <= Constants.num_rounds_game1 + Constants.num_rounds_game2

class ResultsGame2(Page):
    def vars_for_template(self):
        other_player = self.player.other_player()

        return {
            'both_cooperate_payoff': Constants.both_cooperate_payoff_2,
            'betray_payoff': Constants.betray_payoff_2,
            'both_defect_payoff': Constants.both_defect_payoff_2,
            'betrayed_payoff': Constants.betrayed_payoff_2,
            'my_decision': self.player.decision,
            'opponent_decision': other_player.decision,
            'same_choice': self.player.decision == other_player.decision,
            'both_cooperate': self.player.decision == "Action 1" and other_player.decision == "Action 1",
            'both_defect': self.player.decision == "Action 2" and other_player.decision == "Action 2",
            'i_cooperate_he_defects': self.player.decision == "Action 1" and other_player.decision == "Action 2",
            'i_defect_he_cooperates': self.player.decision == "Action 2" and other_player.decision == "Action 1",
            'game_number': 2,
            'match_number': self.subsession.match_number,
            'round_number': self.subsession.round_in_match_number,
        }


    def is_displayed(self):
        return Constants.num_rounds_game1 < self.round_number <= Constants.num_rounds_game1 + Constants.num_rounds_game2

class EndRoundGame2(Page):
    def vars_for_template(self):
        continuation_chance = int(round(Constants.delta * 100))

        # Adjust the last round based on Game 2’s configuration
        is_last_round = self.round_number in [
            r + Constants.num_rounds_game1 for r in Constants.last_rounds_game2
        ]

        # Set the die roll outcome based on whether it’s the last round
        if is_last_round:
            dieroll = random.randint(continuation_chance + 1, 100)  # End the match
        else:
            dieroll = random.randint(1, continuation_chance)  # Continue to next round

        return {
            'dieroll': dieroll,
            'continuation_chance': continuation_chance,
            'die_threshold_plus_one': continuation_chance + 1,
            'is_last_round': is_last_round,
            'match_number': self.subsession.match_number,  # Display match number
        }

    def is_displayed(self):
        return Constants.num_rounds_game1 < self.round_number <= Constants.num_rounds_game1 + Constants.num_rounds_game2


class End(Page):
    def is_displayed(self):
        # Calculate the overall last round in the entire experiment (sum of rounds in both games)
        total_last_round = Constants.num_rounds_game1 + Constants.num_rounds_game2
        # Display the End page only after the last round of Game 2
        return self.round_number == total_last_round

    def vars_for_template(self):
        # Calculate the total number of matches
        total_matches = Constants.num_matches_game1 + Constants.num_matches_game2
        # Get the cumulative payoff for both games
        total_payoff = sum([p.payoff for p in self.player.in_all_rounds()])
        return {
            'total_payoff': total_payoff.to_real_world_currency(self.session),
            'total_matches': total_matches,
        }


page_sequence = [
    # Instructions and Quiz
    Instructions_1,
    Instructions_2,
    Instructions_4,
    Instructions,
    Q1, Q1Result,
    Q2, Q2Result,
    Q3, Q3Result,
    Q4, Q4Result,
    Instructions_3,

    # Game 1 Pages
    Game1Intro,
    DecisionGame1, ResultsWaitPageGame1, ResultsGame1, EndRoundGame1,

    # Game 2 Intro and Pages
    Game2Intro,
    DecisionGame2, ResultsWaitPageGame2, ResultsGame2, EndRoundGame2,

    # End page
    End
]
