import random

def assign_number_pair():
    numbers = list(range(1, 11))  # Numbers from 1 to 10

    # Step 1: Pick a random number R1
    r1 = random.choice(numbers)

    # Step 2: Remove R1 and pick a second random number R2
    remaining = [n for n in numbers if n != r1]
    r2 = random.choice(remaining)

    # Step 3: Return the pair
    return r1, r2

assigned_pair = assign_number_pair()
print("Assigned numbers:", assigned_pair)
