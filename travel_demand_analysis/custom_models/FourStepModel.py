import pandas as pd
from random import randint
import random
from math import exp

class TripGeneration:
    def __init__(self, pathToData, dependent_col_name):
        self.pathToData = pathToData
        self.dependent_col_name = dependent_col_name
        self.production_col_names = []
        self.production_constant = 0
        self.production_intercepts = []
        self.attraction_col_names = []
        self.attraction_constant = 0
        self.attraction_intercepts = []
        self.production_score = 0
        self.attraction_score = 0
        self.balancing_factor = 0

    def printAttributes(self):
        print("Attributes")
        print(self.production_col_names)
        print(self.production_constant)
        print(self.production_intercepts)
        print(self.attraction_col_names)
        print(self.attraction_constant)
        print(self.attraction_intercepts)

    def setProductionParameters(self, production_col_names, production_constant, production_intercepts):
        self.production_col_names = production_col_names
        self.production_constant = production_constant
        self.production_intercepts = production_intercepts

    def setAttractionParameters(self, attraction_col_names, attraction_constant, attraction_intercepts):
        self.attraction_col_names = attraction_col_names
        self.attraction_constant = attraction_constant
        self.attraction_intercepts = attraction_intercepts

    # get trip production score for 'zone'
    def getWholeTripProductionScore(self):
        data = pd.read_csv(self.pathToData, encoding="utf-8",index_col=0)
        # implement specific way to get sub-table(data) just for specific 'zone' i.e: all rows related to zone1
        sub_table = data.loc[:, self.production_col_names]
        length_rows = sub_table.shape[0]
        for x in range(0, length_rows):
            row_values = sub_table.iloc[x, :].values
            self.production_score += self.production_constant
            print(str(row_values))
            for j in range(0, len(row_values)):
                print(str(self.production_col_names[j])+" ROW_VALUES: "+str(row_values[j]))
                self.production_score += int(row_values[j] * self.production_intercepts[j])
                # print("SELFPROD CURR: "+str(self.production_score))
        return int(self.production_score)

    # get trip attraction score for 'zone'
    def getWholeTripAttractionScore(self):
        data = pd.read_csv(self.pathToData, index_col=0)
        # implement specific way to get sub-table(data) just for specific 'zone' i.e: all rows related to zone1
        sub_table = data.loc[:, self.attraction_col_names]
        length_rows = sub_table.shape[0]
        for x in range(0, length_rows):
            row_values = sub_table.iloc[x, :].values
            self.attraction_score += self.attraction_constant
            for j in range(0, len(row_values)):
                self.attraction_score += int(row_values[j] * self.attraction_intercepts[j])
                # print("SELFATTR CURR: "+str(self.attraction_score))
        return int(self.attraction_score)

    def getZoneTripProductionScore(self, zone_number):
        self.production_score = 0
        data = pd.read_csv(self.pathToData, index_col=0)
        # implement specific way to get sub-table(data) just for specific 'zone' i.e: all rows related to zone1
        row_values = data.loc[zone_number, self.production_col_names].values

        self.production_score += self.production_constant
        for j in range(0, len(row_values)):
            self.production_score += row_values[j] * self.production_intercepts[j]

        return self.production_score

    def getZoneTripAttractionScore(self, zone_number):
        self.attraction_score = 0
        data = pd.read_csv(self.pathToData, index_col=0)
        # implement specific way to get sub-table(data) just for specific 'zone' i.e: all rows related to zone1
        row_values = data.loc[zone_number, self.production_col_names].values

        self.attraction_score += self.attraction_constant
        for j in range(0, len(row_values)):
            self.attraction_score += row_values[j] * self.attraction_intercepts[j]

        return self.attraction_score

    def doTripBalancing(self):
        self.balancing_factor = self.production_score / self.attraction_score
        self.attraction_score = self.balancing_factor * self.attraction_score
        self.production_score = self.balancing_factor * self.production_score
        # Implement trip balancing here VOID

    def getBalancingFactor(self):
        return self.balancing_factor

    def printAllZonalTripsProductionAttraction(self):
        productionScores = []
        attractionScores = []
        df = pd.DataFrame(columns=('Trip Production', 'Trip Atraction'))
        total_production = 0
        total_attraction = 0
        data = pd.read_csv(self.pathToData, index_col=0)
        length_rows = data.shape[0]
        for x in range(0, length_rows):
            attr_score = 0
            prod_score = 0
            #print("data_cols: "+str(data.columns.values))
            #print("attr_cols: "+str(self.attraction_col_names))
            attr_row_values = data.loc[x, self.attraction_col_names].values
            prod_row_values = data.loc[x, self.production_col_names].values
            attr_score += self.attraction_constant
            prod_score += self.production_constant
            for j in range(0, len(attr_row_values)):
                attr_score += attr_row_values[j] * self.attraction_intercepts[j]
            total_attraction += attr_score
            for j in range(0, len(prod_row_values)):
                prod_score += prod_row_values[j] * self.production_intercepts[j]
            total_production += prod_score
            df.loc[x] = [int(prod_score), int(attr_score)]
            productionScores.append(int(prod_score))
            attractionScores.append(int(attr_score))
            print("Zone "+str(x)+": Production="+str(prod_score)+" , Attraction="+str(attr_score))

        print("prodscores: " + str(productionScores))
        print("attrscores: " + str(attractionScores))
        balancing_factor = sum(productionScores)/sum(attractionScores)
        balanced_attractionScores = [i * balancing_factor for i in attractionScores]

        print("balanced attr scores: " + str(balanced_attractionScores))
        return df, productionScores, balanced_attractionScores;
        # print("Total Production="+str(total_production)+" , Total Attraction="+str(total_attraction))

    def getTripProductionScores(self):
        productionScores = []
        total_production = 0
        total_attraction = 0
        data = pd.read_csv(self.pathToData, index_col=0)
        length_rows = data.shape[0]
        for x in range(1, length_rows + 1):
            prod_score = 0
            prod_row_values = data.loc[x, self.production_col_names].values
            prod_score += self.production_constant
            for j in range(0, len(prod_row_values)):
                prod_score += prod_row_values[j] * self.production_intercepts[j]
            total_production += prod_score
            productionScores.append(prod_score)
        return productionScores

    def getProductionSubTable(self):
        data = pd.read_csv(self.pathToData, index_col=0)
        return data.loc[:, self.production_col_names]


