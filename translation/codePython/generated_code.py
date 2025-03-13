import threading

# Автоматично згенерований код

# Спільні змінні
x = 12
y = 0
z = 0

lock = threading.Lock()

def thread_Diagram_1():
    with lock:
        # Початок виконання
        y = 10
        x = y
        print('x =', x)
        # Кінець виконання

def thread_Diagram_2():
    with lock:
        # Початок виконання
        x = int(input('Enter value for x: '))
        if x == 10:
            print('x =', x)
        else:
            print('y =', y)
        print('z =', z)
        # Кінець виконання

def thread_Diagram_3():
    with lock:
        # Початок виконання
        y = 1
        while True:
            if y < 5:
                print('y =', y)
            else:
                print('x =', x)
            x = int(input('Enter value for x: '))

def thread_Diagram_4():
    with lock:
        # Початок виконання
        while True:
            y = 1
            print('y =', y)
            print('x =', x)
            x = int(input('Enter value for x: '))

if __name__ == "__main__":
    t_Diagram_1 = threading.Thread(target=thread_Diagram_1)
    t_Diagram_1.start()
    t_Diagram_2 = threading.Thread(target=thread_Diagram_2)
    t_Diagram_2.start()
    t_Diagram_3 = threading.Thread(target=thread_Diagram_3)
    t_Diagram_3.start()
    t_Diagram_4 = threading.Thread(target=thread_Diagram_4)
    t_Diagram_4.start()

    for t in threading.enumerate():
        if t is not threading.current_thread():
            t.join()
