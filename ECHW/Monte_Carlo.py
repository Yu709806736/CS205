import random
import matplotlib.pyplot as plt
import math
from typing import List

origin = [0.0, 0.0]
host = [0.0, 250.0]
smell = 50.0
fly = 250.0
red = 1000.0
test = 10000
days = 100


def dis(pt1: List[float], pt2: List[float]) -> float:
    return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)


if __name__ == '__main__':
    found = 0
    die_outside = 0
    days_coor = [i for i in range(1, days+1)]
    found_days = [0 for _ in range(days+1)]
    # for d in range(1, days+1):
    for j in range(test):
        cur = origin
        for i in range(1, days+1):
            if dis(cur, host) <= smell:
                # print('The mosquito finds the host on day {0}!'.format(i))
                # found += 1
                found_days[i] += 1
                break
            angle = random.random() * 2 * math.pi
            # print(angle)
            cur = [cur[0] + 250 * math.cos(angle), cur[1] + 250 * math.sin(angle)]
            # print('day {0} at {1}'.format(i, cur))
        # else:
        #     if dis(cur, origin) >= red:
        #         # print('The mosquito dies outside the red region!')
        #         die_outside += 1
        #     else:
        #         pass
                # print('The mosquito dies in the red area!')

    # print('the probability that the mosquito will find the host before she dies '
    #       'is approximately {0}'.format(found / test))
    # print('the probability that the mosquito will die outside the red region '
    #       'is approximately {0}'.format(die_outside / test))

    for i in range(1, len(found_days)):
        found_days[i] += found_days[i-1]

    for i in range(1, len(found_days)):
        found_days[i] /= test

    plt.plot(days_coor[1:], found_days[2:])
    plt.title('Probability that she finds the host by day K')
    plt.xlabel('Day K')
    plt.ylabel('Probability')
    plt.savefig('Probability-Day.jpg')
    plt.show()