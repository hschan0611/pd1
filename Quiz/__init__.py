from otree.api import *

class Constants(BaseConstants):
    name_in_url = 'quiz_with_explanation'
    players_per_group = None
    num_rounds = 1
    true_false_choices = [(1, 'True'), (0, 'False')]

def get_quiz_data():
    return [
        dict(
            name='Q1',
            solution=True,
            explanation="The first entry in each cell represents your payoff, while the second entry represents the payoff of the person you are matched with.",
        ),
        dict(
            name='Q2',
            solution=False,
            explanation="Once a match ends, you will be randomly paired with another person for a new match",
        ),
        dict(
            name='Q3',
            solution=12,
            explanation="In the payoff table, the top-right cell shows your payoff as the first entry, which is 12.",
        ),
        dict(
            name='Q4',
            solution='75%',
            explanation="After each round, there is a 75% probability that the match will continue for at least another round.",
        ),
    ]

class Instructions(Page):
    def is_displayed(self):
        # Display only in the first round
        return self.round_number == 1

class Q1(Page):
    form_model = 'player'
    form_fields = ['quiz_Q1_response']

    def is_displayed(self):
        # Display only in the first round
        return self.round_number == 1

    def vars_for_template(self):
        fields = get_quiz_data()
        return {
            'question': fields[0],
        }

    def before_next_page(self):
        # Safely retrieve the player's answer
        player_answer = self.player.field_maybe_none('quiz_Q1_response')
        fields = get_quiz_data()

        # Check if the player's answer matches the correct solution
        self.player.quiz_Q1_correct = (player_answer == fields[0]['solution']) if player_answer is not None else False

        # Debugging output
        print(f"Q1 - Player's answer: {player_answer}, Correct answer: {fields[0]['solution']}")
        print(f"Q1 - Is player's answer correct? {self.player.quiz_Q1_correct}")


class Q1Result(Page):
    form_model = 'player'
    form_fields = ['quiz_Q1_response']

    def is_displayed(self):
        # Display only in the first round
        return self.round_number == 1

    def vars_for_template(self):
        fields = get_quiz_data()
        print("Debug: Passing show_solutions and Q1 to template")
        return {
            'show_solutions': True,
            'Q1': fields[0],
        }

class Q2(Page):
    form_model = 'player'
    form_fields = ['quiz_Q2_response']

    def is_displayed(self):
        # Display only in the first round
        return self.round_number == 1

    def vars_for_template(self):
        fields = get_quiz_data()
        return {
            'question': fields[1],
        }

    def before_next_page(self):
        # Safely retrieve the player's answer
        player_answer = self.player.field_maybe_none('quiz_Q2_response')
        fields = get_quiz_data()

        # Check if the player's answer matches the correct solution
        self.player.quiz_Q2_correct = (player_answer == fields[1]['solution']) if player_answer is not None else False

class Q2Result(Page):
    form_model = 'player'
    form_fields = ['quiz_Q2_response']

    def is_displayed(self):
        # Display only in the first round
        return self.round_number == 1

    def vars_for_template(self):
        fields = get_quiz_data()
        return {
            'show_solutions': True,
            'Q2': fields[1],
        }

class Q3(Page):
    form_model = 'player'
    form_fields = ['quiz_Q3_response']

    def is_displayed(self):
        # Display only in the first round
        return self.round_number == 1

    def vars_for_template(self):
        fields = get_quiz_data()
        return {
            'question': fields[2],
        }

    def before_next_page(self):
        # Safely retrieve the player's answer
        player_answer = self.player.field_maybe_none('quiz_Q3_response')
        fields = get_quiz_data()

        # Check if the player's answer matches the correct solution
        self.player.quiz_Q3_correct = (player_answer == fields[2]['solution']) if player_answer is not None else False

class Q3Result(Page):
    form_model = 'player'
    form_fields = ['quiz_Q3_response']

    def is_displayed(self):
        # Display only in the first round
        return self.round_number == 1

    def vars_for_template(self):
        fields = get_quiz_data()
        return {
            'show_solutions': True,
            'Q3': fields[2],
        }

class Q4(Page):
    form_model = 'player'
    form_fields = ['quiz_Q4_response']

    def is_displayed(self):
        # Display only in the first round
        return self.round_number == 1

    def vars_for_template(self):
        fields = get_quiz_data()
        return {
            'question': fields[3],
        }

    def before_next_page(self):
        # Safely retrieve the player's answer
        player_answer = self.player.field_maybe_none('quiz_Q4_response')
        fields = get_quiz_data()

        # Check if the player's answer matches the correct solution
        self.player.quiz_Q4_correct = (player_answer == fields[3]['solution']) if player_answer is not None else False

class Q4Result(Page):
    form_model = 'player'
    form_fields = ['quiz_Q4_response']

    def is_displayed(self):
        # Display only in the first round
        return self.round_number == 1

    def vars_for_template(self):
        fields = get_quiz_data()
        return {
            'show_solutions': True,
            'Q4': fields[3],
        }

class WaitQuiz(WaitPage):
    wait_for_all_groups = True
