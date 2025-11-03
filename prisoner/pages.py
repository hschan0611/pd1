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

# Last round of the whole experiment (Game 1 + Game 2)
FINAL_ROUND = Constants.num_rounds_game1 + Constants.num_rounds_game2


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


class Game1Intro(Page):
    def is_displayed(self):
        # Show this page only once at the start of Game 1
        return self.round_number == 1

    def vars_for_template(self):
        """
        Add the payoff matrix for Game 1 so it can be displayed in the template.
        """
        return {
            'both_cooperate_payoff': Constants.both_cooperate_payoff_1,
            'betray_payoff': Constants.betray_payoff_1,
            'both_defect_payoff': Constants.both_defect_payoff_1,
            'betrayed_payoff': Constants.betrayed_payoff_1
        }


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
        other = self.player.other_player()

        # Safety net: compute if not done yet
        if (self.player.decision is not None and other.decision is not None
            and self.player.stage_points == 0 and self.player.payoff == 0):
            self.player.set_payoff()

        return dict(
            both_cooperate_payoff = Constants.both_cooperate_payoff_1,
            betray_payoff         = Constants.betray_payoff_1,
            both_defect_payoff    = Constants.both_defect_payoff_1,
            betrayed_payoff       = Constants.betrayed_payoff_1,
            my_decision           = self.player.decision,
            opponent_decision     = other.decision,
            same_choice           = self.player.decision == other.decision,
            both_cooperate        = self.player.decision == "Action 1" and other.decision == "Action 1",
            both_defect           = self.player.decision == "Action 2" and other.decision == "Action 2",
            i_cooperate_he_defects= self.player.decision == "Action 1" and other.decision == "Action 2",
            i_defect_he_cooperates= self.player.decision == "Action 2" and other.decision == "Action 1",

            # Show ONLY PD points on Results page:
            round_stage_points    = self.player.stage_points,
            # (optional) round_total_points = self.player.payoff,
        )


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
        # Show this page only once at the start of Game 2
        return self.round_number == Constants.num_rounds_game1 + 1

    def vars_for_template(self):
        """
        Add the payoff matrix for Game 2 so it can be displayed in the template.
        """
        return {
            'both_cooperate_payoff': Constants.both_cooperate_payoff_2,
            'betray_payoff': Constants.betray_payoff_2,
            'both_defect_payoff': Constants.both_defect_payoff_2,
            'betrayed_payoff': Constants.betrayed_payoff_2
        }


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
        other = self.player.other_player()

        if (self.player.decision is not None and other.decision is not None
            and self.player.stage_points == 0 and self.player.payoff == 0):
            self.player.set_payoff()

        return dict(
            both_cooperate_payoff = Constants.both_cooperate_payoff_2,
            betray_payoff         = Constants.betray_payoff_2,
            both_defect_payoff    = Constants.both_defect_payoff_2,
            betrayed_payoff       = Constants.betrayed_payoff_2,
            my_decision           = self.player.decision,
            opponent_decision     = other.decision,
            same_choice           = self.player.decision == other.decision,
            both_cooperate        = self.player.decision == "Action 1" and other.decision == "Action 1",
            both_defect           = self.player.decision == "Action 2" and other.decision == "Action 2",
            i_cooperate_he_defects= self.player.decision == "Action 1" and other.decision == "Action 2",
            i_defect_he_cooperates= self.player.decision == "Action 2" and other.decision == "Action 1",

            # Show ONLY PD points on Results page:
            round_stage_points    = self.player.stage_points,
            # (optional) round_total_points = self.player.payoff,
        )


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


class BeliefElicitation(Page):
    form_model = 'player'
    form_fields = ['belief', 'belief_interacted']
    template_name = 'prisoner/belief_elicitation.html'

    def before_next_page(self):
        self.player.belief_asked = True

    def vars_for_template(self):
        # game number from subsession flag
        game_number = 1 if self.subsession.active_game == 1 else 2

        # use what you actually store; fall back to sensible defaults
        match_number = getattr(self.subsession, 'match_number', 1)
        round_in_match = getattr(self.subsession, 'round_in_match_number', self.round_number)

        if game_number == 1:
            both_cooperate_payoff = Constants.both_cooperate_payoff_1
            betray_payoff = Constants.betray_payoff_1
            both_defect_payoff = Constants.both_defect_payoff_1
            betrayed_payoff = Constants.betrayed_payoff_1
        else:
            both_cooperate_payoff = Constants.both_cooperate_payoff_2
            betray_payoff = Constants.betray_payoff_2
            both_defect_payoff = Constants.both_defect_payoff_2
            betrayed_payoff = Constants.betrayed_payoff_2

        return dict(
            game_number=game_number,
            match_number=match_number,
            round_in_match=round_in_match,
            both_cooperate_payoff=both_cooperate_payoff,
            betray_payoff=betray_payoff,
            both_defect_payoff=both_defect_payoff,
            betrayed_payoff=betrayed_payoff,
        )

