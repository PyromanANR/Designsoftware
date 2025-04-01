import threading

# Автоматично згенерований код

# Спільні змінні
x = 12
y = 0
z = 0
A = 5
B = 2

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
        A = int(input())
        if A == 5:
            print('A =', A)
        else:
            print('B =', B)
        # Кінець виконання

def thread_Diagram_3():
    with lock:
        # Початок виконання
        while True:
            y = 1
            print('y =', y)
            print('x =', x)
            x = int(input())

if __name__ == "__main__":
    t_Diagram_1 = threading.Thread(target=thread_Diagram_1)
    t_Diagram_1.start()
    t_Diagram_2 = threading.Thread(target=thread_Diagram_2)
    t_Diagram_2.start()
    t_Diagram_3 = threading.Thread(target=thread_Diagram_3)
    t_Diagram_3.start()

    for t in threading.enumerate():
        if t is not threading.current_thread():
            t.join()
