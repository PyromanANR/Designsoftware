# correct_mt.py
import threading

# Глобальна спільна змінна
V = 0

def update_variable():
    global V
    # Симулюємо операцію: присвоєння 10 (навіть якщо V початково 0)
    V = 10
    print(V)

# Створюємо потік, який оновлює змінну та виводить її
t = threading.Thread(target=update_variable)
t.start()
t.join()