import math as math
import matplotlib.pyplot as plt


class TripDistribution:
    def __init__(self, productions, attractions, travelTime, fare, income):
        self.productions = productions
        self.attractions = attractions
        self.travelTime = travelTime
        self.fare = fare
        self.income = income
        self.row = len(productions)
        self.col = len(attractions)
        self.possibleError = sum(productions) * 0.2
        self.error = 0
        self.cost = 0

    def getGeneralizedCost(self, cost):
        return 1.0 / (cost * cost)

    def getCost(self):
        return self.cost

    def computeCost(self, travelTime, fare, income):
        costMatrix = [[1 for x in range(self.row)] for y in range(self.col)]
        for x in range(self.row):
            for y in range(self.col):
                costMatrix[x][y] = (travelTime[x][y]) * income[x] + fare[x][y]
        return costMatrix

    def getTripDistribution(self):
        distributions = [[self.attractions[y] for x in range(self.row)] for y in range(self.col)]
        finalDistributions = [[self.attractions[y] for x in range(self.row)] for y in range(self.col)]
        # costMatrix = [[1 for x in range(self.row)] for y in range(self.col)]
        costMatrix = self.computeCost(self.travelTime, self.fare, self.income)
        self.cost = costMatrix
        A = [1 for x in range(self.row)]
        B = [1 for x in range(self.col)]
        A = self.computeA(B, costMatrix)
        B = self.computeB(A, costMatrix)

        currentBalancingFactor = 0  # 0 for A, 1 for B
        isConvergent = False
        shit = 0
        smallestError = 1000000000

        #         while isConvergent == False:
        for x in range(100):
            if currentBalancingFactor == 0:
                tempA = self.computeA(B, costMatrix)
                A = tempA
                currentBalancingFactor = 1
            elif currentBalancingFactor == 1:
                tempB = self.computeB(A, costMatrix)
                B = tempB
                currentBalancingFactor = 0
            distributions = self.computeDistributions(A, B, costMatrix)
            error = self.getError(distributions)
            if (smallestError > error and error != 0):
                smallestError = error
                finalDistributions = distributions
                self.error = error
                #                 shit = x
        return finalDistributions

    def computeDistributions(self, A, B, costMatrix):
        distributions = [[self.attractions[y] for x in range(self.row)] for y in range(self.col)]
        for x in range(self.row):
            for y in range(self.col):
                distributions[x][y] = round(
                    A[x] * self.productions[x] * B[y] * self.attractions[y] * self.getGeneralizedCost(costMatrix[x][y]),
                    1)
        return distributions

    def checkIfConvergent(self, distributions):
        error = self.getError(distributions)
        if error <= self.possibleError:
            self.error = error
            return True
        return False

    def getError(self, distributions):
        error = 0
        derivedProductions = [0 for x in range(self.row)]
        derivedAttractions = [0 for x in range(self.col)]

        for x in range(self.row):
            for y in range(self.col):
                derivedProductions[x] += distributions[x][y]
                derivedAttractions[y] += distributions[x][y]

        for x in range(self.row):
            error += abs(derivedProductions[x] - self.productions[x])
            error += abs(derivedAttractions[x] - self.attractions[x])

        return error

    def getErrorPercentage(self):
        return self.error / sum(self.productions)

    def computeA(self, B, costMatrix):
        A = [1 for x in range(self.row)]
        for x in range(0, self.row):
            sum = 0.0
            for y in range(0, self.col):
                sum += B[y] * self.attractions[y] * self.getGeneralizedCost(costMatrix[x][y])
            A[x] = 1.0 / sum
        return A

    def computeB(self, A, costMatrix):
        B = [1 for x in range(self.col)]
        for x in range(0, self.row):
            sum = 0.0
            for y in range(0, self.col):
                sum += A[y] * self.productions[y] * self.getGeneralizedCost(costMatrix[x][y])
            B[x] = 1.0 / sum
        return B


