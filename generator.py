#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Jure Forstneric
#jforst at google's email service
#2018-03-10

#This is a D&D 5e random combat encounter generator.

import csv
import random
import argparse

#list copied from DMG pg 82 for xp thresholds by char level

thresholds = [
	[25, 50, 75, 100],
	[50, 100, 150, 200],
	[75, 150, 225, 400],
	[125, 250, 375, 500],
	[250, 500, 750, 1100],
	[300, 600, 900, 1400],
	[350, 750, 1100, 1700],
	[450, 900, 1400, 2100],
	[550, 1100, 1600, 2400],
	[600, 1200, 1900, 2800],
	[800, 1600, 2400, 3600],
	[1000, 2000, 3000, 4500],
	[1100, 2200, 3400, 5100],
	[1250, 2500, 3800, 5700],
	[1400, 2800, 4300, 6400],
	[1600, 3200, 4800, 7200],
	[2000, 3900, 5900, 8800],
	[2100, 4200, 6300, 9500],
	[2400, 4900, 7300, 10900],
	[2800, 5700, 8500, 12700]
]

#this function is new for 2.0, it allows us to parse arguments

def argument_parse():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--partySize", help="The number of PCs in our party.", type=int)
	parser.add_argument("-l", "--level", help="The average level of the PCs.", type=int)
	parser.add_argument("-d", "--difficulty", help="Difficulty (1 - Easy, 2 - Medium, 3 - Difficult, 4 - Deadly)", type=int, choices=[1, 2, 3, 4])
	parser.add_argument("-e", "--environment", help="Environment (0 - City, 1 - Dungeon, 2 - Forest, 3 - Nature, 4 - Other plane, 5 - Underground, 6 - Water)", type=int, choices=[0, 1, 2, 3, 4, 5, 6])
	parser.add_argument("-i", "--interactive", help="Run the program in interactive mode to setup the encounter (implied if arguments are missing).", action="store_true")
	args = parser.parse_args()
	#if any of our arguments besides environment are missing, default to interactive mode by returning None:
	if (not args.partySize) or (not args.level) or (not args.difficulty):
		print("Running in interactive mode!")
		return([None, None, None, None])
	if args.interactive:
		print("Running in interactive mode!")
		return([None, None, None, None])
	print("Party size: " + str(args.partySize))
	print("Party level: " + str(args.level))
	print("Encounter difficulty: " + str(args.difficulty))
	returnedArguments = [args.partySize, args.level, args.difficulty, args.environment]
	return(returnedArguments)

#our function with three inputs - number of PCs, their average level, and difficulty

def party_threshold(numPcs, avgLev, difficulty):
	if difficulty is None:
		print('What is the difficulty of the encounter?')
		print('1 - Easy, 2 - Medium, 3 - Difficult, 4 - Deadly')
		encDiff = int(input())
	else:
		encDiff = difficulty
	xp = thresholds[(avgLev - 1)][(encDiff - 1)]
	xp = (xp * numPcs)
	print()
	print('Our combined party XP threshold is: ' + str(xp))
	return xp

#this is a function to get our adventuring party, save it in a CSV file to use as the default for next time

def party():
	partyFile = open('party.csv', 'r', newline='')		# opens the file party.csv in read-only mode
	partyReader = csv.reader(partyFile)
	partyData = list(partyReader)		# saves data from CSV to list
	print('Our previous party had ' + str(partyData[0][0]) + ' level ' + str(partyData[0][1]) + ' characters.')
	print('Press enter to continue with previous party, \'n\' to make new party, or \'q\' to quit.')
	answer = str(input())
	if answer == 'q' or answer == 'Q':
		raise SystemExit
	if answer == 'n' or answer == 'N':
		print('How many PCs do we have?')
		numPcs = int(input())
		print('What is their average level?')
		avgLev = int(input())
		newParty = {1: [numPcs, avgLev]}		# data to write in the format {line_number:data_to_write}
		with open('party.csv', 'w', newline='') as newParty:		# write data to csv file and replace the lines in newParty
			partyWriter = csv.writer(newParty)
			partyWriter.writerow([numPcs, avgLev])
		return([numPcs, avgLev])
	else:
		print('Our party stays with ' + str(partyData[0][0]) + ' level ' + str(partyData[0][1]) + ' characters.')
		return([int(partyData[0][0]), int(partyData[0][1])])

