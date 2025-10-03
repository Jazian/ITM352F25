hits, spins = 4, 7  

messages = [
    "Get going!",       
    "On your way!",     
    "Almost there!",    
    "You win!"          
]

index = (spins != 0) * (
    (hits / spins > 0) +
    (hits / spins >= 0.25) +
    ((hits / spins >= 0.5) and (hits < spins))
)

print(messages[index])