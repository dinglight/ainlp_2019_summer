from sklearn.datasets import load_boston

import random

data = load_boston()
x,y = data['data'], data['target']
x_rm = x[:,5]

def price(rm, k, b):
    return k*rm+b

def loss(y, y_hat):
    return sum((y_i - y_hat_i)**2 for y_i, y_hat_i in zip(list(y), list(y_hat))) / len(list(y))

def random_find_k_b(trying_times):
    min_loss = float('inf')
    best_k, best_b = None, None

    for i in range(trying_times):
        k = random.random() * 200 - 100
        b = random.random() * 200 - 100
        price_by_random_k_and_b = [price(r, k, b) for r in x_rm]

        current_loss = loss(y, price_by_random_k_and_b)

        if current_loss < min_loss:
            min_loss = current_loss
            best_k, best_b = k, b
            print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, best_k, best_b, min_loss))
    return best_k, best_b

direction = [
    (+1, -1),  # first element: k's change direction, second element: b's change direction
    (+1, +1),
    (-1, -1),
    (-1, +1),
]

def supervised_find_k_b(trying_times):
    min_loss = float('inf')
    best_k = random.random() * 200 - 100
    best_b = random.random() * 200 - 100

    next_direction = random.choice(direction)

    scalar = 1.0

    for i in range(trying_times):
        k_direction, b_direction = next_direction
        current_k, current_b = best_k + k_direction * scalar, best_b + b_direction * scalar
        price_by_k_and_b = [price(r, current_k, current_b) for r in x_rm]
        current_loss = loss(y, price_by_k_and_b)

        if current_loss < min_loss: # performance became better
            min_loss = current_loss
            best_k, best_b = current_k, current_b

            next_direction = next_direction
            print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, best_k, best_b, min_loss))
        else:
            next_direction = random.choice(direction)
    return best_k, best_b
