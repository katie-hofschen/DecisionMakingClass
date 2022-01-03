#!/usr/bin/env python3

import readcsv
import sys
import pandas as pd
import numpy as np


def stats_team(argv):
    rcsv = readcsv.ReadCSV(argv[0])
    stats = rcsv.goals_statistics(argv[1], verbose=True)
    meaning = rcsv.goals_statistics_meaning()

    for i in range(0, len(stats)):
        print(meaning[i], '\t', stats[i])

def goalStatsDf(csv):
    #using this function to bring all of the statistics into a dataframe for easier use and visualisation
    rcsv = readcsv.ReadCSV(csv)
    entire_df = pd.read_csv(csv)
    all_teams = np.sort(entire_df.AwayTeam.unique())
    team_stats = []

    for team in all_teams:
        team_stats.append((team,) + rcsv.goals_statistics(team))
    goalstat_df = pd.DataFrame(team_stats, columns = ["team", "scoredGoals", "concededGoals", "numMatches", "scoredHome", "concededHome", "numMatchesHome", "scoredAway", "concededAway", "numMatchesAway"])
    return goalstat_df

def poissonProb(avgNumEvents, observedEvents):
    numerator = np.math.pow(avgNumEvents,observedEvents) * np.math.pow(np.math.e, (-avgNumEvents))
    denominator = np.math.factorial(observedEvents)
    probObserved = numerator / denominator
    return probObserved

############ 1st part of exercise writing described methods

def exact_score_odds(argv):
    #csv_file, homeTeam, awayTeam, goalsHome, goalsAway
    # exact_score_odds(csv_file, team1,team2, gh, ga) -> returns the predicted exact score goalsHome-goalsAway in the match team1 against team2
    summary_df = goalStatsDf(argv[0])
    avgT1 = np.around(summary_df.loc[summary_df["team"] == argv[1], "scoredGoals"].values[0] / summary_df.loc[summary_df["team"] == argv[1], "numMatches"].values[0], 3)
    avgT2 = np.around(summary_df.loc[summary_df["team"] == argv[2], "scoredGoals"].values[0] / summary_df.loc[summary_df["team"] == argv[2], "numMatches"].values[0], 3)
    odds = 1 / (poissonProb(avgT1, int(argv[3])) * poissonProb(avgT2, int(argv[4])))
    return odds

def oddsMatrix(argv):
    # pred_1X2(csv_file, team1, team2) -> returns the tuple (odds that team1 wins, odds of draw, odds of team2 wins)
    # after analysing the sports df you can see that 7 goals was the max but it is so unlikely/close to 0% that it causes division errors
    oddsMatrix = np.zeros((6,6))
    for h in range(0,6):
        for a in range(0,6):
            oddsMatrix[h,a] = np.around(exact_score_odds(argv),3)
    return oddsMatrix

def pred_1X2(argv):
    matrix = 100/oddsMatrix(argv)
    oddsDraw = np.around(np.diagonal(matrix).sum(),2)
    oddsLoss = np.around(np.triu(matrix, k=1).sum(),2)
    oddsWin = np.around(np.tril(matrix, k=-1).sum(),2)
    return ((100/oddsWin),(100/oddsDraw),(100/oddsLoss))

########### Own solution

def all_matchesStats(csv_file):
    # this function returns avg of goals scored/conceded overall at home and also the same averages for away
    summary_df = goalStatsDf(csv_file)
    totalscoredHomeAvg = summary_df["scoredHome"].sum() / summary_df["numMatchesHome"].sum()
    totalconcededHomeAvg = summary_df["concededHome"].sum() / summary_df["numMatchesHome"].sum()
    totalscoredAwayAvg = summary_df["scoredAway"].sum() / summary_df["numMatchesAway"].sum()
    totalconcededAwayAvg = summary_df["concededAway"].sum() / summary_df["numMatchesAway"].sum()
    # if correct totalscoredHomeAvg should be the same as totalconcededAway
    return (totalscoredHomeAvg, totalconcededHomeAvg, totalscoredAwayAvg, totalconcededAwayAvg)

def exact_score_odds_alt(csv_file, homeTeam, awayTeam, homeGoals, awayGoals):
    summary_df = goalStatsDf(csv_file)
    totalAverages = all_matchesStats(csv_file)

    # calculating the Attack strength and defensive strengths in comparison to the overall averages
    avgHomeScore = np.around(summary_df.loc[summary_df["team"] == homeTeam, "scoredHome"].values[0] / summary_df.loc[summary_df["team"] == homeTeam, "numMatchesHome"].values[0], 3)
    homeAttackAvg = avgHomeScore / totalAverages[0]
    avgHomeConcede = np.around(summary_df.loc[summary_df["team"] == homeTeam, "concededHome"].values[0] / summary_df.loc[summary_df["team"] == homeTeam, "numMatchesHome"].values[0], 3)
    homeDefenseAvg = avgHomeConcede / totalAverages[1]
    avgAwayScore = np.around(summary_df.loc[summary_df["team"] == awayTeam, "scoredAway"].values[0] / summary_df.loc[summary_df["team"] == awayTeam, "numMatchesAway"].values[0], 3)
    awayAttackAvg = avgAwayScore / totalAverages[2]
    avgAwayConcede = np.around(summary_df.loc[summary_df["team"] == awayTeam, "concededAway"].values[0] / summary_df.loc[summary_df["team"] == awayTeam, "numMatchesAway"].values[0], 3)
    awayDefenseAvg = avgAwayConcede / totalAverages[3]
    lambdaHome = homeAttackAvg * awayDefenseAvg * totalAverages[0]
    lambdaAway = homeDefenseAvg * awayAttackAvg * totalAverages[1]
    #to verify what average for home goals vs away goals are
    #print(lambdaHome, lambdaAway)
    oddsOutcome = 1 / (np.around(poissonProb(lambdaHome, homeGoals),4) * np.around(poissonProb(lambdaAway, awayGoals),4))
    return np.around(oddsOutcome,3)

def oddsMatrixAlt(csv, homeTeam, awayTeam):
    # pred_1X2(csv_file, team1, team2) -> returns the tuple (odds that team1 wins, odds of draw, odds of team2 wins)
    # after analysing the sports df you can see that 7 goals was the max but it is so unlikely/close to 0% that it causes division errors
    oddsMatrix = np.zeros((6,6))
    for h in range(0,6):
        for a in range(0,6):
            oddsMatrix[h,a] = np.around(exact_score_odds_alt(csv, homeTeam, awayTeam, h, a),3)
    return oddsMatrix

def pred_1X2_alt(csv,homeTeam, awayTeam):
    matrix = 100/oddsMatrixAlt(csv,homeTeam, awayTeam)
    oddsDraw = 100/np.around(np.diagonal(matrix).sum(),2)
    oddsLoss = 100/np.around(np.triu(matrix, k=1).sum(),2)
    oddsWin = 100/np.around(np.tril(matrix, k=-1).sum(),2)
    return (oddsWin,oddsDraw,oddsLoss)

if __name__ == "__main__":
    '''Run with <csv_file> <team name>
    E.g., I1.csv Bologna'''
    #stats_team(sys.argv[1:])
    print("Odds of exact goals: ",exact_score_odds(sys.argv[1:]))
    print("Odds of win, draw, loss: ", pred_1X2(sys.argv[1:]))
    # Do something to exploit the raw stats, for instance to determine
    # the odds (1, X, 2) of Bologna - Napoli.
    # '''Run with <csv_file> <team home name> <team away name>
    # E.g., I1.csv Bologna Napoli'''
    # pred_1X2(sys.argv[1:])


