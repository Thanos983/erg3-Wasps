import random
import math


class Bomb:
    """
    Class Bomb consist of 1 bomb with x,y and a count that indicates
    how many wasps has the bomb killed
    """

    def __init__(self, x1, y1):
        self.x1 = x1
        self.y1 = y1
        self.count = 0

    def getX(self):
        return self.x1, self.y1

    def fitness(self, dmax, nests, number_of_nests):
        """

        :param dmax: Maximum Distance
        :param nests: Coordinates of nests
        :param number_of_nests: Population of nests
        :return: How many kills did this bomb to all nests
        """

        kills = 0
        distance = 0
        for i in range(1, number_of_nests+1):
            distance += ((nests[i][0] - self.x1) ** 2 + (nests[i][1] - self.y1) ** 2)
            damage = int(nests[i][2] * (dmax / (20 * distance + 0.00001)))  # Many zeros occur due to truncation

            if damage > nests[i][2]:
                nests[i][2] = 0
            else:
                nests[i][2] -= damage

            kills += damage

        print(int(kills))
        return int(kills)


class Solution:
    """
    Solution consist of a list with 3 bombs
    """
    bombPos = []

    def __init__(self, x1, y1, x2, y2, x3, y3):
        Solution.bombPos.append(Bomb(x1, y1))
        Solution.bombPos.append(Bomb(x2, y2))
        Solution.bombPos.append(Bomb(x3, y3))
        self.fitness = 0

    def get_Pos(self):
        return self.bombPos

    def SolutionFitness(self, nests, numberOfNests):
        """

        :param dmax: Maximum distance of nests
        :param nests: dictionary containing coordinates of nest
        :param numberOfNests: how many nests exist
        :return: How many death of wasps occur by this solution
        """
        dmax = maxDistance(nests, numberOfNests)

        count = 0

        for i in range(3):  # Number of bombs
            count += self.bombPos[i].fitness(dmax, nests, numberOfNests)

        self.fitness = count


def maxDistance(nest, numberOfNests):
    """
    Finds the maximum distance(dmax) between nests
    Input: a dictionary with nests coordinates and the number of nests
    Output: maximum distance (dmax)
    """
    dmax = -1

    for p in range(1, numberOfNests + 1):
        for k in range(p + 1, numberOfNests + 1):
            distance = math.sqrt((nest[p][0] - nest[k][0]) ** 2 + (nest[p][1] - nest[k][1]) ** 2)

            if distance > dmax:
                dmax = distance

    return int(dmax * 1000) / 1000  # Truncates dmax to 3 digits precision


def main():
    NubmerOfBombs = 3

    # reading nests co-ordinates from a txt
    nests = {}
    count = 0

    with open("nests.txt", "r") as file:
        for line in file:
            reader = line.split()
            count += 1
            nests[count] = [int(reader[0]), int(reader[1]), int(reader[2])]

    x_axis = []
    y_axis = []
    numberOfWasps = []

    # pass nests coordinates in separate lists
    for c in range(1, count + 1):
        x_axis.append(nests[c][0])
        y_axis.append(nests[c][1])
        numberOfWasps.append(nests[c][2])

    # Visualize nests
    # mp.plot(x_axis, y_axis, 'mD')
    # mp.axis([0, 100, 0, 100])
    # mp.show()

    # Populate bombs with random population. Will have 6 float numbers with 3 digit precision

    bombs = []
    population = 5  # Preferable population 100000

    for i in range(population):  # Preferable range 100000
        randomBomb = random.sample(range(100000), 6)
        randomBomb[:] = [x / 1000 for x in randomBomb]

        bombs.append(Solution(randomBomb[0], randomBomb[1], randomBomb[2], randomBomb[3], randomBomb[4], randomBomb[5]))

    testVar = bombs[0].get_Pos()[0].getX()[1]
    # Finally got it. Accessed into a variable of class bomb

    test = bombs[0].SolutionFitness(nests, count)

    dmax = maxDistance(nests, count)

    print(nests)

if __name__ == '__main__':
    main()
