def fibonacci(list):
    Fibo = [0, 1]
    for val in list:
        Fibo.append(Fibo[-1] + Fibo[-2])
    return Fibo

my_list = [1, 2, 3, 4, 5]
print(fibonacci(my_list)) 
