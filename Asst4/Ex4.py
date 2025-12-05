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

# Card deck setup
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Deal a card
def deal_card():
    rank = random.choice(list(ranks.keys()))
    suit = random.choice(suits)
    filename = f"{rank}_of_{suit}.svg"
    return (rank, suit, filename)

# Calculate the score of a hand
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

# Blackjack game
@app.route('/blackjack', methods=['GET', 'POST'])
def blackjack():
    if 'chips' not in session:
        session['chips'] = 1000
    if 'bet' not in session:
        session['bet'] = 0
    if 'player_hand' not in session:
        session['player_hand'] = []
        session['dealer_hand'] = []

    player_hand = session['player_hand']
    dealer_hand = session['dealer_hand']

    player_score = calculate_score(player_hand) if player_hand else 0
    dealer_score = calculate_score(dealer_hand) if dealer_hand else 0

    hide_dealer = True
    result = None

    # No chips? = Broke
    # Game Over check if no chips and no bet is placed
    if session['chips'] <= 0 and session['bet'] == 0:
        result = "You're out of chips! Game over."
        return render_template('blackjack.html',
                               player_hand=[],
                               dealer_hand=[],
                               player_score=0,
                               dealer_score=0,
                               result=result,
                               hide_dealer=True,
                               chips=session['chips'],
                               bet=session['bet'])

    if request.method == 'POST':
        action = request.form.get('action')

        # Placing bet == Deal cards
        if action == 'bet':
            bet_amount = int(request.form.get('bet'))
            if bet_amount <= session['chips']:
                session['bet'] = bet_amount
                session['chips'] -= bet_amount
                session['player_hand'] = [deal_card(), deal_card()]
                session['dealer_hand'] = [deal_card(), deal_card()]
                player_hand = session['player_hand']
                dealer_hand = session['dealer_hand']
                player_score = calculate_score(player_hand)
                dealer_score = calculate_score(dealer_hand)
            
            if player_score > 21:
                result = "You busted!"
                session['bet'] = 0
                return render_template('blackjack.html',
                                    player_hand=player_hand,
                                    dealer_hand=dealer_hand,
                                    player_score=player_score,
                                    dealer_score=dealer_score,
                                    result=result,
                                    hide_dealer=True,
                                    chips=session['chips'],
                                    bet=session['bet'])

            # Check for immediate blackjack
            if player_score == 21 or dealer_score == 21:
                hide_dealer = False
                if player_score == 21 and dealer_score == 21:
                    result = "Both have Blackjack! It's a tie!"
                    session['chips'] += session['bet']  # return bet
                elif player_score == 21:
                    result = "Blackjack! You win!"
                    session['chips'] += session['bet'] * 2
                else:
                    result = "Dealer has Blackjack! Dealer wins!"
                session['bet'] = 0

                return render_template('blackjack.html',
                                    player_hand=player_hand,
                                    dealer_hand=dealer_hand,
                                    player_score=player_score,
                                    dealer_score=dealer_score,
                                    result=result,
                                    hide_dealer=False,
                                    chips=session['chips'],
                                    bet=session['bet'])


        # Hit action
        elif action == 'hit':
            player_hand.append(deal_card())
            session['player_hand'] = player_hand
            player_score = calculate_score(player_hand)

            if player_score > 21:
                result = "You busted!"
                session['bet'] = 0
                return render_template('blackjack.html',
                                    player_hand=player_hand,
                                    dealer_hand=dealer_hand,
                                    player_score=player_score,
                                    dealer_score=dealer_score,
                                    result=result,
                                    hide_dealer=True,
                                    chips=session['chips'],
                                    bet=session['bet'])

            # Check for blackjack after hit
            if player_score == 21:
                hide_dealer = False
                while dealer_score < 17:
                    dealer_hand.append(deal_card())
                    dealer_score = calculate_score(dealer_hand)
                session['dealer_hand'] = dealer_hand

                if dealer_score > 21 or player_score > dealer_score:
                    result = "You win!"
                    session['chips'] += session['bet'] * 2
                elif player_score == dealer_score:
                    result = "It's a tie!"
                    session['chips'] += session['bet']
                else:
                    result = "Dealer wins!"
                session['bet'] = 0

                return render_template('blackjack.html',
                                    player_hand=player_hand,
                                    dealer_hand=dealer_hand,
                                    player_score=player_score,
                                    dealer_score=dealer_score,
                                    result=result,
                                    hide_dealer=False,
                                    chips=session['chips'],
                                    bet=session['bet'])


        # Stand action
        elif action == 'stand':
            hide_dealer = False
            while dealer_score < 17:
                dealer_hand.append(deal_card())
                dealer_score = calculate_score(dealer_hand)
            session['dealer_hand'] = dealer_hand

            if dealer_score > 21 or player_score > dealer_score:
                result = "You win!"
                session['chips'] += session['bet'] * 2
            elif player_score == dealer_score:
                result = "It's a tie!"
                session['chips'] += session['bet']
            else:
                result = "Dealer wins!"
            session['bet'] = 0

            return render_template('blackjack.html',
                                   player_hand=player_hand,
                                   dealer_hand=dealer_hand,
                                   player_score=player_score,
                                   dealer_score=dealer_score,
                                   result=result,
                                   hide_dealer=False,
                                   chips=session['chips'],
                                   bet=session['bet'])

    return render_template('blackjack.html',
                           player_hand=player_hand,
                           dealer_hand=dealer_hand,
                           player_score=player_score,
                           dealer_score=dealer_score,
                           result=result,
                           hide_dealer=hide_dealer,
                           chips=session['chips'],
                           bet=session['bet'])

# Reset the game
@app.route('/reset')
def reset():
    # Always clear hands and bet
    session.pop('player_hand', None)
    session.pop('dealer_hand', None)
    session['bet'] = 0

    # Only reset chips if player is out
    if session.get('chips', 0) <= 0:
        session['chips'] = 1000

    return redirect(url_for('blackjack'))

if __name__ == '__main__':
    app.run(debug=True)
