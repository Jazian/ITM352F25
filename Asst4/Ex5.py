
# Ex1. Create a Flask web application that is gambling-themed, this includes a home page and for now a blackjack card game page selectable from the home page.
# Ex2. Add images of the cards being played on the blackjack page instead of just text representation.
# Ex3. Add Chips and Betting System.
# Ex3. If the player runs out of chips, display a game over message and provide an option to restart with a default amount of chips.
# Ex4. Dealer behavior (dealer must hit until reaching a score of 17 or higher).
# Ex4. Handle the split option for pairs in blackjack.
# Ex5. Have cards limited to a standard 52-card deck, reshuffling when the deck is exhausted.
# Ex5. Add a cheat button that allows the player to see cards that have been used in the deck so far reset upon deck reshuffle.

from flask import Flask, render_template, redirect, url_for, request, session
import random

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

@app.route('/reset')
def reset():
    session.pop('player_hand', None)
    session.pop('dealer_hand', None)
    session['bet'] = 0
    session['split'] = False
    session['split_hand'] = []
    session['current_hand'] = 'player'
    session.pop('hand_done', None)
    session['round_over'] = False   # reset round flag
    if session.get('chips', 0) <= 0:
        session['chips'] = 1000
    return redirect(url_for('blackjack'))

if __name__ == '__main__':
    app.run(debug=True)