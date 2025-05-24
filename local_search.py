import random
import math


# Визначення функції Сфери
def sphere_function(x):
    """
    Обчислює значення функції Сфери для заданих координат.
    Функція Сфери: f(x) = sum(xi^2)
    """
    return sum(xi ** 2 for xi in x)


# Допоміжна функція для генерації сусідньої точки
def get_neighbor(current_solution, bounds, step_size=0.1):
    """
    Генерує сусідню точку шляхом випадкового зсуву по одній з координат.
    """
    num_dimensions = len(current_solution)
    neighbor = list(current_solution)

    # Випадково обираємо вимір для зміни
    dim_to_change = random.randint(0, num_dimensions - 1)

    # Випадково обираємо напрямок (збільшення або зменшення)
    change_direction = random.choice([-1, 1])

    # Змінюємо значення у вибраному вимірі
    neighbor[dim_to_change] += change_direction * step_size

    # Перевіряємо та обмежуємо значення в межах
    min_bound, max_bound = bounds[dim_to_change]
    neighbor[dim_to_change] = max(min_bound, min(max_bound, neighbor[dim_to_change]))

    return neighbor


# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    """
    Реалізує алгоритм "Підйом на гору" (Hill Climbing).

    Параметри:
    func: функція, яку потрібно мінімізувати.
    bounds: список кортежів (min, max) для кожної змінної.
    iterations: максимальна кількість ітерацій.
    epsilon: поріг для зупинки алгоритму.

    Повертає:
    Оптимальна точка (список координат x) та значення функції в цій точці.
    """
    num_dimensions = len(bounds)

    # Ініціалізація початкового випадкового розв'язку
    current_solution = [random.uniform(b[0], b[1]) for b in bounds]
    current_value = func(current_solution)

    for i in range(iterations):
        # Генеруємо сусідню точку
        neighbor_solution = get_neighbor(current_solution, bounds)
        neighbor_value = func(neighbor_solution)

        # Якщо сусідня точка краща, переходимо до неї
        if neighbor_value < current_value:
            # Перевіряємо умову зупинки за epsilon
            if abs(current_value - neighbor_value) < epsilon:
                break
            current_solution = neighbor_solution
            current_value = neighbor_value
        else:
            # Якщо сусідня точка не краща, залишаємось на місці.
            # Це може призвести до застрягання в локальному мінімумі.
            pass

    return current_solution, current_value


# Random Local Search
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    """
    Реалізує алгоритм "Випадковий локальний пошук".

    Параметри:
    func: функція, яку потрібно мінімізувати.
    bounds: список кортежів (min, max) для кожної змінної.
    iterations: максимальна кількість ітерацій.
    epsilon: поріг для зупинки алгоритму.

    Повертає:
    Оптимальна точка (список координат x) та значення функції в цій точці.
    """
    num_dimensions = len(bounds)

    # Ініціалізація початкового випадкового розв'язку
    best_solution = [random.uniform(b[0], b[1]) for b in bounds]
    best_value = func(best_solution)

    for i in range(iterations):
        # Генеруємо сусідню точку (випадково, але в межах)
        # Random Local Search може генерувати сусіда далеко, або близько.
        # Для простоти, використаємо той же get_neighbor, але можна було б і просто
        # згенерувати повністю нову випадкову точку в межах.
        current_solution = [random.uniform(b[0], b[1]) for b in bounds]
        current_value = func(current_solution)

        # Якщо поточний випадковий розв'язок кращий за найкращий, оновлюємо
        if current_value < best_value:
            # Перевіряємо умову зупинки за epsilon
            if abs(best_value - current_value) < epsilon:
                break
            best_solution = current_solution
            best_value = current_value

    return best_solution, best_value


# Simulated Annealing
def simulated_annealing(func, bounds, iterations=1000, temp=1000, cooling_rate=0.95, epsilon=1e-6):
    """
    Реалізує алгоритм "Імітація відпалу" (Simulated Annealing).

    Параметри:
    func: функція, яку потрібно мінімізувати.
    bounds: список кортежів (min, max) для кожної змінної.
    iterations: максимальна кількість ітерацій.
    temp: початкова температура.
    cooling_rate: швидкість охолодження (коефіцієнт зменшення температури).
    epsilon: поріг для зупинки алгоритму (для температури).

    Повертає:
    Оптимальна точка (список координат x) та значення функції в цій точці.
    """
    num_dimensions = len(bounds)

    # Ініціалізація початкового випадкового розв'язку
    current_solution = [random.uniform(b[0], b[1]) for b in bounds]
    current_value = func(current_solution)

    best_solution = list(current_solution)
    best_value = current_value

    for i in range(iterations):
        # Умова зупинки за температурою
        if temp < epsilon:
            break

        # Генеруємо сусідню точку
        neighbor_solution = get_neighbor(current_solution, bounds)
        neighbor_value = func(neighbor_solution)

        # Обчислюємо різницю значень
        delta_e = neighbor_value - current_value

        # Якщо сусідня точка краща або приймаємо гіршу точку з певною ймовірністю
        if delta_e < 0 or random.random() < math.exp(-delta_e / temp):
            current_solution = neighbor_solution
            current_value = neighbor_value

            # Оновлюємо найкращий розв'язок
            if current_value < best_value:
                best_solution = list(current_solution)
                best_value = current_value

        # Зменшуємо температуру
        temp *= cooling_rate

    return best_solution, best_value


if __name__ == "__main__":
    # Межі для функції Сфери: xi ∈ [-5, 5] для кожного параметра xi
    bounds = [(-5, 5), (-5, 5)]  # Для двовимірної функції

    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", [round(x, 8) for x in hc_solution], "Значення:", round(hc_value, 8))

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", [round(x, 8) for x in rls_solution], "Значення:", round(rls_value, 8))

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print("Розв'язок:", [round(x, 8) for x in sa_solution], "Значення:", round(sa_value, 8))