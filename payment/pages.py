# payment/pages.py
from otree.api import *
from otree.api import Currency as c

class FinalPayment(Page):
    def vars_for_template(self):
        pp = self.participant
        sess = self.session

        g1_pd_match      = pp.vars.get('g1_pd_match')
        g1_belief_match  = pp.vars.get('g1_belief_match')
        g1_belief_round  = pp.vars.get('g1_belief_round')

        g2_pd_match      = pp.vars.get('g2_pd_match')
        g2_belief_match  = pp.vars.get('g2_belief_match')
        g2_belief_round  = pp.vars.get('g2_belief_round')

        g1_pd_points     = pp.vars.get('g1_pd_points', 0.0)
        g1_belief_points = pp.vars.get('g1_belief_points', 0.0)
        g2_pd_points     = pp.vars.get('g2_pd_points', 0.0)
        g2_belief_points = pp.vars.get('g2_belief_points', 0.0)
        bret_points      = pp.vars.get('bret_points', 0.0)
        crt_points       = pp.vars.get('crt_points', 0.0)  # <-- NEW

        grand_points     = pp.vars.get('grand_points', 0.0)

        task_cash = c(grand_points).to_real_world_currency(sess)
        showup = sess.config.get('participation_fee', 5.00)
        grand_total_cash = task_cash + showup

        return dict(
            g1_pd_match=g1_pd_match,
            g1_belief_match=g1_belief_match,
            g1_belief_round=g1_belief_round,
            g2_pd_match=g2_pd_match,
            g2_belief_match=g2_belief_match,
            g2_belief_round=g2_belief_round,

            g1_pd_points=g1_pd_points,
            g1_belief_points=g1_belief_points,
            g2_pd_points=g2_pd_points,
            g2_belief_points=g2_belief_points,
            bret_points=bret_points,
            crt_points=crt_points,  # <-- NEW

            grand_points=grand_points,
            task_cash=task_cash,
            participation_fee=showup,
            grand_total_cash=grand_total_cash,
        )

page_sequence = [FinalPayment]
