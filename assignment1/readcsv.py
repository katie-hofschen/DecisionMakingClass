#!/usr/bin/env python3

'''Exploiting data from http://www.football-data.co.uk/data.php'''

import datetime
import csv
import pandas as pd
import numpy as np

EARLIEST_DATE="01/01/00"

def today_str():
    return datetime.date.today().strftime("%d/%m/%y")

def strptime_specific(str):
    try:
        return datetime.datetime.strptime(str, '%d/%m/%y')
    except ValueError:
        return datetime.datetime.strptime(str, '%d/%m/%Y')


class ReadCSV:
    
    def __init__(self, csv_file_name):
        self.csv_file = csv_file_name
        self.KEY_HTEAM = 'HomeTeam'  # home team name
        self.KEY_ATEAM = 'AwayTeam'  # away team name
        self.KEY_DATE = 'Date'       # match date
        self.KEY_RES_HDA = 'FTR'     # match result (Home H, Draw D, Away A)
        self.KEY_FT_HG = 'FTHG'      # final time number goals home team
        self.KEY_FT_AG = 'FTAG'      # final time number goals away team

    def matches_all_gen(self):
        with open(self.csv_file, 'r', encoding="utf-8", errors='replace') as csvfile:
            try:
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    yield row
            except UnicodeDecodeError:
                raise RuntimeError('Bad encoding. Problem while reading',
                                   self.csv_file)

    def matches_gen(self, team, reader):
        for row in reader:
            if row[self.KEY_HTEAM] == team or row[self.KEY_ATEAM] == team:
                yield row

    # before date (excluded)
    def matches_before_gen(self, date, reader):
        dateobj = strptime_specific(date)
        for row in reader:
            dateobjrow = strptime_specific(row[self.KEY_DATE])
            if dateobjrow < dateobj:
                yield row

    # after date (included)
    def matches_after_gen(self, date, reader):
        dateobj = strptime_specific(date)
        for row in reader:
            dateobjrow = strptime_specific(row[self.KEY_DATE])
            if dateobjrow >= dateobj:
                yield row

    def goals_statistics_meaning(self):
        '''A human readable explanation of the tuple of numbers returned by the function goals_statistics.

        (sum_for, sum_against, num_matches, sum_for_h, sum_against_h, num_matches_h, sum_for_a, sum_against_a, num_matches_a)
        '''
        return ("number goals scored", "number goals conceded", "number of matches played",
                "number goals scored at home", "number goals conceded at home", "number of matches played at home",
                "number goals scored away", "number goals conceded away", "number of matches played away")
 
 
    def goals_statistics(self, team, start_date=EARLIEST_DATE,
                         end_date=today_str(), verbose=False):
        sum_for=0  
        sum_against=0
        num_matches=0
        sum_for_h=0  
        sum_against_h=0
        num_matches_h=0
        sum_for_a=0  
        sum_against_a=0
        num_matches_a=0        
        for row in self.matches_gen(team, self.matches_before_gen(end_date, self.matches_after_gen(start_date, self.matches_all_gen()))):
            isHome = row[self.KEY_HTEAM] == team
            if isHome:
                opp_team = row[self.KEY_ATEAM]
                team_ft_goals = row[self.KEY_FT_HG]
                opp_team_ft_goals = row[self.KEY_FT_AG]
            else:
                opp_team = row[self.KEY_HTEAM]
                team_ft_goals = row[self.KEY_FT_AG]
                opp_team_ft_goals = row[self.KEY_FT_HG]
            if verbose:
                print('{homeoraway} against {:<30} {}-{} {} {}'
                      .format(opp_team,
                              team_ft_goals,
                              opp_team_ft_goals,
                              "\t", row[self.KEY_DATE],
                              homeoraway="H" if isHome else "A"))
            num_matches = num_matches + 1
            try:
                sum_for = sum_for + int(team_ft_goals)
                sum_against = sum_against + int(opp_team_ft_goals)
                if isHome:
                    num_matches_h += 1
                    sum_for_h += int(team_ft_goals)
                    sum_against_h += int(opp_team_ft_goals)
                else:
                    num_matches_a += 1
                    sum_for_a += int(team_ft_goals)
                    sum_against_a += int(opp_team_ft_goals)
            except ValueError:
                # because sometimes, the match did not happen yet
                continue
        return (sum_for, sum_against, num_matches, sum_for_h, sum_against_h, num_matches_h, sum_for_a, sum_against_a, num_matches_a)
        
def main():
    pass
    
if __name__ == "__main__":
    main()
