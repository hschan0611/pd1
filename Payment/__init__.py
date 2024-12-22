from otree.api import *

doc = """
Payment page for Prisoner's Dilemma game.
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    pd_earnings_template = 'prisoner/pd_earning_summary.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class FinalPayment(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pp = player.participant
        # Only consider PD earnings as quiz earnings are zero
        pp.pd_earning = sum([p.payoff for p in player.in_all_rounds()])  # Sum all PD payoffs
        pp.payoff = pp.pd_earning  # Set total payoff to just the PD earnings

    @staticmethod
    def vars_for_template(player: Player):
        pp = player.participant
        # Convert PD points to real-world currency
        pd_payment = cu(pp.pd_earning).to_real_world_currency(player.session)
        total_payment = pd_payment + player.session.config['participation_fee']

        return dict(
            pd_payment=pd_payment,
            total_payment=total_payment,
            participation_fee=player.session.config['participation_fee'],
            match_history=player.in_all_rounds()  # Providing match history for display
        )


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [FinalPayment]
