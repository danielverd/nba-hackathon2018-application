# nba-hackathon2018-application

The code in this repository is a full solution to the application question for the 2018 NBA Hackathon. I learned about the event about 3 days before the application deadline, so the code was never submitted. However, I recently came back and debugged the script so that it creates an output with reasonable data values.

The question asked to parse play by play data for 50 NBA games and calculate the Plus-Minus for every player that played in the game. Additional data files included the starting lineups for each team and a key for event codes (1 = Made Basket, 4 = Rebound, etc.). The full prompt is in the included PDF file.

Interestingly enough, there is a quirk in the data that is never mentioned in the prompt. For free throws (Event Code = 3), the Option1 data field signals whether the shot was made or missed. In the prompt, Option1 is specified to be "the point value of any attempted shot". This completely ignores its utility in judging free throw accuracy. This conclusion was made by observing that all free throws with an Option1 value of 2 were followed by a rebound. This is only possible on misses.

The final script is stored in plus_minus.py and the iPython notebook includes my scratch notes, a few tests, and a bunch of print statements I used for debugging (some errors in this notebook were never fixed). The final result is stored in Indiana PaVers.csv.

#EDIT 7/23/19 : Two significant bugs have been noticed and fixed. The first was the range of the Period for loop. By looping through quarters 1 through 4, the program was unable to catch any stats from overtime games. Additionally, though it does not seem to negatively affect how this program runs, the for loop now sorts data values by the recommended fields in the prompt rather than just by the indices.
