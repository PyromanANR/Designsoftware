# Автоматично згенерований код

# Спільні змінні
x = 12
y = 0
z = 0

def thread_Diagram_1():
    # Початок виконання
    y = 10
    x = y
    print('x =', x)
    # Кінець виконання

def thread_Diagram_2():
    # Початок виконання
    x = int(input('Enter value for x: '))
    if x == 10:
        print('x =', x)
    else:
        print('y =', y)
    print('x =', x)
    print('y =', y)
    print('z =', z)
    # Кінець виконання

def thread_Diagram_3():
    # Початок виконання
    y = 1
    while True:
        if y < 5:
            print('y =', y)
        else:
            print('x =', x)
        print('y =', y)
        print('x =', x)
        x = int(input('Enter value for x: '))

def thread_Diagram_4():
    # Початок виконання
    while True:
        y = 1
        print('y =', y)
        print('x =', x)
        x = int(input('Enter value for x: '))

if __name__ == "__main__":
    thread_Diagram_1()
    thread_Diagram_2()
    thread_Diagram_3()
    thread_Diagram_4()