#function to load monsters from csv file and return them as a list

def load_monsters():
	monsterFile = open('monsters.csv', 'r', newline='')		# opens the file monsters.csv in read-only mode
	monsterReader = csv.reader(monsterFile)
	monsterData = list(monsterReader)		# saves data from CSV to list
	return(monsterData)


# specify the encounter (in 2.0 we only chose among locations)

def specify_encounter(monsterData, encounterChoice, specifiedLocation):
	specificType = []
	for i in monsterData:
		if i[encounterChoice] not in str(specificType):
			specificType.append(i[encounterChoice])
	specificType.sort()
	print()
	# if we didn't get a location argument, we select it interactively
	if specifiedLocation is None:
		print('Press the corresponding number to select encounter type:')
		for i in range(len(specificType)):
			print(str(i) + ' ' + str(specificType[i]))
		encounterType = int(input())
	else:
		encounterType = specifiedLocation
	print()
	print('Your choice is ' + str(specificType[encounterType]) + ' encounter.')
	print()
	return specificType[encounterType]

# create a new list of monsters defined by the type of encounter

def create_monster_list(monsterData, encounterType, encounterChoice):
	possibleMonsters = []
	for m in monsterData:
		if encounterType in m[encounterChoice]:
			possibleMonsters.append(m)
	return possibleMonsters

# generate our combat encounter

def encounter_gen(monsterList, xpThreshold):
	encounteredMonsters = []		# list for the encountered monsters
	monsterCounter = 0
	xpMonsters = 0
	xpLowerLimit = int(xpThreshold / 25)
	while xpMonsters < (xpThreshold - (3 * xpLowerLimit)):		# keep adding monsters until we get close enought to xpThreshold
		possibleMonsters = []
		for m in monsterList:		# remove monsters with too high or too low xp values
			if xpLowerLimit < int(m[4]) < (xpThreshold - xpMonsters):
				possibleMonsters.append(m)
		if not possibleMonsters:
			print('Ran out of suitable monsters :-(')		# this is just a warning that there might have been xp left over
			return encounteredMonsters
		r = random.randint(0, (len(possibleMonsters) - 1))
		encounteredMonsters.append(possibleMonsters[r])
		monsterCounter = len(encounteredMonsters)
		xpMonsters = 0
		for xp in encounteredMonsters:
			xpMonsters += int(xp[4])
		if monsterCounter == 2:			# these if statements take into account difficulty scaling with # of monsters
			xpMonsters = int(xpMonsters * 1.5)
		if 3 <= monsterCounter <= 6:
			xpMonsters = xpMonsters * 2
		if 7 <= monsterCounter <= 10:
			xpMonsters = int(xpMonsters * 2.5)
	return encounteredMonsters

#print out the monsters in a nicely formated way

def print_encounter(encounteredMonsters, encounterType):
	print('Our encounter consists of:')
	for m in encounteredMonsters:
		print(str(m[0].capitalize()) + ', type ' + str(m[2]) + ', XP value of ' + str(m[4]) + ' (MM pg. ' + m[3] + ')')
	print()
	print('Press enter to repeat or \'q\' to quit.')
	answer = str(input())
	if answer == 'q' or answer == 'Q':
		raise SystemExit
	else:
		return()


def main():
	returnedArguments = argument_parse()
	# if argumentParse returns None (when we are missing any of the party arguments), run the party and difficulty setup:
	if (returnedArguments[0] is None):
		ourParty = party()
		xp = party_threshold(ourParty[0], ourParty[1], None)
	# if we do have the party arguments, we use them to generate our XP threshold
	else:
		ourParty = returnedArguments
		xp = party_threshold(ourParty[0], ourParty[1], ourParty[2])
	monster_data = load_monsters()
	encounterChoice = 1   # this option is static in 2.0, previously, this was encounterChoice=chooseEncounterType()
	encounterType = specify_encounter(monster_data, encounterChoice, returnedArguments[3])
	monsterList = create_monster_list(monster_data, encounterType, encounterChoice)
	encounteredMonsters = encounter_gen(monsterList, xp)
	print_encounter(encounteredMonsters, encounterChoice)


while True:
	main()
