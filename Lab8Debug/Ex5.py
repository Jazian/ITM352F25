def fibonacci(list):
    Fibo = list[0, 1]
    for val in list:
        Fibo = Fibo.append(Fibo[-1] + val)
    return Fibo

my_list = [1, 2, 3, 4, 5]
print(fibonacci(my_list)) 