class BeliefElicitationGame1(BeliefElicitation):
    def is_displayed(self):
        return self.subsession.active_game == 1 and self.round_number <= Constants.num_rounds_game1

class BeliefElicitationGame2(BeliefElicitation):
    def is_displayed(self):
        return (
            self.subsession.active_game == 2 and
            Constants.num_rounds_game1 < self.round_number <= (Constants.num_rounds_game1 + Constants.num_rounds_game2)
        )



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

# --- bombINTRO  ---
class BombIntro(Page):
    def is_displayed(self):
        return self.round_number == FINAL_ROUND

    def vars_for_template(self):
        cols = Constants.bret_cols
        nums = list(range(1, Constants.bret_num_boxes + 1))
        grid = [nums[i:i+cols] for i in range(0, len(nums), cols)]
        return dict(
            grid=grid,
            num_boxes=Constants.bret_num_boxes,
            points_per_box=Constants.bret_points_per_box,
            pay_if_hit=Constants.bret_pay_if_hit,
            interval_sec=Constants.bret_interval_sec,
        )


# --- NEW: a Start page that draws the bomb & starts the timer ---
class BombStart(Page):
    def is_displayed(self):
        return self.round_number == FINAL_ROUND

    def vars_for_template(self):
        # build a 10x10 grid of numbers 1–100
        grid = []
        counter = 1
        for _ in range(10):          # 10 rows
            row = []
            for _ in range(10):      # 10 cols
                row.append(counter)
                counter += 1
            grid.append(row)

        return dict(
            num_boxes=Constants.bret_num_boxes,
            points_per_box=Constants.bret_points_per_box,
            pay_if_hit=Constants.bret_pay_if_hit,
            interval_sec=Constants.bret_interval_sec,
            grid=grid,
        )


    def before_next_page(self):
        # When participant clicks "Start", start the sequential BRET
        self.player.bret_start()


# --- NEW: a Stop page that shows the live counter (client-side),
#          and when user clicks "Stop", we freeze and score server-side. ---
class BombStop(Page):
    form_model = 'player'
    template_name = 'prisoner/BRETStop.html'

    def is_displayed(self):
        return self.round_number == FINAL_ROUND

    def vars_for_template(self):
        cols = Constants.bret_cols
        nums = list(range(1, Constants.bret_num_boxes + 1))
        grid = [nums[i:i+cols] for i in range(0, len(nums), cols)]
        start_ts = int(self.player.bret_start_time * 1000) if self.player.bret_start_time else int(time.time() * 1000)
        return dict(
            start_ts_ms=start_ts,
            interval_sec=Constants.bret_interval_sec,
            num_boxes=Constants.bret_num_boxes,
            points_per_box=Constants.bret_points_per_box,
            grid=grid,                        # <-- added
        )

    def before_next_page(self):
        self.player.bret_stop_and_score()



# --- RESULTS: read the new sequential fields ---
class BombResults(Page):
    def is_displayed(self):
        return self.round_number == FINAL_ROUND

    def vars_for_template(self):
        p = self.player
        # compute bomb row/col for display
        bomb_idx = p.bret_bomb_box
        r = (bomb_idx - 1) // Constants.bret_cols + 1
        c = (bomb_idx - 1) % Constants.bret_cols + 1
        return dict(
            collected=p.bret_collected_count,
            bomb_idx=bomb_idx,
            bomb_rc=f'{r}-{c}',
            hit=p.bret_hit,
            points=p.bret_points,
            points_per_box=Constants.bret_points_per_box,
            num_boxes=Constants.bret_num_boxes,
        )


