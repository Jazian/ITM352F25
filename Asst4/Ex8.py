# Ex1-5. Blackjack Game with Flask
# Ex6. Create a Flask Poker Game Using Sessions utulizing a deck of cards stored in the session 
# Ex6. Reset deck when switching games.
# Ex7. Create a global reset route to reset both games and directs them to their respective home pages.
# Ex7. Add AI Poker Bet, Raise, Fold Logic
# Ex8. Add a cheat feature for poker that reveals win odds based on current hand and remaining cards in the deck.

from flask import Flask, render_template, redirect, url_for, request, session
import random
# Poker specific imports
import itertools
from collections import Counter


app = Flask(__name__)
app.secret_key = "supersecretkey"

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def make_deck():
    deck = []
    # ranks is the existing dict; use its keys for rank names
    for r in list(ranks.keys()):
        for s in suits:
            filename = f"{r}_of_{s}.svg"
            deck.append((r, s, filename))
    random.shuffle(deck)
    return deck

def ensure_deck():
    if 'deck' not in session or not session.get('deck'):
        session['deck'] = make_deck()
        session['used_cards'] = []
        session['show_used'] = False
        session.modified = True

# Replaces deal_card()
def draw_from_deck():
    """Draw one card from the session deck, track it in used_cards, reshuffle if empty."""
    ensure_deck()
    deck = session.get('deck', [])
    if not deck:
        # reshuffle if somehow empty
        session['deck'] = make_deck()
        session['used_cards'] = []
        session['show_used'] = False
        deck = session['deck']
    card = deck.pop()           # draw one card
    used = session.get('used_cards', [])
    used.append(card)
    session['deck'] = deck
    session['used_cards'] = used
    session.modified = True
    return card

