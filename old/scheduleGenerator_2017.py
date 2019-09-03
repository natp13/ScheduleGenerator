import random

r = [["natural", "dillon"],
["garber", "johnwayne"],
["franchise", "kormanation"],
["grony", "kumarius"],
["marta", "hanks"],
["rdirk", "mdirk"]]

divisions = [['natural', 'kumarius', 'mdirk'],
['garber', 'dillon', 'grony'],
['rdirk', 'kormanation', 'marta'],
['franchise', 'hanks', 'johnwayne']]

weeks = 13
schedule = [r]

allGames = []
allTeams = []
opponentsMap = {}
awayGames = {}

def printSchedule():
    for iWeek in range(0,len(schedule)):
        print(iWeek+1, ":")
        for matchup in schedule[iWeek]:
            divisionMatchup = False
            for division in divisions:
                if (matchup[0] in division) and (matchup[1] in division):
                    divisionMatchup = True
                    break
                    
            if divisionMatchup:
                print("\t", matchup[0], "@", matchup[1], "**")
            else:
                print("\t", matchup[0], "@", matchup[1])
        print("")

def scheduleGame(iWeek, game):
    # opponentsMap[game[0]].append(game[1])
    # opponentsMap[game[1]].append(game[0])  
    
    if (awayGames[game[0]] > 6):
        game.reverse()
    
    schedule[iWeek].append(game)
    if (len(schedule[iWeek]) > 6):
        print("too many games for week", iWeek)
        raise Exception
        
    awayGames[game[0]] = awayGames[game[0]] + 1

def isTeamInGame(team, game):
    return (team == game[0]) or (team == game[1])

def areGamesEqual(game1, game2):
    # return ((game1[0] == game2[0]) or (game1[0] == game2[1])) and ((game1[1] == game2[0]) or (game1[1] == game2[1]))
    return (isTeamInGame(game1[0], game2) and isTeamInGame(game1[1], game2))
    
def isGameValidForWeek(iWeek, game):
    # the game is valid for that week if we don't find either of the teams from that game in any other
    # scheduled game that week
    for scheduledGame in schedule[iWeek]:
        if isTeamInGame(game[0], scheduledGame) or isTeamInGame(game[1], scheduledGame):
            return False
    
    #and if the same matchup exists in the previous or next week it's not valid either
    if (iWeek > 0):
        for scheduledGame in schedule[iWeek - 1]:
            if (areGamesEqual(scheduledGame, game)):
                return False
    
    if (iWeek < (weeks - 1)):
        for scheduledGame in schedule[iWeek + 1]:
            if (areGamesEqual(scheduledGame, game)):
                return False
    
    return True
    
def populateAllTeams():
    global allTeams
    
    allTeams = []
    for iMatchup in range(0,len(r)):
        allTeams.append(r[iMatchup][0])
        allTeams.append(r[iMatchup][1])
        
    for team in allTeams:
        opponentsMap[team] = []
        
def initializeSchedule():
    global schedule
    global awayGames
    schedule = []
    for iWeek in range(0, weeks):
        schedule.append([])
    
    awayGames = {}
    for team in allTeams:
        awayGames[team] = 0

