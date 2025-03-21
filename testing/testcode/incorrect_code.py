# sometimes_correct.py
import threading
import time
import random

# Спільна змінна
V = 0

def thread1():
    global V
    # Невелика затримка з випадковим часом
    time.sleep(random.random() * 0.1)
    V = 10

def thread2():
    global V
    # Невелика затримка з випадковим часом
    time.sleep(random.random() * 0.1)
    V = 5

# Створюємо та запускаємо два потоки
t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)
t1.start()
t2.start()

# Чекаємо на завершення обох потоків
t1.join()
t2.join()

# Виводимо кінцеве значення V
print(V)
