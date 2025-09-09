# prisoner/models.py
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import time, random, itertools
# (You can delete numpy/calculate_rounds if you’re no longer using random lengths)

# ---- helper moved OUTSIDE the class ----
def bounds_from_durations(durations):
    """
    Given a list of supergame lengths (durations), return:
      last_rounds: cumulative ends of each supergame (1-indexed)
      first_rounds: starting indices of each supergame (1, last_prev+1, ...)
      last_round: last round index within the game (== last_rounds[-1])
    """
    last = list(itertools.accumulate(durations))
    first = [1] + [x + 1 for x in last[:-1]]
    return last, first, last[-1]


class Constants(BaseConstants):
    name_in_url = 'prisoner'
    players_per_group = 2
    instructions_template = 'prisoner/instructions.html'
    time_limit = False
    time_limit_seconds = 5400

    # PD payoffs
    betray_payoff_1 = 50
    betrayed_payoff_1 = 12
    both_cooperate_payoff_1 = 48
    both_defect_payoff_1 = 25

    betray_payoff_2 = 50
    betrayed_payoff_2 = 12
    both_cooperate_payoff_2 = 32
    both_defect_payoff_2 = 25

    # (delta still used in your instruction text, but not for lengths now)
    delta = 0.75

    # -------- Fixed supergame structure: each game sums to 48 rounds --------
    num_matches_game1 = 12
    match_duration_game1 = [4, 5, 3, 2, 4, 3, 5, 4, 2, 6, 5, 5]  # sum = 48
    last_rounds_game1, first_rounds_game1, last_round_game1 = bounds_from_durations(match_duration_game1)
    num_rounds_game1 = sum(match_duration_game1)  # 48

    num_matches_game2 = 12
    match_duration_game2 = [3, 4, 5, 2, 4, 6, 3, 4, 3, 5, 4, 5]  # sum = 48
    last_rounds_game2, first_rounds_game2, last_round_game2 = bounds_from_durations(match_duration_game2)
    num_rounds_game2 = sum(match_duration_game2)  # 48

    # Total rounds across both games
    num_rounds = num_rounds_game1 + num_rounds_game2  # 96

    # --- BRET constants ---
    bret_num_boxes  = 100        # 1 bomb among 100 boxes
    bret_max_points = 16         # TOTAL possible points if no bomb and k=100
    bret_pay_if_hit = 0          # payoff if the chosen set includes the bomb


