def check_budget(purchases, budget):
    total_spent = sum(purchases)
    if total_spent > budget:
        return f"You spent ${total_spent} and that is over your budget of ${budget}"
    else:
        return f"You spent ${total_spent} and that is within your budget of ${budget}"

def test_check_budget(check_budget):
    # Test Case 1: Over budget
    purchases1 = [36.13, 23.87, 183.35, 22.93, 11.62]
    budget1 = 50
    assert check_budget(purchases1, budget1) == \
        "You spent $277.90 and that is over your budget of $50.00"

    # Test Case 2: Exactly at budget
    purchases2 = [20.00, 30.00]
    budget2 = 50
    assert check_budget(purchases2, budget2) == \
        "You spent $50.00 and that is within your budget of $50.00"

    # Test Case 3: Under budget
    purchases3 = [10.00, 15.00]
    budget3 = 50
    assert check_budget(purchases3, budget3) == \
        "You spent $25.00 and that is within your budget of $50.00"

    # Test Case 4: Empty purchases
    purchases4 = []
    budget4 = 50
    assert check_budget(purchases4, budget4) == \
        "You spent $0.00 and that is within your budget of $50.00"

    print("All test cases passed!")

test_check_budget(check_budget)