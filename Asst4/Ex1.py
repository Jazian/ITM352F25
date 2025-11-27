# Create a Flask web application that is gambling-themed, this includes a home page and for now a blackjack card game page selectable from the home page.
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
    return (rank, suit)

# Function to calculate the score of a hand
def calculate_score(hand):
    score = sum(ranks[card[0]] for card in hand)
    # Adjust for Aces
    aces = sum(1 for card in hand if card[0] == 'A')
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

@app.route('/')
def home():
    return render_template('home.html')

# Blackjack game route
@app.route('/blackjack', methods=['GET', 'POST'])
def blackjack():
    if 'player_hand' not in session:
        session['player_hand'] = [deal_card(), deal_card()]
        session['dealer_hand'] = [deal_card(), deal_card()]

    player_hand = session['player_hand']
    dealer_hand = session['dealer_hand']

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    # Handle player actions
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'hit':
            player_hand.append(deal_card())
            session['player_hand'] = player_hand
            player_score = calculate_score(player_hand)
            if player_score > 21:
                return render_template('blackjack.html',
                                       player_hand=player_hand,
                                       dealer_hand=dealer_hand,
                                       player_score=player_score,
                                       dealer_score=dealer_score,
                                       result="Bust! Dealer wins.")

        # Handle stand action
        elif action == 'stand':
            while dealer_score < 17:
                dealer_hand.append(deal_card())
                dealer_score = calculate_score(dealer_hand)
            session['dealer_hand'] = dealer_hand
            # Determine the winner
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
                                   result=result)

    return render_template('blackjack.html',
                           player_hand=player_hand,
                           dealer_hand=dealer_hand,
                           player_score=player_score,
                           dealer_score=dealer_score,
                           result=None)


# Route to reset the game
@app.route('/reset')
def reset():
    session.pop('player_hand', None)
    session.pop('dealer_hand', None)
    return redirect(url_for('blackjack'))

if __name__ == '__main__':
    app.run(debug=True)
