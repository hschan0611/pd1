# prisoner/models.py
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import time, random, itertools
import numpy as np

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

def calculate_rounds(num_matches, delta):
    """
    Calculate match duration, last rounds, and first rounds based on delta.
    Each supergame length follows a geometric distribution.
    """
    match_duration = np.random.geometric(p=(1 - delta), size=num_matches).astype(int)  # NumPy int64 array
    match_duration = [int(rounds) for rounds in match_duration]  # Convert to Python int list

    last_rounds = list(np.cumsum(match_duration))  # Cumulative sum of match durations
    first_rounds = [1] + [last_rounds[k - 1] + 1 for k in range(1, len(match_duration))]

    last_round = last_rounds[-1] if last_rounds else 1  # Ensure last round is at least 1
    return match_duration, last_rounds, first_rounds, last_round


class Constants(BaseConstants):
    name_in_url = 'prisoner'
    players_per_group = 2
    instructions_template = 'prisoner/instructions.html'
    time_limit = False
    time_limit_seconds = 5400

    # PD payoffs
    betray_payoff_1 = 50
    betrayed_payoff_1 = 12
    both_cooperate_payoff_1 = 32
    both_defect_payoff_1 = 25

    betray_payoff_2 = 50
    betrayed_payoff_2 = 12
    both_cooperate_payoff_2 = 48
    both_defect_payoff_2 = 25

    # (delta still used in your instruction text, but not for lengths now)
    delta = 0.75

    # -------- Fixed supergame structure: each game sums to 48 rounds --------
    num_matches_game1 = 10
    match_duration_game1 = [3, 5, 4, 1, 2, 7, 6, 4, 4, 4]  # sum = 40
    last_rounds_game1, first_rounds_game1, last_round_game1 = bounds_from_durations(match_duration_game1)
    num_rounds_game1 = sum(match_duration_game1)  # 48

    num_matches_game2 = 10
    match_duration_game2 = [3, 5, 4, 1, 2, 7, 6, 4, 4, 4]  # sum = 40
    last_rounds_game2, first_rounds_game2, last_round_game2 = bounds_from_durations(match_duration_game2)
    num_rounds_game2 = sum(match_duration_game2)  # 48

    # Total rounds across both games
    num_rounds = num_rounds_game1 + num_rounds_game2  # 96

    # --- BRET constants ---
    bret_rows = 10
    bret_cols = 10
    bret_num_boxes = bret_rows * bret_cols  # 100 boxes
    bret_interval_sec = 2  # every 2 seconds a box is collected
    bret_points_per_box = 1  # 1 point per collected box
    bret_pay_if_hit = 0  # payoff = 0 if bomb collected


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
    quiz_Q1_response = models.BooleanField(
        label="True/False: Referring to the payoff table, the first entry in each cell represents your payoff, while the second entry represents the payoff of the person you are matched with.",
        choices=[(True, 'True'), (False, 'False')],
        initial=None
    )
    quiz_Q1_correct = models.BooleanField()

    quiz_Q2_response = models.BooleanField(
        label="True/False: You will play with the same participant for the entire session.",
        choices=[(True, 'True'), (False, 'False')],
        initial=None
    )
    quiz_Q2_correct = models.BooleanField()

    quiz_Q3_response = models.IntegerField(
        label="If you choose Action 1 and the other person chooses Action 2, you will receive...",
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

    belief_quiz = models.StringField(
        label='If your slider shows 75% as above, what does that mean? ',
        choices=[
            ('all_75', 'You believe that 75% of all participants chose Action 1.'),
            ('paired_75', 'You believe that the person you are paired with has a 75% chance of choosing Action 1.'),
            ('paired_25', 'You believe that the person you are paired with has a 75% chance of choosing Action 2.'),
            ('75_points', 'You believe that you will receive 75 points.'),
        ],
        widget=widgets.RadioSelect
    )
    belief_quiz_correct = models.BooleanField(initial=False)

    # --- Belief task ---
    belief = models.IntegerField(
        min=0, max=100,
        label="Probability (0-100) that the other player will choose Action 1?",
    )
    belief_interacted = models.BooleanField(initial=False)
    belief_asked = models.BooleanField(initial=False)
    belief_draw1 = models.IntegerField(initial=None)
    belief_draw2 = models.IntegerField(initial=None)
    belief_prize = models.IntegerField(initial=0)


    # --- PD decision/points ---
    decision = models.StringField(choices=['Action 1', 'Action 2'], widget=widgets.RadioSelect)
    stage_points = models.IntegerField(initial=0)

    def other_player(self):
        return self.get_others_in_group()[0]

    # --- Demographics  ---
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
                prize_points = 50
        self.belief_prize = prize_points

        self.payoff = base_points + prize_points

    bret_bomb_box = models.IntegerField(initial=0)
    bret_started = models.BooleanField(initial=False)
    bret_stopped = models.BooleanField(initial=False)
    bret_start_time = models.FloatField(initial=0)
    bret_stop_time = models.FloatField(initial=0)
    bret_collected_count = models.IntegerField(initial=0)
    bret_hit = models.BooleanField(initial=False)
    bret_points = models.IntegerField(initial=0)

    def bret_start(self):
        """Called when participant presses Start."""
        if not self.bret_bomb_box:
            self.bret_bomb_box = random.randint(1, Constants.bret_num_boxes)
        self.bret_started = True
        self.bret_stopped = False
        self.bret_start_time = time.time()
        self.bret_stop_time = 0
        self.bret_collected_count = 0
        self.bret_hit = False
        self.bret_points = 0

    def bret_compute_collected(self, now: float = None) -> int:
        """Compute how many boxes would be collected at given time."""
        if not self.bret_started or self.bret_start_time <= 0:
            return 0
        if now is None:
            now = time.time()
        elapsed = max(0.0, now - self.bret_start_time)
        # Box #1 collected immediately at t=0
        count = int(elapsed // Constants.bret_interval_sec) + 1
        return min(Constants.bret_num_boxes, max(0, count))

    def bret_stop_and_score(self):
        """Called when participant presses Stop."""
        if not self.bret_started:
            self.bret_start()

        self.bret_stop_time = time.time()
        self.bret_stopped = True

        # freeze count
        final_count = self.bret_compute_collected(now=self.bret_stop_time)
        self.bret_collected_count = final_count

        # bomb check
        self.bret_hit = (self.bret_bomb_box <= final_count and final_count > 0)

        if self.bret_hit:
            self.bret_points = Constants.bret_pay_if_hit
        else:
            self.bret_points = final_count * Constants.bret_points_per_box

        self.participant.vars['bret_points'] = int(self.bret_points)


    crt_q1 = models.FloatField(
        label="A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost (in cents)?"
    )
    crt_q1_correct = models.BooleanField(initial=False)

    crt_q2 = models.FloatField(
        label="If it takes 4 machines 4 minutes to make 4 widgets, how many minutes would it take 80 machines to make 80 widgets?"
    )
    crt_q2_correct = models.BooleanField(initial=False)

    crt_q3 = models.FloatField(
        label="In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 36 days for the patch to cover the entire lake, how many days would it take to cover half of the lake?"
    )
    crt_q3_correct = models.BooleanField(initial=False)
