import os
import numpy as np
import pandas as pd

path = os.path.dirname(__file__)
pbpname = os.path.join(path,'NBA_Hackathon_-_Play_by_Play.txt')
lineupname = os.path.join(path,'NBA_Hackathon_-_Game_Lineup.txt')

lineups = pd.read_csv(lineupname, sep='\t')
events = pd.read_csv(pbpname, sep='\t')

def startOfPeriod(game,period,master,active):
    """Access the lineup data file to determine the starters for each quarter. Populate the active players list with the starters.
       If any players are not yet in the master list, append them to the master list."""

    pStarters = lineups[(lineups['Game_id'] == game) & (lineups['Period'] == period)]
    condition = True

    for index, row in pStarters.iterrows():
        index = index #the unused variable warning was getting on my nerves, lol
        player = row['Person_id']

        for sublist in master:
            if player == sublist[1]:
                active.append([row['Game_id'],player,row['Team_id'],0])
                condition = False
                break
        
        if condition:
            master.append([row['Game_id'],player,row['Team_id'],0])
            active.append([row['Game_id'],player,row['Team_id'],0])            


def madeBasket(ev,active):
    """At any made basket, add the point value to the scoring team's players' +/- and subtract it from the defending team's players."""

    if ev['Event_Msg_Type'] == 3 & ev['Option1'] == 2:
        return

    points = int(ev['Option1'])
    scoringTeam = ev['Team_id']

    for player in active:
        if(player[2] == scoringTeam):
            player[3] += points
        else:
            player[3] -= points

def freeThrow(events,active,master):
    """Update the +/- of all players on the court when a foul is called. If there is a substitution between free throws, delay the 
       substitution until after all free throws have been shot."""
    
    subs = []
    i = 0

    for i, row in events.iterrows():
        if row['Event_Msg_Type'] == 8:
            subs.append(row)
        if row['Event_Msg_Type'] == 3:
            madeBasket(row,active)
        if (row['Event_Msg_Type'] != 8) & (row['Event_Msg_Type'] != 3):
            break
    
    for sub in subs:
        subIn(sub,active,master)
    
    return i

def subIn(ev,active,master):
    """Remove Player1 from the active players list and replace him with Player2; update Player1's total +/- in the master list."""

    inPlayer = ev['Person2']
    outPlayer = ev['Person1']

    for player in active:
        if player[1] == outPlayer:
            pM = player[3]
            active.remove(player)
    
    for player in master:
        if player[1] == outPlayer:
            player[3] += pM
    
    for player in master:
        if player[1] == inPlayer:
            active.append([ev['Game_id'],inPlayer,ev['Team_id'],0])
            return

    master.append([ev['Game_id'],inPlayer,ev['Team_id'],0])
    active.append([ev['Game_id'],inPlayer,ev['Team_id'],0])

def endOfPeriod(master,active):
    """Clear the active players list and update the master list for all +/- at the end of a quarter."""

    for player in active:
        for mPlayer in master:
            if player[1] == mPlayer[1]:
                mPlayer[3] += player[3]

games = events['Game_id'].unique()
sol = pd.DataFrame(columns=['Game_id','Player_id','Team_id','Player_Plus/Minus'])
solutionRow = 0

for game in games:
    master,active = [],[]

    for x in range(1,5):
        i = 0  
        startOfPeriod(game,x,master,active)
        pEvents = events[(events['Game_id'] == game) & (events['Period'] == x)]
        for index, row in pEvents.iterrows():
            if index < i:
                continue
            if row['Event_Msg_Type'] == 1:
                madeBasket(row,active)
            if row['Event_Msg_Type'] == 3:
                ftEvents = pEvents.loc[index:]
                i = freeThrow(ftEvents,active,master)
            if row['Event_Msg_Type'] == 8:
                subIn(row,active,master)
            if row['Event_Msg_Type'] == 13:
                endOfPeriod(master,active)
                active = []
    for element in master:
        sol.loc[solutionRow] = element
        solutionRow += 1

sol = sol.drop(columns='Team_id')

sol.to_csv('Indiana PaVers.csv',index=False)