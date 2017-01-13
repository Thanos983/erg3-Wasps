import random
import math

try:
    import operator
except ImportError:
    print("Warning: No operator is imported.\n Install operator for better performance \n")
    key_fun = lambda sol: sol.fitness  # Use lamba if no operator is imported
else:
    key_fun = operator.attrgetter("fitness")


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

        :param cnests: Coordinates of nests
        :return: How many kills did this bomb to all nests
        """
        dmax = maxDistance(cnests)

        for i in range(1, cnests.__len__() + 1):
            distance = math.sqrt((cnests[i][0] - self.x1) ** 2 + (cnests[i][1] - self.y1) ** 2)
            damage = round(cnests[i][2] * dmax / (20 * distance + 0.00001))  # Many zeros occur due to truncation

            if damage > cnests[i][2]:
                cnests[i][2] = 0
            else:
                cnests[i][2] -= damage
                self.count += damage

        return self.count


# <================================== End of class Bomb ==================================>
# <=======================================================================================>


class Solution:
    """
    Solution consist of a list with 3 bombs
    """

    # bombPos = []

    def __init__(self, x1, y1, x2, y2, x3, y3, cnests):
        self.b1 = Bomb(x1, y1)
        self.b2 = Bomb(x2, y2)
        self.b3 = Bomb(x3, y3)
        self.fitness = self.SolutionFitness(cnests)
        self.probability = 0

    def SolutionFitness(self, cnests):
        """
        :param cnests:
        :return: The total fitness of solution
        """
        return self.b1.fitness(cnests) + self.b2.fitness(cnests) + self.b3.fitness(cnests)


    def calculate_probability_of_solution(self, lenght, position_of_solution):
        """
        Calculates the probability of the soltion based on the Rank Roulete Wheel
        and stores it in a variable (p = (lenght + position_of_solution + 1) / sum_of_solutions)
        input : lenght--> lenght of the list of Bombs
                position_of_solution --> the position i in the list
        Output: Sets the probability of the Solution
        """

        sum_of_solutions = int((lenght*(lenght+1)) / 2)

        self.probability = (lenght - position_of_solution + 1)/ sum_of_solutions



# <================================== End of class Solution ==============================>
# <=======================================================================================>


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

    nests = {}
    count = 0

    with open("nests.txt", "r") as file:
        for line in file:
            reader = line.split()
            count += 1
            nests[count] = [int(reader[0]), int(reader[1]), int(reader[2])]

    return nests


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

def create_random_population(number_of_solutions):
    """
    Creates N random solutions and returns them in a sorted list
    input: N = number_of_solutions
    Output: Bombs = a list of solution
    """
    bombs = []
    #  Populate bombs with random number_of_solutions. Will have 6 float numbers with 3 digit precision
    for i in range(number_of_solutions):
        random_bomb = random.sample(range(100000), 6)
        random_bomb[:] = [x / 1000 for x in random_bomb]
        copy_nests = openFile()  # reading the coordinates of the nests. That should be done once before for loop
        bombs.append(Solution(random_bomb[0], random_bomb[1], random_bomb[2], random_bomb[3], random_bomb[4],
                              random_bomb[5], copy_nests))

    bombs.sort(key=key_fun, reverse=True)
    return bombs


def main():

    number_of_solutions = 6  # Preferable number_of_solutions 500
    Bombs = create_random_population(number_of_solutions) #  Populate Bombs with random solution
    
if __name__ == '__main__':
    main()