def generateSchedule():
    global allGames
    global allTeams
    global schedule
    
    initializeSchedule()
    schedule.append(r)
    populateAllTeams()
        
    print(allTeams)
    
    tryAgain = True
    while (tryAgain):
        allGames = []
        initializeSchedule()
        schedule.append(r)
        for team in allTeams:
            opponentsMap[team] = []
    
        # generate games for everyone playing everyone once and schedule those
        for iTeam in range(0, len(allTeams)):
            for jTeam in range(iTeam + 1, len(allTeams)):
                if (iTeam == jTeam):
                    raise Exception
                    
                allGames.append([allTeams[iTeam], allTeams[jTeam]])
        random.shuffle(allGames)

        # remove the games we already scheduled for week 1
        for gameScheduled in schedule[0]:
            iGame = 0
            while (iGame < len(allGames)):
                # if not (areGamesEqual(gameScheduled, game)):
                if areGamesEqual(gameScheduled, allGames[iGame]):
                    allGames.pop(iGame)
                else:
                    iGame = iGame + 1
                
        iWeek = 1 # we can skip week 1 because we already filled it out - but we don't have to
        while (iWeek < weeks):
            iGame = 0
            while iGame < len(allGames):
                if (isGameValidForWeek(iWeek, allGames[iGame])):
                    # add this game to the schedule
                    scheduleGame(iWeek, allGames[iGame])
                    allGames.pop(iGame)
                    
                    if (len(schedule[iWeek]) == 6):
                        break                
                else:
                    #only increment if we didn't remove this game
                    iGame = iGame + 1

            iWeek = iWeek + 1
            
        if (len(allGames) == 0):
            tryAgain = False
            
    # printSchedule()

    # now we have all of the everyone plays everyone else games done
    # generate games for everyone playing everyone once
    allGames = []
    for iTeam in range(0, len(allTeams)):
        for jTeam in range(iTeam + 1, len(allTeams)):
            if (iTeam == jTeam):
                raise Exception
                
            allGames.append(random.shuffle([allTeams[iTeam], allTeams[jTeam]]))
    random.shuffle(allGames)
    
    iWeek = 0
    while (iWeek < weeks):
        while (len(schedule[iWeek]) < 6):
            foundGame = False
            for iGame in range(0, len(allGames)):
                #find a game that we can schedule for this week
                if (isGameValidForWeek(iWeek, allGames[iGame])):
                    # print iWeek, allGames[iGame]
                    scheduleGame(iWeek, allGames[iGame])
                    allGames.pop(iGame);
                    foundGame = True
                    break # out of for loop
            
            if (not foundGame):
                print("somehow we couldn't schedule a game")
                print(schedule[iWeek])
                print(allGames)
                raise Exception
            
        iWeek = iWeek + 1

def removeScheduledGamesFromGameList(games):
    for week in schedule:
        for scheduledGame in week:
            iGame = 0
            while (iGame < len(games)):
                if areGamesEqual(games[iGame], scheduledGame):
                    games.pop(iGame)
                else:
                    iGame = iGame + 1
        
def scheduleGamesFromList(games):
    gamesToSchedule = [g for g in games]
    removeScheduledGamesFromGameList(gamesToSchedule)
    
    scheduleOrder = [3,4,5,10,11,12,0,1,2,6,7,8,9]
    iWeek = 0
    while (iWeek < weeks):
        while (len(schedule[scheduleOrder[iWeek]]) < 6):
            foundGame = False
            for iGame in range(0, len(gamesToSchedule)):
                #find a game that we can schedule for this week
                if (isGameValidForWeek(scheduleOrder[iWeek], gamesToSchedule[iGame])):
                    # print iWeek, gamesToSchedule[iGame]
                    scheduleGame(scheduleOrder[iWeek], gamesToSchedule[iGame])
                    gamesToSchedule.pop(iGame);
                    foundGame = True
                    break # out of for loop
            
            if (not foundGame):
                # print "somehow we couldn't schedule a game"
                # print schedule[iWeek]
                # print gamesToSchedule
                # raise Exception
                # printSchedule()
                
                return False
            
        iWeek = iWeek + 1
    return True
    
def getHomeTeam(game):
    return game[0]

