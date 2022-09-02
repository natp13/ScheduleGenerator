import random

divisions = [['natural', 'hanks', 'tyler', 'marta'],
['kumar', 'kormanation', 'franchise', 'garber'],
['rdirk', 'eckmanity', 'dillon', 'grony']]

weeks = 14
schedule = []

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

    for division in divisions:
        for team in division:
            allTeams.append(team)

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

    scheduleOrder = [2,3,4,11,12,13,0,1,5,6,7,8,9,10]
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

        # week 3
        thisGames.append(random.sample([randomOrderDivision[0], randomOrderDivision[1]], 2))
        thisGames.append(random.sample([randomOrderDivision[2], randomOrderDivision[3]], 2))
        # week 4
        thisGames.append(random.sample([randomOrderDivision[0], randomOrderDivision[2]], 2))
        thisGames.append(random.sample([randomOrderDivision[1], randomOrderDivision[3]], 2))
        # week 5
        thisGames.append(random.sample([randomOrderDivision[0], randomOrderDivision[3]], 2))
        thisGames.append(random.sample([randomOrderDivision[1], randomOrderDivision[2]], 2))

        random.shuffle(randomOrderDivision)

        # week 12
        thisGames.append([randomOrderDivision[0], randomOrderDivision[1]])
        thisGames.append([randomOrderDivision[2], randomOrderDivision[3]])
        # week 13
        thisGames.append([randomOrderDivision[0], randomOrderDivision[2]])
        thisGames.append([randomOrderDivision[1], randomOrderDivision[3]])
        # week 14
        thisGames.append([randomOrderDivision[0], randomOrderDivision[3]])
        thisGames.append([randomOrderDivision[1], randomOrderDivision[2]])

        for i in range(0, 6):
            for j in range(6, 12):
                if areGamesEqual(thisGames[i], thisGames[j]):
                    if getHomeTeam(thisGames[i]) == getHomeTeam(thisGames[j]):
                        thisGames[j].reverse()

        scheduleGame(2, thisGames[0])
        scheduleGame(2, thisGames[1])
        scheduleGame(3, thisGames[2])
        scheduleGame(3, thisGames[3])
        scheduleGame(4, thisGames[4])
        scheduleGame(4, thisGames[5])
        scheduleGame(11, thisGames[6])
        scheduleGame(11, thisGames[7])
        scheduleGame(12, thisGames[8])
        scheduleGame(12, thisGames[9])
        scheduleGame(13, thisGames[10])
        scheduleGame(13, thisGames[11])

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

    random.shuffle(gamesToSchedule)

    # schedule the division games and the non-division rivalry games
    scheduleDivisionOnlyGames()
    #scheduleRivalryWeekGames()

    tries = 0
    while (not scheduleGamesFromList(gamesToSchedule)):
        random.shuffle(gamesToSchedule)

        # we're trying again, so schedule the division games and the non-division rivalry games
        scheduleDivisionOnlyGames()
        # scheduleRivalryWeekGames()
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
    generateScheduleForDivisions()
    printSchedule()
    validateSchedule()