class Subsession(BaseSubsession):
    match_number = models.IntegerField()
    round_in_match_number = models.IntegerField()
    active_game = models.IntegerField(initial=1)

    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['start_time'] = time.time()
            self.session.vars['alive'] = True

        # initialize the demographics flag for every participant
        for p in self.get_players():
            p.participant.vars['demographics_done'] = False

        # Determine active game and in-match counters
        if self.round_number <= Constants.num_rounds_game1:
            self.active_game = 1
            for k, last_round in enumerate(Constants.last_rounds_game1):
                if self.round_number <= int(last_round):
                    self.match_number = k + 1
                    break
            first = Constants.first_rounds_game1[self.match_number - 1]
            self.round_in_match_number = int(self.round_number - int(first) + 1)
        else:
            self.active_game = 2
            game2_round = self.round_number - Constants.num_rounds_game1
            for k, last_round in enumerate(Constants.last_rounds_game2):
                if game2_round <= int(last_round):
                    self.match_number = k + 1
                    break
            first = Constants.first_rounds_game2[self.match_number - 1]
            self.round_in_match_number = int(game2_round - int(first) + 1)

        # Grouping
        if (self.active_game == 1 and self.round_number in Constants.first_rounds_game1) or \
           (self.active_game == 2 and self.round_number - Constants.num_rounds_game1 in Constants.first_rounds_game2):
            self.group_randomly()
        else:
            self.group_like_round(self.round_number - 1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # --- Quiz fields (unchanged) ---
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
        label="If you choose Action 1 and the other person chooses Action 2 in Game 1, you will receive...",
        choices=[48, 12, 25, 50],
        widget=widgets.RadioSelect
    )
    quiz_Q3_correct = models.BooleanField()

    quiz_Q4_response = models.StringField(
        label="If you have already played 2 rounds, the probability that there will be another round in your match is...",
        choices=['0%', '25%', '75%', '100%'],
        widget=widgets.RadioSelect
    )
    quiz_Q4_correct = models.BooleanField()

    # --- Belief task ---
    belief = models.IntegerField(min=0, max=100, label="Probability (0-100) that the other player will choose Action 1?", initial=50)
    belief_interacted = models.BooleanField(initial=False)
    belief_asked = models.BooleanField(initial=False)
    belief_draw1 = models.IntegerField(initial=None)
    belief_draw2 = models.IntegerField(initial=None)
    belief_prize = models.IntegerField(initial=0)  # 0 or 8

    # --- PD decision/points ---
    decision = models.StringField(choices=['Action 1', 'Action 2'], widget=widgets.RadioSelect)
    stage_points = models.IntegerField(initial=0)

    def other_player(self):
        return self.get_others_in_group()[0]

    # --- Demographics (unchanged) ---
    age = models.IntegerField(label="Age (enter a whole number)", min=18, max=120)
    gender = models.StringField(
        label="Gender",
        choices=["Woman","Man","Non-binary / third gender","Self-describe","Prefer not to say"],
        widget=widgets.RadioSelect
    )
    gender_self_describe = models.StringField(label="If you selected “Self-describe”, please specify", blank=True)
    education = models.StringField(
        label="Highest level of education completed",
        choices=["High school or less","Some college","Bachelor’s degree","Master’s degree","Doctorate","Other","Prefer not to say"],
        widget=widgets.RadioSelect
    )
    education_other = models.StringField(label="If you selected “Other”, please specify", blank=True)
    econ_courses = models.StringField(
        label="How many college-level economics courses have you taken?",
        choices=["None","One","Two or more","Prefer not to say"],
        widget=widgets.RadioSelect
    )
    native_english = models.BooleanField(label="Are you a native English speaker?", choices=[(True,"Yes"),(False,"No")])

    # --- Payoff logic ---
    def set_payoff(self):
        if self.subsession.active_game == 1:
            payoff_matrix = {
                'Action 1': {'Action 1': Constants.both_cooperate_payoff_1, 'Action 2': Constants.betrayed_payoff_1},
                'Action 2': {'Action 1': Constants.betray_payoff_1,        'Action 2': Constants.both_defect_payoff_1},
            }
        else:
            payoff_matrix = {
                'Action 1': {'Action 1': Constants.both_cooperate_payoff_2, 'Action 2': Constants.betrayed_payoff_2},
                'Action 2': {'Action 1': Constants.betray_payoff_2,        'Action 2': Constants.both_defect_payoff_2},
            }

        base_points = payoff_matrix[self.decision][self.other_player().decision]
        self.stage_points = base_points

        prize_points = 0
        if self.belief_asked:
            r1 = random.randint(0, 100)
            r2 = random.randint(0, 100)
            self.belief_draw1 = r1
            self.belief_draw2 = r2
            # pay 8 if opponent chose Action 1 and belief > at least one draw
            if self.other_player().decision == 'Action 1' and (self.belief > r1 or self.belief > r2):
                prize_points = 8
        self.belief_prize = prize_points

        self.payoff = base_points + prize_points

    # --- BRET fields & payoff ---
    bret_boxes    = models.IntegerField(min=0, max=Constants.bret_num_boxes, initial=0)
    bret_bomb_box = models.IntegerField()
    bret_hit      = models.BooleanField(initial=False)
    bret_points   = models.IntegerField(initial=0)

    def draw_bomb_and_set_bret_payoff(self):
        """Total BRET points are in [0,16]. Each box is worth ~0.16 points if no bomb."""
        self.bret_bomb_box = random.randint(1, Constants.bret_num_boxes)

        k = self.bret_boxes or 0
        self.bret_hit = (k >= self.bret_bomb_box and k > 0)

        if self.bret_hit:
            self.bret_points = Constants.bret_pay_if_hit
        else:
            # scale: k/100 of the 16-point cap
            self.bret_points = int(round(k * Constants.bret_max_points / Constants.bret_num_boxes))

        self.participant.vars['bret_points'] = int(self.bret_points)
