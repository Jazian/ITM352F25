# Create a Flask web application that is gambling-themed, this includes a home page and for now a blackjack card game page selectable from the home page.
# Add images of the cards being played on the blackjack page instead of just text representation.
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

# Function to deal a card
def deal_card():
    rank = random.choice(list(ranks.keys()))
    suit = random.choice(suits)
    filename = f"{rank}_of_{suit}.svg"   # matches files in static/cards/
    return (rank, suit, filename)

# Function to calculate the score of a hand
def calculate_score(hand):
    score = sum(ranks[card[0]] for card in hand)  # card[0] = rank
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
    if 'player_hand' not in session:
        session['player_hand'] = [deal_card(), deal_card()]
        session['dealer_hand'] = [deal_card(), deal_card()]

    player_hand = session['player_hand']
    dealer_hand = session['dealer_hand']

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    hide_dealer = True   # default: hide dealer’s second card

    if request.method == 'POST':
        action = request.form.get('action')
        # Hit action
        if action == 'hit':
            player_hand.append(deal_card())
            session['player_hand'] = player_hand
            player_score = calculate_score(player_hand)
            if player_score > 21:
                # bust: still hide dealer’s second card
                return render_template('blackjack.html',
                                       player_hand=player_hand,
                                       dealer_hand=dealer_hand,
                                       player_score=player_score,
                                       dealer_score=dealer_score,
                                       result="You busted!",
                                       hide_dealer=True)
        # Stand action
        elif action == 'stand':
            # reveal dealer’s hand
            hide_dealer = False
            while dealer_score < 17:
                dealer_hand.append(deal_card())
                dealer_score = calculate_score(dealer_hand)
            session['dealer_hand'] = dealer_hand

            if dealer_score > 21 or player_score > dealer_score:
                result = "You win!"
            elif player_score == dealer_score:
                result = "It's a tie!"
            else:
                result = "Dealer wins!"
            return render_template('blackjack.html',
                                   player_hand=player_hand,
                                   dealer_hand=dealer_hand,
                                   player_score=player_score,
                                   dealer_score=dealer_score,
                                   result=result,
                                   hide_dealer=False)

    # default render (initial deal or after hit)
    return render_template('blackjack.html',
                           player_hand=player_hand,
                           dealer_hand=dealer_hand,
                           player_score=player_score,
                           dealer_score=dealer_score,
                           result=None,
                           hide_dealer=hide_dealer)

# Reset the game
@app.route('/reset')
def reset():
    session.pop('player_hand', None)
    session.pop('dealer_hand', None)
    return redirect(url_for('blackjack'))

if __name__ == '__main__':
    app.run(debug=True)

