###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
import copy
def dp_make_weight(egg_weights, target_weight, memo = {}):
    dp_egg = []
    combination = []
    for i in range(1000):
        dp_egg.append(-1)
    dp_egg[0] = 0
    combination.append((0,[0]))
    for w in range(1,target_weight+1):
        min_num = 9999
        for egg in egg_weights:
            if egg <= w:
                temp_num = dp_egg[w-egg] + 1 #状态转移方程
                if temp_num < min_num:
                    min_num = temp_num
                    add_egg = egg
                    temp_comb = copy.deepcopy(combination[w-egg][1])
                    temp_comb.append(add_egg)
        dp_egg[w] = min_num
        combination.append((w,temp_comb))
    return dp_egg[w]
# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    egg_weights = (1, 5, 10, 50)
    n = 100
    print("Egg weights = (1, 50, 95)")
    print("n = 100")
    print("Expected ouput: 2 (2 * 50 = 100)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    egg_weights = (1, 9, 25, 30, 35, 40, 45, 92)
    n = 98
    print("Egg weights = (1, 9, 25, 30, 35, 40, 45, 92)")
    print("n = 98")
    print("Expected ouput: 4 (9 * 2 + 35 + 45 = 98)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()