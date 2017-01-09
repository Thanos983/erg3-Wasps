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

    def fitness(self, cnests):
        """

        :param dmax: Maximum Distance
        :param cnests: Coordinates of nests
        :param number_of_nests: NumberOfSolutions of nests
        :return: How many kills did this bomb to all nests
        """
        dmax = maxDistance(cnests)
        kills = 0
        distance = 0
        damage = 0

        for i in range(1, cnests.__len__()+1):
            distance = math.sqrt((cnests[i][0] - self.x1) ** 2 + (cnests[i][1] - self.y1) ** 2)
            damage = round(cnests[i][2] * dmax / (20 * distance + 0.00001))  # Many zeros occur due to truncation

            if damage > cnests[i][2]:
                cnests[i][2] = 0
            else:
                cnests[i][2] -= damage
                self.count += damage

        return self.count


class Solution:
    """
    Solution consist of a list with 3 bombs
    """
    bombPos = []

    def __init__(self, x1, y1, x2, y2, x3, y3, cnests):
        self.bombPos.append(Bomb(x1, y1))
        self.bombPos.append(Bomb(x2, y2))
        self.bombPos.append(Bomb(x3, y3))
        self.fitness = self.SolutionFitness(cnests)

    def get_Pos(self):
        return self.bombPos

    def SolutionFitness(self, cnests):
        """

        :param dmax: Maximum distance of nests
        :param cnests: dictionary containing coordinates of nest
        :param numberOfNests: how many nests exist
        :return: How many death of wasps occur by this solution
        """

        count = 0

        for i in range(3):  # Number of bombs
            count += self.bombPos[i].fitness(cnests)

        return count


def maxDistance(nest):
    """
    Finds the maximum distance(dmax) between nests
    Input: a dictionary with nests coordinates and the number of nests
    Output: maximum distance (dmax)
    """
    dmax = -1

    for p in range(1, nest.__len__() + 1):
        for k in range(p + 1, nest.__len__() + 1):
            distance = math.sqrt((nest[p][0] - nest[k][0]) ** 2 + (nest[p][1] - nest[k][1]) ** 2)

            if distance > dmax:
                dmax = distance

    return int(dmax * 1000) / 1000  # Truncates dmax to 3 digits precision


def openFile():
    """
    Opens the file and returns a dictionary with the coordinates of nest and the number of bees inside
    """

    anests = {}
    count = 0
    count = 0

    with open("nests.txt", "r") as file:
        for line in file:
            reader = line.split()
            count += 1
            anests[count] = [int(reader[0]), int(reader[1]), int(reader[2])]

    return anests


def visualiseNests(nests):

    # Separate x,y values in order to create a graph of nests
    x_axis = []
    y_axis = []
    number_of_wasps = []

    # pass nests coordinates in separate lists
    for c in range(1, nests.__len__):
        x_axis.append(nests[c][0])
        y_axis.append(nests[c][1])
        number_of_wasps.append(nests[c][2])

    # Visualize nests
    # mp.plot(x_axis, y_axis, 'mD')
    # mp.axis([0, 100, 0, 100])
    # mp.show()


def main():
    nubmerofbombs = 3

    # reading nests co-ordinates from a txt
    nests = openFile()

    bombs = []
    NumberOfSolutions = 3  # Preferable NumberOfSolutions 100000

    # Populate bombs with random NumberOfSolutions. Will have 6 float numbers with 3 digit precision
    for i in range(NumberOfSolutions):  # Preferable range 100000
        randomBomb = random.sample(range(100000), 6)
        randomBomb[:] = [x / 1000 for x in randomBomb]
        copy_nests = nests.copy()
        bombs.append(Solution(randomBomb[0], randomBomb[1], randomBomb[2], randomBomb[3], randomBomb[4], randomBomb[5], copy_nests))
        print(nests)
        print(copy_nests)
        print()

    testVar = bombs[0].get_Pos()[0].getX()[1]
    # Finally got it. Accessed into a variable of class bomb

    for i in range(NumberOfSolutions):
        print(bombs[i].fitness)

if __name__ == '__main__':
    main()