def scheduleDivisionOnlyGames():
    initializeSchedule()
    
    for division in divisions:
        randomOrderDivision = [r for r in division]
        random.shuffle(randomOrderDivision)

        thisGames = []
        
        thisGames.append([randomOrderDivision[0], randomOrderDivision[1]])
        thisGames.append([randomOrderDivision[1], randomOrderDivision[2]])
        thisGames.append([randomOrderDivision[2], randomOrderDivision[0]])
        
        random.shuffle(randomOrderDivision)
        
        thisGames.append([randomOrderDivision[0], randomOrderDivision[1]])
        thisGames.append([randomOrderDivision[1], randomOrderDivision[2]])
        thisGames.append([randomOrderDivision[2], randomOrderDivision[0]])
        
        for i in [0,1,2]:
            for j in [3,4,5]:
                if areGamesEqual(thisGames[i], thisGames[j]):
                    if getHomeTeam(thisGames[i]) == getHomeTeam(thisGames[j]):
                        thisGames[j].reverse()
        
        
        scheduleGame(3, thisGames[0])
        scheduleGame(4, thisGames[1])
        scheduleGame(5, thisGames[2])
        scheduleGame(10, thisGames[3])
        scheduleGame(11, thisGames[4])
        scheduleGame(12, thisGames[5])

        
def scheduleRivalryWeekGames():
    for i in range(len(r)):
        random.shuffle(r[i])
        scheduleGame(0, r[i])
            
def removeScheduledGamesFromGameList(games):
    for week in schedule:
        for scheduledGame in week:
            iGame = 0
            while (iGame < len(games)):
                if areGamesEqual(games[iGame], scheduledGame):
                    games.pop(iGame)
                else:
                    iGame = iGame + 1
    
def printGamesToSchedule(games):
    for game in games:
        print(game)
        
def generateScheduleForDivisions():
    global allTeams
    global schedule
    
    initializeSchedule()
    populateAllTeams()
    
    gamesToSchedule = []
    
    #populate games to schedule with playing each person in division twice and everyone else once
    for i in range(0, len(allTeams)):
        for j in range (i+1, len(allTeams)):
            newGame = [allTeams[i], allTeams[j]]
            random.shuffle(newGame)
            gamesToSchedule.append(newGame)
            
            # now see if these two teams are in the same division
            for division in divisions:
                if (allTeams[i] in division) and (allTeams[j] in division):
                    gamesToSchedule.append([allTeams[i], allTeams[j]])
    # printGamesToSchedule(gamesToSchedule)
    random.shuffle(gamesToSchedule)
    
    # schedule the division games and the non-division rivalry games
    scheduleDivisionOnlyGames()
    scheduleRivalryWeekGames()
    
    tries = 0
    while (not scheduleGamesFromList(gamesToSchedule)):
        random.shuffle(gamesToSchedule)
        
        # we're trying again, so schedule the division games and the non-division rivalry games
        scheduleDivisionOnlyGames()
        scheduleRivalryWeekGames()
        tries = tries + 1
    print("tries:", tries)
    
def validateSchedule():
    teamSchedule = {}
    teamawayGames = {}
    for team in allTeams:
        teamSchedule[team] = []
        teamawayGames[team] = 0
            
    # Now validate all schedules:
    for iWeek in range(0,len(schedule)):
        for matchup in schedule[iWeek]:
            teamSchedule[matchup[0]].append(matchup[1])
            teamSchedule[matchup[1]].append(matchup[0])
            teamawayGames[matchup[0]] = teamawayGames[matchup[0]] + 1
            if (matchup[0] == matchup[1]):
                print("playing yourself")
                raise Exception
    
    for team in teamSchedule:
        numUniqueTeams = len(set(teamSchedule[team]))
        print(team, ": ", numUniqueTeams, " - ", "away:", teamawayGames[team], "-", teamSchedule[team])
        
        if numUniqueTeams != 11:
            print("someone not playing everyone")
            raise Exception
        
        for opponent in teamSchedule[team]:
            if teamSchedule[team].count(opponent) > 2:
                print("someone playing someone more than twice")
                raise Exception
           
        for iOpponent in range(1,len(teamSchedule[team])):
            if teamSchedule[team][iOpponent-1] == teamSchedule[team][iOpponent]:
                print("back to back weeks against opponent")
                raise Exception
    
if __name__ == "__main__":
    # generateSchedule()
    generateScheduleForDivisions()
    
    printSchedule()
    
    validateSchedule()