import random


class ModalSplit:
    def __init__(self, od_matrix, pathToData, income, fares, travelTimes):
        self.od_matrix = od_matrix
        self.pathToData = pathToData
        self.travel_costs = []
        self.travel_probabilities = []
        self.modes = ['jeep', 'bus']
        self.income = income
        self.fares = fares
        self.travelTimes = travelTimes
        self.travel_costs = [0] * len(self.modes)

    def computeGeneralizedCosts(self, mode_number):
        costMatrix = [[1 for x in range(len(self.od_matrix))] for y in range(len(self.od_matrix))]
        for x in range(len(self.od_matrix)):
            for y in range(len(self.od_matrix)):
                if (self.fares[mode_number][x][y] == 0):
                    costMatrix[x][y] = 0
                else:
                    costMatrix[x][y] = self.travelTimes[mode_number][x][y] * self.income[x] + \
                                       self.fares[mode_number][x][y]

        return costMatrix

    #         #data = pd.read_csv(self.pathToData, index_col=0)

    #         self.travel_costs = [None] * len(self.modes)
    #         for x in range(0, len(self.modes)):
    #             self.travel_costs[x] = random.randrange(1,4)
    #         #Compute for generalized cost for each mode for this specific zone
    #         # populate self.travel_costs with the travel costs
    #         self.computeModalProbabilities()

    def computeModalProbabilities(self, mode_number, beta):
        travel_probabilities = [[1 for x in range(len(self.od_matrix))] for y in range(len(self.od_matrix))]
        sum = 0
        # print(len(self.travel_costs))
        for x in range(len(self.od_matrix)):
            for y in range(len(self.od_matrix)):
                sum = 0
                for k in range(len(self.modes)):
                    if (self.travel_costs[k][x][y] != 0):
                        sum += math.e ** ((-beta) * self.travel_costs[k][x][y])

                if (self.travel_costs[mode_number][x][y] != 0):
                    travel_probabilities[x][y] = math.e ** ((-beta) * self.travel_costs[mode_number][x][y]) / sum
                else:
                    travel_probabilities[x][y] = 0
        return travel_probabilities
        # print(self.travel_costs)
        # print(self.travel_probabilities)

    def getBeta(self, mode_number):
        sum = 0
        for x in range(len(self.od_matrix)):
            for y in range(len(self.od_matrix)):
                if (self.travel_costs[mode_number][x][y] != 0):
                    sum += self.travel_costs[mode_number][x][y]
        return 1 / (sum / (len(self.od_matrix) * len(self.od_matrix)))

    def getSplittedTrips(self, mode_number):
        splittedTrips = [[0 for x in range(len(self.od_matrix))] for y in range(len(self.od_matrix))]
        for x in range(len(self.od_matrix)):
            for y in range(len(self.od_matrix)):
                if (self.travel_probabilities[mode_number][x][y] != 0):
                    splittedTrips[x][y] = round(self.od_matrix[x][y] * self.travel_probabilities[mode_number][x][y], 2)

        return splittedTrips

    def process_od_matrix(self):
        # print("size:"+str(len(self.od_matrix))+","+str(len(self.od_matrix[0])))
        # df = DataFrame(columns=('lib', 'qty1', 'qty2'))
        # for i in range(5):
        # df.loc[i] = [randint(-1,1) for n in range(3)]
        for x in range(len(self.modes)):
            self.travel_costs[x] = self.computeGeneralizedCosts(x)

        beta = [0] * len(self.modes)
        for x in range(len(self.modes)):
            beta[x] = self.getBeta(x)

        self.travel_probabilities = [0] * len(self.modes)
        for x in range(len(self.modes)):
            self.travel_probabilities[x] = self.computeModalProbabilities(x, beta[x]);

        final_matrices = [0] * len(self.modes)
        for x in range(len(self.modes)):
            final_matrices[x] = self.getSplittedTrips(x)

        return final_matrices