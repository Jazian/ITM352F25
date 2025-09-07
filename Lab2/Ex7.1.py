def FtoC(degreesF, decimal_places=0):
    degreesF_float = float(degreesF)
    degreesC = (degreesF_float - 32) * 5.0/9.0
    degreesC = round(degreesC, decimal_places)
    return degreesC

degreesF = input("Enter a temperature in degrees Fahrenheit: ")
degreesC = FtoC(degreesF, 1)

print(f"{degreesF} degrees Fahrenheit is {degreesC} degrees Celsius")