class CRTIntro(Page):
    def is_displayed(self):
        return self.round_number == FINAL_ROUND

class CRT_Q1(Page):
    def is_displayed(self):
        return self.round_number == FINAL_ROUND
    form_model = 'player'
    form_fields = ['crt_q1']

    def error_message(self, values):
        v = values.get('crt_q1')
        if v is None or not isinstance(v, int):
            return "Please enter an integer (no decimals)."
    def before_next_page(self):
        self.player.crt_q1_correct = (self.player.crt_q1 == 5)

class CRT_Q1_Result(Page):
    def is_displayed(self):
        return self.round_number == FINAL_ROUND
    def vars_for_template(self):
        return dict(correct=self.player.crt_q1_correct)
class CRT_Q2(Page):
    def is_displayed(self):
        return self.round_number == FINAL_ROUND
    form_model = 'player'
    form_fields = ['crt_q2']

    def error_message(self, values):
        v = values.get('crt_q2')
        if v is None or not isinstance(v, int):
            return "Please enter an integer (no decimals)."
    def before_next_page(self):
        self.player.crt_q2_correct = (self.player.crt_q2 == 5)

class CRT_Q2_Result(Page):
    def is_displayed(self):
        return self.round_number == FINAL_ROUND
    def vars_for_template(self):
        return dict(correct=self.player.crt_q2_correct)

class CRT_Q3(Page):
    def is_displayed(self):
        return self.round_number == FINAL_ROUND
    form_model = 'player'
    form_fields = ['crt_q3']

    def error_message(self, values):
        v = values.get('crt_q3')
        if v is None or not isinstance(v, int):
            return "Please enter an integer (no decimals)."

    def before_next_page(self):
        self.player.crt_q3_correct = (self.player.crt_q3 == 47)

class CRT_Q3_Result(Page):
    def is_displayed(self):
        return self.round_number == FINAL_ROUND
    def vars_for_template(self):
        return dict(correct=self.player.crt_q3_correct)

class Demographics(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender', 'gender_self_describe',
        'education', 'education_other',
        'econ_courses',
        'native_english',
    ]

    def is_displayed(self):
        return self.round_number == FINAL_ROUND

    def error_message(self, values):
        errors = {}
        if values.get('gender') == 'Self-describe' and not values.get('gender_self_describe'):
            errors['gender_self_describe'] = "Please specify your gender or choose a different option."
        if values.get('education') == 'Other' and not values.get('education_other'):
            errors['education_other'] = "Please specify your education or choose a different option."
        return errors or None

    def before_next_page(self):
        self.participant.vars['demographics_done'] = True


