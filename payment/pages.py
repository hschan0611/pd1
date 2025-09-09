# payment/pages.py
from otree.api import *
from otree.api import Currency as c
import random


class FinalPayment(Page):
    """
    Payment rule:
      • Randomly select 1 supergame from Game 1 and 1 from Game 2.
      • PD payoff = sum of stage_points (actions only) within each selected supergame.
      • Belief payoff = 1 randomly selected round within each selected supergame (0 or 16).
      • BRET payoff = participant.vars['bret_points'] (default 0; must be int).
      • Conversion rate set in settings (e.g., 16 pts = $1), plus $5 show-up.
    """

    # ---------- helpers ----------
    @staticmethod
    def _group_rounds_by_game_and_match(rounds):
        out = {1: {}, 2: {}}
        for r in rounds:
            g = r.subsession.active_game
            m = r.subsession.match_number
            out[g].setdefault(m, []).append(r)
        # sort each match’s rounds by in-match order (optional)
        for g in (1, 2):
            for m in out[g]:
                out[g][m].sort(key=lambda rr: rr.subsession.round_in_match_number)
        return out

    @staticmethod
    def _choose_match(match_dict):
        if not match_dict:
            return None, []
        match_num = random.choice(list(match_dict.keys()))
        return match_num, match_dict[match_num]

    # ---------- oTree hooks ----------
    def before_next_page(self, timeout_happened):
        pp = self.participant
        rounds = self.player.in_all_rounds()

        grouped = self._group_rounds_by_game_and_match(rounds)

        # Game 1
        g1_match_num, g1_rounds = self._choose_match(grouped.get(1, {}))
        g1_pd_points = sum(r.stage_points for r in g1_rounds) if g1_rounds else 0
        g1_belief_points = 0
        g1_belief_round_no = None
        if g1_rounds:
            chosen = random.choice(g1_rounds)
            g1_belief_points = chosen.belief_prize or 0
            g1_belief_round_no = chosen.round_number

        # Game 2
        g2_match_num, g2_rounds = self._choose_match(grouped.get(2, {}))
        g2_pd_points = sum(r.stage_points for r in g2_rounds) if g2_rounds else 0
        g2_belief_points = 0
        g2_belief_round_no = None
        if g2_rounds:
            chosen = random.choice(g2_rounds)
            g2_belief_points = chosen.belief_prize or 0
            g2_belief_round_no = chosen.round_number

        # BRET (ensure int)
        bret_points = int(pp.vars.get('bret_points', 0))

        pd_points_total = g1_pd_points + g2_pd_points
        belief_points_total = g1_belief_points + g2_belief_points
        grand_points = pd_points_total + belief_points_total + bret_points

        # Save for template
        pp.vars.update({
            'chosen_g1_match': g1_match_num,
            'chosen_g2_match': g2_match_num,
            'chosen_g1_belief_round': g1_belief_round_no,
            'chosen_g2_belief_round': g2_belief_round_no,

            'g1_pd_points': g1_pd_points,
            'g2_pd_points': g2_pd_points,
            'g1_belief_points': g1_belief_points,
            'g2_belief_points': g2_belief_points,
            'bret_points': bret_points,

            'pd_points_total': pd_points_total,
            'belief_points_total': belief_points_total,
            'grand_points': grand_points,
        })

        # participant payoff in Currency units
        self.participant.payoff = c(grand_points)

    def vars_for_template(self):
        pp = self.participant
        sess = self.session

        g1_match = pp.vars.get('chosen_g1_match')
        g2_match = pp.vars.get('chosen_g2_match')

        g1_pd_points = pp.vars.get('g1_pd_points', 0)
        g1_belief_points = pp.vars.get('g1_belief_points', 0)
        g2_pd_points = pp.vars.get('g2_pd_points', 0)
        g2_belief_points = pp.vars.get('g2_belief_points', 0)
        bret_points = pp.vars.get('bret_points', 0)

        grand_points = pp.vars.get('grand_points', 0)

        task_cash = c(grand_points).to_real_world_currency(sess)
        showup = sess.config.get('participation_fee', 5.00)
        grand_total_cash = task_cash + showup

        return dict(
            g1_match=g1_match,
            g2_match=g2_match,

            g1_pd_points=g1_pd_points,
            g1_belief_points=g1_belief_points,
            g2_pd_points=g2_pd_points,
            g2_belief_points=g2_belief_points,
            bret_points=bret_points,

            grand_points=grand_points,
            task_cash=task_cash,
            participation_fee=showup,
            grand_total_cash=grand_total_cash,
        )

page_sequence = [FinalPayment]