def calculate_score(hand):
    score = sum(ranks[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == 'A')
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

@app.route('/')
def home():
    return render_template('home.html')

# Blackjack game ------------------------------------------------------------------------------------
@app.route('/blackjack', methods=['GET', 'POST'])
def blackjack():
    if 'chips' not in session:
        session['chips'] = 1000
    if 'bet' not in session:
        session['bet'] = 0
    if 'player_hand' not in session:
        session['player_hand'] = []
    if 'dealer_hand' not in session:
        session['dealer_hand'] = []
    if 'split' not in session: # Track if player has split
        session['split'] = False
    if 'split_hand' not in session: # Hand for split cards
        session['split_hand'] = []
    if 'current_hand' not in session:
        session['current_hand'] = 'player'
    if 'used_cards' not in session: # Track used cards for cheat feature
        session['used_cards'] = []
    if 'show_used' not in session: # Whether to show used cards
        session['show_used'] = False


    player_hand = session.get('player_hand', [])
    dealer_hand = session.get('dealer_hand', [])
    split_hand = session.get('split_hand', [])
    split_flag = session.get('split', False)
    current_hand = session.get('current_hand', 'player')

    player_score = calculate_score(player_hand) if player_hand else 0
    dealer_score = calculate_score(dealer_hand) if dealer_hand else 0
    split_score = calculate_score(split_hand) if split_hand else 0

    hide_dealer = True
    result = None
    messages = []

    if session['chips'] <= 0 and session['bet'] == 0 and not session['player_hand'] and not session['split_hand']:
        result = "You're out of chips! Game over."
        return render_template('blackjack.html',
                               player_hand=[],
                               split_hand=[],
                               dealer_hand=[],
                               player_score=0,
                               split_score=0,
                               dealer_score=0,
                               result=result,
                               hide_dealer=True,
                               chips=session['chips'],
                               bet=session['bet'],
                               split=False,
                               current_hand='player'
                               )

    if request.method == 'POST':
        action = request.form.get('action')

        # Toggle cheat view
        if action == 'cheat':
            session['show_used'] = not session.get('show_used', False)
            # re-render current state immediately
            return render_template('blackjack.html',
                                player_hand=session.get('player_hand', []),
                                split_hand=session.get('split_hand', []),
                                dealer_hand=session.get('dealer_hand', []),
                                player_score=calculate_score(session.get('player_hand', [])),
                                split_score=calculate_score(session.get('split_hand', [])),
                                dealer_score=calculate_score(session.get('dealer_hand', [])),
                                result=None,
                                hide_dealer=True,
                                chips=session['chips'],
                                bet=session['bet'],
                                split=session['split'],
                                current_hand=session['current_hand'],
                                messages=[],
                                used_cards=session.get('used_cards', []),
                                show_used=session.get('show_used', False)
                                )
        
        if action == 'bet':
            bet_amount = int(request.form.get('bet'))
            if bet_amount <= session['chips'] and bet_amount > 0:
                session['bet'] = bet_amount
                session['chips'] -= bet_amount
                # If deck is low on cards, reshuffle
                if len(session.get('deck', [])) < 10:
                    session['deck'] = make_deck()
                    session['used_cards'] = []
                    session['show_used'] = False
                    session.modified = True
                session['player_hand'] = [draw_from_deck(), draw_from_deck()]
                session['dealer_hand'] = [draw_from_deck(), draw_from_deck()]
                session['split'] = False
                session['split_hand'] = []
                session['current_hand'] = 'player'
                session['hand_done'] = {'player': False, 'split': False}
                session['round_over'] = False

                player_hand = session['player_hand']
                dealer_hand = session['dealer_hand']
                player_score = calculate_score(player_hand)
                dealer_score = calculate_score(dealer_hand)

            if player_score > 21:
                result = "You busted!"
                session['bet'] = 0
                return render_template('blackjack.html',
                                       player_hand=session.get('player_hand', []),
                                       split_hand=session.get('split_hand', []),
                                       dealer_hand=dealer_hand,
                                       player_score=player_score,
                                       split_score=calculate_score(session.get('split_hand', [])),
                                       dealer_score=dealer_score,
                                       result=result,
                                       hide_dealer=True,
                                       chips=session['chips'],
                                       bet=session['bet'],
                                       split=session['split'],
                                       current_hand=session['current_hand'],
                                       messages=messages,
                                       round_over=session.get('round_over', False),
                                       used_cards=session.get('used_cards', []),
                                       show_used=session.get('show_used', False)
                                       )

            if player_score == 21 or dealer_score == 21:
                hide_dealer = False
                if player_score == 21 and dealer_score == 21:
                    result = "Both have Blackjack! It's a tie!"
                    session['chips'] += session['bet']
                elif player_score == 21:
                    result = "Blackjack! You win!"
                    session['chips'] += session['bet'] * 2
                else:
                    result = "Dealer has Blackjack! Dealer wins!"
                session['bet'] = 0

                return render_template('blackjack.html',
                                       player_hand=player_hand,
                                       split_hand=session['split_hand'],
                                       dealer_hand=dealer_hand,
                                       player_score=player_score,
                                       split_score=calculate_score(session['split_hand']),
                                       dealer_score=dealer_score,
                                       result=result,
                                       hide_dealer=False,
                                       chips=session['chips'],
                                       bet=session['bet'],
                                       split=session['split'],
                                       current_hand=session['current_hand'],
                                       used_cards=session.get('used_cards', []),
                                       show_used=session.get('show_used', False)
                                       )
        # Generated by Copilot using the phrase "Create a split action for blackjack game in Flask" thus then auto eddited most of the fixes in my Session, Hit, and Stand logic
        elif action == 'split':
            if len(player_hand) == 2 and player_hand[0][0] == player_hand[1][0] and session['chips'] >= session['bet'] and session['bet'] > 0:
                session['chips'] -= session['bet']
                first_card = player_hand[0]
                second_card = player_hand[1]
                session['player_hand'] = [first_card, draw_from_deck()]
                session['split_hand'] = [second_card, draw_from_deck()]
                session['split'] = True
                session['current_hand'] = 'player'
                player_hand = session['player_hand']
                split_hand = session['split_hand']
                player_score = calculate_score(player_hand)
                split_score = calculate_score(split_hand)
            else:
                messages.append("Cannot split: cards don't match or insufficient chips.")

        elif action == 'hit':
            # don't allow actions if round already resolved
            if session.get('round_over', False):
                messages.append("Round is over. Place a new bet to continue.")
            else:
                active = session.get('current_hand', 'player')
                hand_done = session.get('hand_done', {'player': False, 'split': False})

                # refuse hit if this hand is already finished
                if hand_done.get(active, False):
                    messages.append(f"{active.capitalize()} hand is finished. Choose Stand or wait for resolution.")
                else:
                    # operate on the active hand using reassign pattern
                    if session.get('split', False) and active == 'split':
                        sh = session.get('split_hand', [])
                        sh.append(draw_from_deck())
                        session['split_hand'] = sh
                        split_score = calculate_score(sh)

                        if split_score > 21:
                            messages.append("Split hand busted.")
                            hd = session.get('hand_done', {'player': False, 'split': False})
                            hd['split'] = True
                            session['hand_done'] = hd
                            # if player hand already done, finish round as both busted
                            if session['hand_done'].get('player', False):
                                result = "Both hands busted!"
                                session['bet'] = 0
                                session['round_over'] = True
                                return render_template('blackjack.html',
                                                    player_hand=session.get('player_hand', []),
                                                    split_hand=session.get('split_hand', []),
                                                    dealer_hand=dealer_hand,
                                                    player_score=calculate_score(session.get('player_hand', [])),
                                                    split_score=split_score,
                                                    dealer_score=dealer_score,
                                                    result=result,
                                                    hide_dealer=True,
                                                    chips=session['chips'],
                                                    bet=session['bet'],
                                                    split=session['split'],
                                                    current_hand=session['current_hand'],
                                                    messages=messages,
                                                    round_over=session.get('round_over', False),
                                                    used_cards=session.get('used_cards', []),
                                                    show_used=session.get('show_used', False)
                                                    )
                        elif split_score == 21:
                            # mark split hand done
                            hd = session.get('hand_done', {'player': False, 'split': False})
                            hd['split'] = True
                            session['hand_done'] = hd
                            messages.append("Split hand reached 21.")
                            # if player hand already done -> resolve now (dealer plays and compare)
                            if session['hand_done'].get('player', False):
                                hide_dealer = False
                                dh = session.get('dealer_hand', [])
                                dealer_score = calculate_score(dh)
                                while dealer_score < 17:
                                    dh.append(draw_from_deck())
                                    dealer_score = calculate_score(dh)
                                session['dealer_hand'] = dh

                                total_return = 0
                                outcomes = []

                                ph = session.get('player_hand', [])
                                if ph:
                                    s = calculate_score(ph)
                                    if s > 21:
                                        outcomes.append("Hand 1: Busted")
                                    elif dealer_score > 21 or s > dealer_score:
                                        outcomes.append("Hand 1: Win")
                                        total_return += session['bet'] * 2
                                    elif s == dealer_score:
                                        outcomes.append("Hand 1: Tie")
                                        total_return += session['bet']
                                    else:
                                        outcomes.append("Hand 1: Lose")

                                sh2 = session.get('split_hand', [])
                                if sh2:
                                    s2 = calculate_score(sh2)
                                    if s2 > 21:
                                        outcomes.append("Hand 2: Busted")
                                    elif dealer_score > 21 or s2 > dealer_score:
                                        outcomes.append("Hand 2: Win")
                                        total_return += session['bet'] * 2
                                    elif s2 == dealer_score:
                                        outcomes.append("Hand 2: Tie")
                                        total_return += session['bet']
                                    else:
                                        outcomes.append("Hand 2: Lose")

                                session['chips'] += total_return
                                result = " | ".join(outcomes) if outcomes else "Round resolved."
                                session['bet'] = 0
                                session['round_over'] = True

                                return render_template('blackjack.html',
                                                    player_hand=session.get('player_hand', []),
                                                    split_hand=session.get('split_hand', []),
                                                    dealer_hand=session.get('dealer_hand', []),
                                                    player_score=calculate_score(session.get('player_hand', [])),
                                                    split_score=calculate_score(session.get('split_hand', [])),
                                                    dealer_score=dealer_score,
                                                    result=result,
                                                    hide_dealer=False,
                                                    chips=session['chips'],
                                                    bet=session['bet'],
                                                    split=session.get('split', False),
                                                    current_hand=session.get('current_hand', 'player'),
                                                    messages=messages,
                                                    used_cards=session.get('used_cards', []),
                                                    show_used=session.get('show_used', False)
                                                    )
                            else:
                                # switch to the other hand so player can play it
                                session['current_hand'] = 'player'
                                return render_template('blackjack.html',
                                                    player_hand=session.get('player_hand', []),
                                                    split_hand=session.get('split_hand', []),
                                                    dealer_hand=session.get('dealer_hand', []),
                                                    player_score=calculate_score(session.get('player_hand', [])),
                                                    split_score=split_score,
                                                    dealer_score=calculate_score(session.get('dealer_hand', [])),
                                                    result=None,
                                                    hide_dealer=True,
                                                    chips=session['chips'],
                                                    bet=session['bet'],
                                                    split=session['split'],
                                                    current_hand=session['current_hand'],
                                                    messages=messages,
                                                    used_cards=session.get('used_cards', []),
                                                    show_used=session.get('show_used', False)
                                                    )

                    else:
                        ph = session.get('player_hand', [])
                        ph.append(draw_from_deck())
                        session['player_hand'] = ph
                        player_score = calculate_score(ph)

                        if player_score > 21:
                            hd = session.get('hand_done', {'player': False, 'split': False})
                            hd['player'] = True
                            session['hand_done'] = hd

                            if session.get('split', False):
                                messages.append("First hand busted. Moving to split hand.")
                                session['current_hand'] = 'split'
                            else:
                                result = "You busted!"
                                session['bet'] = 0
                                session['round_over'] = True
                                return render_template('blackjack.html',
                                                    player_hand=session.get('player_hand', []),
                                                    split_hand=session.get('split_hand', []),
                                                    dealer_hand=dealer_hand,
                                                    player_score=player_score,
                                                    split_score=calculate_score(session.get('split_hand', [])),
                                                    dealer_score=dealer_score,
                                                    result=result,
                                                    hide_dealer=True,
                                                    chips=session['chips'],
                                                    bet=session['bet'],
                                                    split=session['split'],
                                                    current_hand=session['current_hand'],
                                                    messages=messages,
                                                    used_cards=session.get('used_cards', []),
                                                    show_used=session.get('show_used', False)
                                                    )
                        elif player_score == 21:
                            # mark player hand done
                            hd = session.get('hand_done', {'player': False, 'split': False})
                            hd['player'] = True
                            session['hand_done'] = hd
                            messages.append("First hand reached 21.")

                            # If no split, immediate payout and end round
                            if not session.get('split', False):
                                result = "21! You win!"
                                session['chips'] += session['bet'] * 2
                                session['bet'] = 0
                                session['round_over'] = True
                                return render_template('blackjack.html',
                                                    player_hand=session.get('player_hand', []),
                                                    split_hand=session.get('split_hand', []),
                                                    dealer_hand=session.get('dealer_hand', []),
                                                    player_score=player_score,
                                                    split_score=calculate_score(session.get('split_hand', [])),
                                                    dealer_score=calculate_score(session.get('dealer_hand', [])),
                                                    result=result,
                                                    hide_dealer=True,
                                                    chips=session['chips'],
                                                    bet=session['bet'],
                                                    split=session['split'],
                                                    current_hand=session['current_hand'],
                                                    messages=messages,
                                                    used_cards=session.get('used_cards', []),
                                                    show_used=session.get('show_used', False)
                                                    )

                            # If split exists, either switch to split or resolve if both done
                            else:
                                # if split already done -> both hands finished, resolve now
                                if session['hand_done'].get('split', False):
                                    hide_dealer = False
                                    dh = session.get('dealer_hand', [])
                                    dealer_score = calculate_score(dh)
                                    while dealer_score < 17:
                                        dh.append(draw_from_deck())
                                        dealer_score = calculate_score(dh)
                                    session['dealer_hand'] = dh

                                    total_return = 0
                                    outcomes = []

                                    ph2 = session.get('player_hand', [])
                                    if ph2:
                                        s = calculate_score(ph2)
                                        if s > 21:
                                            outcomes.append("Hand 1: Busted")
                                        elif dealer_score > 21 or s > dealer_score:
                                            outcomes.append("Hand 1: Win")
                                            total_return += session['bet'] * 2
                                        elif s == dealer_score:
                                            outcomes.append("Hand 1: Tie")
                                            total_return += session['bet']
                                        else:
                                            outcomes.append("Hand 1: Lose")

                                    sh3 = session.get('split_hand', [])
                                    if sh3:
                                        s2 = calculate_score(sh3)
                                        if s2 > 21:
                                            outcomes.append("Hand 2: Busted")
                                        elif dealer_score > 21 or s2 > dealer_score:
                                            outcomes.append("Hand 2: Win")
                                            total_return += session['bet'] * 2
                                        elif s2 == dealer_score:
                                            outcomes.append("Hand 2: Tie")
                                            total_return += session['bet']
                                        else:
                                            outcomes.append("Hand 2: Lose")

                                    session['chips'] += total_return
                                    result = " | ".join(outcomes) if outcomes else "Round resolved."
                                    session['bet'] = 0
                                    session['round_over'] = True

                                    return render_template('blackjack.html',
                                                        player_hand=session.get('player_hand', []),
                                                        split_hand=session.get('split_hand', []),
                                                        dealer_hand=session.get('dealer_hand', []),
                                                        player_score=calculate_score(session.get('player_hand', [])),
                                                        split_score=calculate_score(session.get('split_hand', [])),
                                                        dealer_score=dealer_score,
                                                        result=result,
                                                        hide_dealer=False,
                                                        chips=session['chips'],
                                                        bet=session['bet'],
                                                        split=session.get('split', False),
                                                        current_hand=session.get('current_hand', 'player'),
                                                        messages=messages,
                                                        used_cards=session.get('used_cards', []),
                                                        show_used=session.get('show_used', False)
                                                        )
                                else:
                                    # switch to split hand so player can play it
                                    session['current_hand'] = 'split'
                                    return render_template('blackjack.html',
                                                        player_hand=session.get('player_hand', []),
                                                        split_hand=session.get('split_hand', []),
                                                        dealer_hand=session.get('dealer_hand', []),
                                                        player_score=player_score,
                                                        split_score=calculate_score(session.get('split_hand', [])),
                                                        dealer_score=calculate_score(session.get('dealer_hand', [])),
                                                        result=None,
                                                        hide_dealer=True,
                                                        chips=session['chips'],
                                                        bet=session['bet'],
                                                        split=session['split'],
                                                        current_hand=session['current_hand'],
                                                        messages=messages,
                                                        used_cards=session.get('used_cards', []),
                                                        show_used=session.get('show_used', False)
                                                        )

        elif action == 'stand':
            if session.get('split', False) and session.get('current_hand') == 'player':
                session['current_hand'] = 'split'
                messages.append("Now playing split hand.")
            else:
                hide_dealer = False
                dh = session.get('dealer_hand', [])
                dealer_score = calculate_score(dh)
                while dealer_score < 17:
                    dh.append(draw_from_deck())
                    dealer_score = calculate_score(dh)
                session['dealer_hand'] = dh
                dealer_hand = session['dealer_hand']

                total_return = 0
                outcomes = []

                ph = session.get('player_hand', [])
                if ph:
                    s = calculate_score(ph)
                    if s > 21:
                        outcomes.append("Hand 1: Busted")
                    elif dealer_score > 21 or s > dealer_score:
                        outcomes.append("Hand 1: Win")
                        total_return += session['bet'] * 2
                    elif s == dealer_score:
                        outcomes.append("Hand 1: Tie")
                        total_return += session['bet']
                    else:
                        outcomes.append("Hand 1: Lose")
                
                if session.get('split', False):
                    sh = session.get('split_hand', [])
                    if sh:
                        s2 = calculate_score(sh)
                        if s2 > 21:
                            outcomes.append("Hand 2: Busted")
                        elif dealer_score > 21 or s2 > dealer_score:
                            outcomes.append("Hand 2: Win")
                            total_return += session['bet'] * 2
                        elif s2 == dealer_score:
                            outcomes.append("Hand 2: Tie")
                            total_return += session['bet']
                        else:
                            outcomes.append("Hand 2: Lose")

                session['chips'] += total_return
                if outcomes:
                    result = " | ".join(outcomes)
                else:
                    result = "Round resolved."

                # mark round finished but KEEP hands so template can show them
                session['bet'] = 0
                session['round_over'] = True
                # do NOT clear session['player_hand'] or session['split_hand'] here

                return render_template('blackjack.html',
                                        player_hand=session.get('player_hand', []),
                                        split_hand=session.get('split_hand', []),
                                        dealer_hand=dealer_hand,
                                        player_score=calculate_score(session.get('player_hand', [])),
                                        split_score=calculate_score(session.get('split_hand', [])),
                                        dealer_score=dealer_score,
                                        result=result,
                                        hide_dealer=False,
                                        chips=session['chips'],
                                        bet=session['bet'],
                                        split=session.get('split', False),
                                        current_hand=session.get('current_hand', 'player'),
                                        messages=messages,
                                        used_cards=session.get('used_cards', []),
                                        show_used=session.get('show_used', False)
                                        )



    return render_template('blackjack.html',
                           player_hand=session.get('player_hand', []),
                           split_hand=session.get('split_hand', []),
                           dealer_hand=session.get('dealer_hand', []),
                           player_score=calculate_score(session.get('player_hand', [])),
                           split_score=calculate_score(session.get('split_hand', [])),
                           dealer_score=calculate_score(session.get('dealer_hand', [])),
                           result=result,
                           hide_dealer=hide_dealer,
                           chips=session['chips'],
                           bet=session['bet'],
                           split=session['split'],
                           current_hand=session['current_hand'],
                           messages=messages,
                           used_cards=session.get('used_cards', []),
                           show_used=session.get('show_used', False)
                        )

# Blackjack game END ----------------------------------------------------------------------------------

# Poker game evaluation START -------------------------------------------------------------------------

# Map rank strings to numeric values for comparison (Ace high)
RANK_VALUE = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

def reveal_remaining_community(poker_state):
    """Ensure the community list has 5 cards by drawing from the deck."""
    ensure_deck()
    community = poker_state.setdefault('community', [])
    while len(community) < 5:
        community.append(draw_from_deck())
    poker_state['community'] = community

def perform_showdown(poker_state, messages):
    """Reveal full board and evaluate winners, updating poker_state and player chips."""
    # make sure the full community is present
    reveal_remaining_community(poker_state)

    ph = poker_state.get('player_hand', [])
    a1 = poker_state.get('ai1_hand', [])
    a2 = poker_state.get('ai2_hand', [])
    community = poker_state.get('community', [])

    ev_p, _ = best_five_card_value(ph, community)
    ev_a1, _ = best_five_card_value(a1, community)
    ev_a2, _ = best_five_card_value(a2, community)

    best_all = max(ev_p, ev_a1, ev_a2)
    winners = []
    if ev_p == best_all:
        winners.append('player')
    if ev_a1 == best_all:
        winners.append('ai1')
    if ev_a2 == best_all:
        winners.append('ai2')

    pot = poker_state.get('pot', 0)

    if 'player' in winners and len(winners) == 1:
        session['chips'] += pot
        poker_state['result'] = f"You win the pot of {pot}!"
    elif 'player' in winners:
        share = pot // len(winners)
        session['chips'] += share
        poker_state['result'] = f"Tie. You receive {share} (split among {len(winners)})."
    else:
        poker_state['result'] = "You lost the pot."

    poker_state['stage'] = 'showdown'
    poker_state['round_over'] = True
    messages.append(poker_state['result'])


def estimate_win_odds(poker_state, trials=1000):
    """Monte-Carlo estimate of (win, tie, loss) for the player vs two random opponents.
       Uses the remaining cards in session['deck'] (does not modify session).
       Returns dict: {'win': float,'tie':float,'loss':float,'trials':int}
    """
    # Require player to have hole cards
    player_hole = poker_state.get('player_hand', [])
    if not player_hole or len(player_hole) != 2:
        return None

    community = list(poker_state.get('community', []))
    # remaining deck (copy) from session (these are the undealt cards)
    remaining = list(session.get('deck', []))
    if not remaining:
        # defensive fallback: build a fresh deck and remove known cards
        full = make_deck()
        # remove the known cards (player + community + ai hands if present)
        known = set((c[0], c[1], c[2]) for c in player_hole + community + poker_state.get('ai1_hand', []) + poker_state.get('ai2_hand', []))
        remaining = [c for c in full if (c[0], c[1], c[2]) not in known]

    wins = ties = losses = 0
    needed_comm = max(0, 5 - len(community))

    # Small micro-optimizations: local refs
    best5 = best_five_card_value
    rand = random.random
    for _ in range(trials):
        d = remaining[:]  # copy
        random.shuffle(d)

        # deal two opponents: draw 2 cards each
        # if not enough cards left, break early
        if len(d) < 4 + needed_comm:
            # fallback to fewer trials if deck is too small (shouldn't normally happen)
            break

        ai1 = [d.pop(), d.pop()]
        ai2 = [d.pop(), d.pop()]

        # complete the community board for this sim
        comm = list(community)
        for _n in range(needed_comm):
            comm.append(d.pop())

        ev_p, _ = best5(player_hole, comm)
        ev_a1, _ = best5(ai1, comm)
        ev_a2, _ = best5(ai2, comm)

        best_all = max(ev_p, ev_a1, ev_a2)
        counts = 0
        if ev_p == best_all:
            counts += 1
        if ev_a1 == best_all:
            counts += 1
        if ev_a2 == best_all:
            counts += 1

        if ev_p == best_all and counts == 1:
            wins += 1
        elif ev_p == best_all:
            ties += 1
        else:
            losses += 1

    total = wins + ties + losses
    if total == 0:
        return None

    return {
        'win': wins / total,
        'tie': ties / total,
        'loss': losses / total,
        'trials': total
    }

# Generated by Copilot using the phrase "Create poker hand evaluation functions in Python" and then edited for clarity and correctness
def _is_straight(values_desc_unique):
    """Detect straight in a list of unique values sorted descending.
       Returns (is_straight_bool, high_card_of_straight)."""
    if len(values_desc_unique) < 5:
        return False, None
    vals = values_desc_unique
    # sliding window check
    for i in range(len(vals) - 4):
        window = vals[i:i+5]
        if window[0] - window[4] == 4:
            return True, window[0]
    # wheel (A-2-3-4-5) special case: treat Ace as 1
    if 14 in vals and {5,4,3,2}.issubset(set(vals)):
        return True, 5
    return False, None

# Generated by Copilot using the phrase "Create poker hand evaluation functions in Python" and then edited for clarity and correctness
def evaluate_5card(hand):
    """Evaluate exactly 5 cards.
       Returns a tuple ranking where larger tuples compare greater for better hands.
       Structure: (category_rank, tiebreakers...)
       Category ranks (higher is better):
         9 = Straight Flush
         8 = Four of a Kind
         7 = Full House
         6 = Flush
         5 = Straight
         4 = Three of a Kind
         3 = Two Pair
         2 = One Pair
         1 = High Card
    """
    # Generated by Copilot using the phrase "Create poker hand evaluation functions in Python" and then edited for clarity and correctness
    vals = [RANK_VALUE[c[0]] for c in hand]
    vals_desc = sorted(vals, reverse=True)
    counts = Counter(vals)
    counts_by_freq = sorted(counts.items(), key=lambda kv: (-kv[1], -kv[0]))  # (value, freq) sorted by freq desc, value desc
    suits = [c[1] for c in hand]
    is_flush = len(set(suits)) == 1
    unique_desc = sorted(set(vals_desc), reverse=True)
    is_str, high_st = _is_straight(unique_desc)

    # Straight flush
    if is_flush and is_str:
        return (9, high_st, ) + tuple(vals_desc)

    # Four of a kind
    if counts_by_freq[0][1] == 4:
        four_val = counts_by_freq[0][0]
        kicker = max(v for v in vals_desc if v != four_val)
        return (8, four_val, kicker)

    # Full house (3 + 2)
    if counts_by_freq[0][1] == 3 and counts_by_freq[1][1] >= 2:
        three_val = counts_by_freq[0][0]
        pair_val = counts_by_freq[1][0]
        return (7, three_val, pair_val)

    # Flush
    if is_flush:
        return (6,) + tuple(vals_desc)

    # Straight
    if is_str:
        return (5, high_st)

    # Three of a kind
    if counts_by_freq[0][1] == 3:
        three_val = counts_by_freq[0][0]
        kickers = [v for v in vals_desc if v != three_val]
        return (4, three_val) + tuple(kickers[:2])

    # Two pair
    if counts_by_freq[0][1] == 2 and counts_by_freq[1][1] == 2:
        pair_high = counts_by_freq[0][0]
        pair_low = counts_by_freq[1][0]
        kicker = max(v for v in vals_desc if v != pair_high and v != pair_low)
        # order pairs high->low
        high_pair, low_pair = max(pair_high, pair_low), min(pair_high, pair_low)
        return (3, high_pair, low_pair, kicker)

    # One pair
    if counts_by_freq[0][1] == 2:
        pair_val = counts_by_freq[0][0]
        kickers = [v for v in vals_desc if v != pair_val]
        return (2, pair_val) + tuple(kickers[:3])

    # High card
    return (1,) + tuple(vals_desc[:5])

def best_five_card_value(hole, community):
    """Given hole (2 cards) and community (0-5 cards), pick the best 5-card hand.
       Returns (best_rank_tuple, best_hand_cards_list)."""
    cards = list(hole) + list(community)
    if len(cards) < 5:
        # evaluate with padding of lowest possible values (should not normally happen)
        # just return high-card of available cards
        vals_desc = sorted([RANK_VALUE[c[0]] for c in cards], reverse=True)
        return ((1,) + tuple(vals_desc), cards)
    best_rank = None
    best_hand = None
    for combo in itertools.combinations(cards, 5):
        rank = evaluate_5card(combo)
        if best_rank is None or rank > best_rank:
            best_rank = rank
            best_hand = list(combo)
    return best_rank, best_hand

# Poker game evaluation functions END ----------------------------------------------------------

# Poker game route ----------------------------------------------------------------------------------------------------

@app.route('/poker', methods=['GET', 'POST'])
def poker():
    """
    Hold'em-like simple flow vs two AIs:
      - Stages: 'preflop' (initial bet & deal), 'flop', 'turn', 'river', 'showdown'
      - Player bets each betting round (can enter 0 to check). AI always "matches" player's bet.
      - Pot accumulates player contribution + AI matches (we credit full pot size; only player chips tracked).
      - Uses shared session deck via draw_from_deck(), reshuffles automatically when needed.
      - AI hands hidden until showdown.
    """
    if 'chips' not in session:
        session['chips'] = 1000
    ensure_deck()

    default = {
        'stage': 'preflop',        # 'preflop', 'flop', 'turn', 'river', 'showdown'
        'bet': 0,                  # last player bet for display
        'pot': 0,
        'player_hand': [],
        'ai1_hand': [],
        'ai2_hand': [],
        'community': [],           # up to 5 cards
        'round_over': False,
        'result': None,
        'ai1_folded': False,
        'ai2_folded': False,
        'last_raise': 0,
        'to_call': 0,              # amount the player must put up to match last raise
        'awaiting_response': False # True when an AI raised and player must respond
    }

    poker_state = session.get('poker_state', default.copy())
    messages = []

    if request.method == 'POST':
        action = request.form.get('action')

        # Place a bet (used at any active betting stage)
        if action == 'bet':
            try:
                bet_amount = int(request.form.get('bet', 0))
            except (ValueError, TypeError):
                bet_amount = 0

            # If all five community cards are present (stage == 'river'), disallow further bets
            # and force an immediate showdown instead.
            if poker_state.get('stage') == 'river':
                perform_showdown(poker_state, messages)
                session['poker_state'] = poker_state
                return render_template('poker.html',
                                        chips=session.get('chips', 0),
                                        poker=poker_state,
                                        messages=messages)
            
            # If player must respond to an AI raise, handle that first (call/raise)
            if poker_state.get('awaiting_response', False):
                to_call = poker_state.get('to_call', 0)
                # require the player to at least match the to_call
                if bet_amount < to_call:
                    messages.append(f"You must bet at least {to_call} to call the raise.")
                elif bet_amount > session.get('chips', 0):
                    messages.append("Bet exceeds your chips.")
                else:
                    # charge player and add to pot as the response (call or re-raise if amount greater)
                    session['chips'] -= bet_amount
                    poker_state['pot'] = poker_state.get('pot', 0) + bet_amount

                    # If player put more than to_call, treat as a re-raise
                    extra = max(0, bet_amount - to_call)
                    if extra > 0:
                        poker_state['last_raise'] = extra
                        poker_state['to_call'] = extra
                        poker_state['awaiting_response'] = True
                        messages.append(f"You raised by {extra}. Opponents may respond.")
                        # Note: opponents will be given a chance to act on next bet request
                    else:
                        # player called; clear pending raise state
                        poker_state['awaiting_response'] = False
                        poker_state['to_call'] = 0
                        poker_state['last_raise'] = 0
                        messages.append(f"You called the raise of {to_call}.")

                # persist and render current view (don't continue the usual deal/reveal flow)
                session['poker_state'] = poker_state
                return render_template('poker.html',
                                       chips=session.get('chips', 0),
                                       poker=poker_state,
                                       messages=messages)
            
            if bet_amount < 0:
                messages.append("Bet must be 0 or positive.")
            elif bet_amount > session.get('chips', 0):
                messages.append("Bet exceeds your chips.")
            else:
                # Ensure enough cards remain; need up to 11 cards for a full round:
                # 6 hole cards + 5 community
                ensure_deck()
                if len(session.get('deck', [])) < 11 and poker_state['stage'] == 'preflop':
                    session['deck'] = make_deck()
                    session['used_cards'] = []
                    session['show_used'] = False
                    session.modified = True
                    messages.append("Deck reshuffled before dealing.")

                # charge player chips now
                session['chips'] -= bet_amount
                poker_state['bet'] = bet_amount

                # start pot with player's contribution
                pot = poker_state.get('pot', 0) + bet_amount

                # Stage-specific actions (deal / reveal community)
                if poker_state['stage'] == 'preflop':
                    # initial deal: 2 hole cards each and flop community (3)
                    poker_state['player_hand'] = [draw_from_deck(), draw_from_deck()]
                    poker_state['ai1_hand']   = [draw_from_deck(), draw_from_deck()]
                    poker_state['ai2_hand']   = [draw_from_deck(), draw_from_deck()]
                    # deal flop (3 community cards)
                    poker_state['community'] = [draw_from_deck(), draw_from_deck(), draw_from_deck()]
                    poker_state['stage'] = 'flop'
                    poker_state['round_over'] = False
                    poker_state['result'] = None
                    messages.append(f"Dealt. Flop revealed. Bet: {bet_amount}")
                elif poker_state['stage'] == 'flop':
                    # betting at flop, then reveal turn
                    poker_state['community'].append(draw_from_deck())  # turn
                    poker_state['stage'] = 'turn'
                    messages.append(f"Bet {bet_amount} accepted. Turn revealed.")
                elif poker_state['stage'] == 'turn':
                    # betting at turn, then reveal river
                    poker_state['community'].append(draw_from_deck())  # river
                    poker_state['stage'] = 'river'
                    messages.append(f"Bet {bet_amount} accepted. River revealed.")
                elif poker_state['stage'] == 'river':
                    # betting at river; after this player may click showdown
                    messages.append(f"Bet {bet_amount} accepted. You may now Showdown.")
                else:
                    messages.append("Bet accepted.")

                # Simple AI decision function (call / raise / fold) based on hand strength
                def ai_decision(ai_hand, community, bet_amount):
                    ev, _ = best_five_card_value(ai_hand, community)
                    # category is first tuple element (1..9)
                    cat = ev[0] if isinstance(ev, tuple) else ev
                    # probabilities based on category
                    if cat >= 6:         # Flush+ -> strong
                        fold = 0.05; raise_p = 0.25
                    elif cat == 5:       # Straight
                        fold = 0.08; raise_p = 0.18
                    elif cat == 4:       # Trips
                        fold = 0.12; raise_p = 0.12
                    elif cat == 3:       # Two pair
                        fold = 0.18; raise_p = 0.08
                    elif cat == 2:       # One pair
                        fold = 0.25; raise_p = 0.06
                    else:                # High card
                        fold = 0.45; raise_p = 0.02

                    # increase fold chance against very large bets relative to player's chips
                    player_chips = session.get('chips', 0)
                    if bet_amount > max(50, max(1, player_chips // 4)):
                        fold = min(0.95, fold + 0.20)

                    r = random.random()
                    if r < fold:
                        return 'fold', 0
                    elif r < fold + raise_p:
                        # simple raise: 1x or 2x the bet_amount
                        raise_amount = max(1, int(bet_amount * random.choice([1, 2])))
                        return 'raise', raise_amount
                    else:
                        return 'call', 0

                # ensure fold flags exist
                poker_state.setdefault('ai1_folded', False)
                poker_state.setdefault('ai2_folded', False)

                ai_actions = []

                # Run decisions for each AI (if they haven't folded previously)
                if not poker_state.get('ai1_folded', False):
                    # If hands weren't dealt yet (shouldn't happen except for weird flow), handle gracefully
                    if not poker_state.get('ai1_hand'):
                        poker_state['ai1_hand'] = [draw_from_deck(), draw_from_deck()]
                    act1, val1 = ai_decision(poker_state.get('ai1_hand', []), poker_state.get('community', []), bet_amount)
                    if act1 == 'fold':
                        poker_state['ai1_folded'] = True
                        ai_actions.append("AI1 folded")
                    elif act1 == 'call':
                        pot += bet_amount
                        ai_actions.append("AI1 called")
                    else:  # raise
                        # AI matches player's bet and adds its raise
                        pot += bet_amount + val1
                        # record the raise amount and require player to respond
                        poker_state['last_raise'] = max(poker_state.get('last_raise', 0), val1)
                        poker_state['to_call'] = poker_state['last_raise']
                        poker_state['awaiting_response'] = True
                        ai_actions.append(f"AI1 raised by {val1}")

                if not poker_state.get('ai2_folded', False):
                    if not poker_state.get('ai2_hand'):
                        poker_state['ai2_hand'] = [draw_from_deck(), draw_from_deck()]
                    act2, val2 = ai_decision(poker_state.get('ai2_hand', []), poker_state.get('community', []), bet_amount)
                    if act2 == 'fold':
                        poker_state['ai2_folded'] = True
                        ai_actions.append("AI2 folded")
                    elif act2 == 'call':
                        pot += bet_amount
                        ai_actions.append("AI2 called")
                    else:  # raise
                        pot += bet_amount + val2
                        poker_state['last_raise'] = max(poker_state.get('last_raise', 0), val2)
                        poker_state['to_call'] = poker_state['last_raise']
                        poker_state['awaiting_response'] = True
                        ai_actions.append(f"AI2 raised by {val2}")

                poker_state['pot'] = pot

                  # If both AIs folded, player wins immediately
                if poker_state.get('ai1_folded', False) and poker_state.get('ai2_folded', False):
                    # reveal remaining community cards so template indexing is safe
                    reveal_remaining_community(poker_state)

                    session['chips'] += poker_state.get('pot', 0)
                    poker_state['result'] = f"Both opponents folded. You win the pot of {poker_state.get('pot',0)}!"
                    poker_state['stage'] = 'showdown'
                    poker_state['round_over'] = True
                    messages.extend(ai_actions)
                    # save and render immediately to show result
                    session['poker_state'] = poker_state
                    return render_template('poker.html',
                                           chips=session.get('chips', 0),
                                           poker=poker_state,
                                           messages=messages)

                # append AI action messages for UI when not ending round early
                if ai_actions:
                    messages.extend(ai_actions)

        elif action == 'odds':
            # Estimate win/tie/loss odds via Monte Carlo (non-destructive)
            # Lower trial count for interactive speed; increase if you want more accuracy
            trials = 250
            odds = estimate_win_odds(poker_state, trials=trials)
            if odds:
                poker_state['odds'] = odds
                poker_state['show_odds'] = True
                messages.append(f"Estimated odds (based on {odds['trials']} sims): Win {odds['win']*100:.1f}%, Tie {odds['tie']*100:.1f}%, Lose {odds['loss']*100:.1f}%")
            else:
                # provide explicit feedback and still set show_odds so template can display a message
                poker_state['odds'] = {'win': 0.0, 'tie': 0.0, 'loss': 0.0, 'trials': 0}
                poker_state['show_odds'] = True
                messages.append("Could not estimate odds. Ensure you have 2 hole cards dealt and there are enough undealt cards in the deck.")
            # persist state and re-render
            session['poker_state'] = poker_state
            return render_template('poker.html',
                                   chips=session.get('chips', 0),
                                   poker=poker_state,
                                   messages=messages)

        elif action == 'showdown':
            # require that at least river stage reached
            if poker_state.get('stage') not in ('river', 'showdown'):
                messages.append("Showdown allowed only after river.")
            else:
                # ensure full board so evaluator & template can index safely
                reveal_remaining_community(poker_state)

                # evaluate best 5-card hands
                ph = poker_state['player_hand']
                a1 = poker_state['ai1_hand']
                a2 = poker_state['ai2_hand']
                community = poker_state['community']

                ev_p, _ = best_five_card_value(ph, community)
                ev_a1, _ = best_five_card_value(a1, community)
                ev_a2, _ = best_five_card_value(a2, community)

                best_all = max(ev_p, ev_a1, ev_a2)
                winners = []
                if ev_p == best_all:
                    winners.append('player')
                if ev_a1 == best_all:
                    winners.append('ai1')
                if ev_a2 == best_all:
                    winners.append('ai2')

                if 'player' in winners and len(winners) == 1:
                    # player sole winner: award full pot
                    session['chips'] += poker_state.get('pot', 0)
                    poker_state['result'] = f"You win the pot of {poker_state.get('pot',0)}!"
                elif 'player' in winners:
                    # tie including player: split pot between winners, give player's share
                    share = poker_state.get('pot', 0) // len(winners)
                    session['chips'] += share
                    poker_state['result'] = f"Tie. You receive {share} (split among {len(winners)})."
                else:
                    # player lost: nothing to add (bet already deducted)
                    poker_state['result'] = "You lost the pot."

                poker_state['stage'] = 'showdown'
                poker_state['round_over'] = True
                messages.append(poker_state['result'])
            
        elif action == 'fold':
            # Player folds: end the round, reveal AI hands, player forfeits bet
            # Keep chips as-is (bet already deducted when placing bets)
            # Reveal the full board so template indexing is safe
            reveal_remaining_community(poker_state)

            poker_state['stage'] = 'showdown'
            poker_state['round_over'] = True
            poker_state['result'] = "You folded. You forfeit your bet."
            messages.append(poker_state['result'])

        elif action == 'reset_poker':
            poker_state = {
                'stage': 'preflop',
                'bet': 0,
                'pot': 0,
                'player_hand': [],
                'ai1_hand': [],
                'ai2_hand': [],
                'community': [],
                'round_over': False,
                'result': None,
                'ai1_folded': False,
                'ai2_folded': False,
                'last_raise': 0
            }
            messages.append("Poker state reset (chips kept).")

    # save back to session
    session['poker_state'] = poker_state
    return render_template('poker.html',
                           chips=session.get('chips', 0),
                           poker=poker_state,
                           messages=messages)

# Poker game END ----------------------------------------------------------------------------------------------------

@app.route('/reset/<game>')
def reset_game(game):
    # preserve chips by default
    if game == 'blackjack':
        session.pop('player_hand', None)
        session.pop('dealer_hand', None)
        session['bet'] = 0
        session['split'] = False
        session['split_hand'] = []
        session['current_hand'] = 'player'
        session.pop('hand_done', None)
        session['round_over'] = False
        # keep chips as-is
        return redirect(url_for('blackjack'))

    elif game == 'poker':
        session.pop('poker_state', None)
        # optionally clear deck/used cards so poker starts fresh:
        # session.pop('deck', None); session.pop('used_cards', None)
        session['show_used'] = False
        return redirect(url_for('poker'))

    elif game == 'all':
        # clear both games but keep chips
        session.pop('player_hand', None)
        session.pop('dealer_hand', None)
        session['bet'] = 0
        session['split'] = False
        session['split_hand'] = []
        session['current_hand'] = 'player'
        session.pop('hand_done', None)
        session['round_over'] = False

        session.pop('poker_state', None)

        # clear shared deck/used-cards so games start fresh
        session.pop('deck', None)
        session.pop('used_cards', None)
        session['show_used'] = False

        return redirect(url_for('home'))

    # unknown target -> go home
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)