class StoreTotals(WaitPage):
    """Final step inside 'prisoner'.

    For each game (Part 1 and Part 2):
      - PD payoff = sum of stage_points within ONE randomly selected match.
      - Belief payoff = ONE randomly selected round within a DIFFERENT randomly selected match.
        *If a game has fewer than 2 matches, no belief payoff is paid for that game.*
    Also adds:
      - BRET points in participant.vars['bret_points'].
      - CRT (Part 4) points: 20 per correct answer across 3 questions.
    Saves everything into participant.vars for the payment app to display.
    """
    def is_displayed(self):
        return self.round_number == FINAL_ROUND

    @staticmethod
    def _group_by_game_and_match(rounds):
        grouped = {1: {}, 2: {}}
        for r in rounds:
            g = r.subsession.active_game
            m = r.subsession.match_number
            grouped[g].setdefault(m, []).append(r)
        for g in (1, 2):
            for m in grouped[g]:
                grouped[g][m].sort(key=lambda rr: rr.subsession.round_in_match_number)
        return grouped

    @staticmethod
    def _choose_two_distinct_matches_or_none(match_dict):
        """
        Return:
          (pd_match_num, pd_rounds), (belief_match_num, belief_rounds)
        - If >= 2 matches exist: returns 2 DISTINCT matches (by construction).
        - If exactly 1 match exists: returns (that_match, rounds) for PD, and (None, []) for belief.
        - If 0 matches: returns (None, []), (None, []).
        """
        if not match_dict:
            return (None, []), (None, [])
        keys = list(match_dict.keys())
        if len(keys) >= 2:
            import random
            pd_match, belief_match = random.sample(keys, 2)  # distinct
            return (pd_match, match_dict[pd_match]), (belief_match, match_dict[belief_match])
        # only one match → PD uses it; belief is unavailable
        k = keys[0]
        return (k, match_dict[k]), (None, [])

    def after_all_players_arrive(self):
        import random
        from otree.api import Currency as c

        for p in self.group.get_players():
            pp = p.participant
            rounds = p.in_all_rounds()
            grouped = self._group_by_game_and_match(rounds)

            # ====== GAME 1 ======
            (g1_pd_match, g1_pd_rounds), (g1_belief_match, g1_belief_rounds) = \
                self._choose_two_distinct_matches_or_none(grouped.get(1, {}))

            g1_pd_points = sum((r.stage_points or 0) for r in g1_pd_rounds) if g1_pd_rounds else 0

            g1_belief_points = 0.0
            g1_belief_round_no = None
            if g1_belief_rounds:
                chosen_r = random.choice(g1_belief_rounds)
                g1_belief_points = float(chosen_r.belief_prize or 0)
                # show the round index within the belief match:
                g1_belief_round_no = chosen_r.subsession.round_in_match_number

            # ====== GAME 2 ======
            (g2_pd_match, g2_pd_rounds), (g2_belief_match, g2_belief_rounds) = \
                self._choose_two_distinct_matches_or_none(grouped.get(2, {}))

            g2_pd_points = sum((r.stage_points or 0) for r in g2_pd_rounds) if g2_pd_rounds else 0

            g2_belief_points = 0.0
            g2_belief_round_no = None
            if g2_belief_rounds:
                chosen_r = random.choice(g2_belief_rounds)
                g2_belief_points = float(chosen_r.belief_prize or 0)
                g2_belief_round_no = chosen_r.subsession.round_in_match_number

            # ====== BRET ======
            bret_points = float(pp.vars.get('bret_points', 0))

            # ====== CRT (Part 4): 20 points per correct (3 questions) ======
            crt_correct = 0
            if getattr(p, 'crt_q1_correct', False): crt_correct += 1
            if getattr(p, 'crt_q2_correct', False): crt_correct += 1
            if getattr(p, 'crt_q3_correct', False): crt_correct += 1
            CRT_POINTS_PER_CORRECT = 20
            crt_points = CRT_POINTS_PER_CORRECT * crt_correct

            # Totals
            pd_points_total = float(g1_pd_points + g2_pd_points)
            belief_points_total = float(g1_belief_points + g2_belief_points)
            grand_points = pd_points_total + belief_points_total + bret_points + crt_points

            # Save for payment page
            pp.vars.update({
                # Matches & paying rounds
                'g1_pd_match': g1_pd_match,
                'g1_belief_match': g1_belief_match,
                'g1_belief_round': g1_belief_round_no,

                'g2_pd_match': g2_pd_match,
                'g2_belief_match': g2_belief_match,
                'g2_belief_round': g2_belief_round_no,

                # Points breakdown
                'g1_pd_points': float(g1_pd_points),
                'g1_belief_points': float(g1_belief_points),
                'g2_pd_points': float(g2_pd_points),
                'g2_belief_points': float(g2_belief_points),
                'bret_points': float(bret_points),
                'crt_points': float(crt_points),

                'pd_points_total': pd_points_total,
                'belief_points_total': belief_points_total,
                'grand_points': float(grand_points),
            })

            # Points → Currency via SESSION_CONFIG
            pp.payoff = c(grand_points)



    # --- Page sequence ---


page_sequence = [
Instructions_1,
Instructions_2,
Instructions_4,
Instructions,
Q1, Q1Result,
Q2, Q2Result,
Q3, Q3Result,
Q4, Q4Result,
Instructions_3,

# === GAME 1 ===
Game1Intro,
DecisionGame1,
BeliefElicitationGame1,
ResultsWaitPageGame1,
ResultsGame1,
EndRoundGame1,

# === GAME 2 ===
Game2Intro,
DecisionGame2,
BeliefElicitationGame2,
ResultsWaitPageGame2,
ResultsGame2,
EndRoundGame2,

BombIntro,
BombStart,
BombStop,
BombResults,

CRTIntro,
CRT_Q1, CRT_Q1_Result,
CRT_Q2, CRT_Q2_Result,
CRT_Q3, CRT_Q3_Result,

Demographics,
StoreTotals,
]

