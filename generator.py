#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#Jure Forstneric
#jforst at google's email service
#2018-03-10

#This is a D&D 5e random combat encounter generator.

import pprint
import csv
import random

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

#our function with two inputs - the number of PCs and their average level  

def partyThreshold(numPcs, avgLev):
	print('What is the difficulty of the encounter?')
	print('1 - Easy, 2 - Medium, 3 - Difficult, 4 - Deadly')
	encDiff = int(input())
	xp = thresholds[(avgLev - 1)][(encDiff - 1)]
	xp = (xp * numPcs)
	print()
	print('Our combined party XP threshold is: ' + str(xp))
	print()
	return xp
	
#this is a function to get our adventuring party, save it in a CSV file to use as the default for next time

def party():
	partyFile = open('party.csv', 'r', newline='')	#opens the file party.csv in read-only mode
	partyReader = csv.reader(partyFile)
	partyData = list(partyReader)		#saves data from CSV to list
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
		newParty = {1:[numPcs, avgLev]}		#data to write in the format {line_number:data_to_write}
		with open('party.csv', 'w', newline='') as newParty:	#write data to csv file and replace the lines in newParty
			partyWriter = csv.writer(newParty)
			partyWriter.writerow([numPcs, avgLev])
		return([numPcs,avgLev])
	else:
		print('Our party stays with ' + str(partyData[0][0]) + ' level ' + str(partyData[0][1]) + ' characters.')
		return([int(partyData[0][0]), int(partyData[0][1])])
		
#function to load monsters from csv file and return them as a list

def loadMonsters():
	monsterFile = open('monsters.csv', 'r', newline='')	#opens the file monsters.csv in read-only mode
	monsterReader = csv.reader(monsterFile)
	monsterData = list(monsterReader)		#saves data from CSV to list
	return(monsterData)
	
#function to choose if want to select monsters by location or type
	
def chooseEncounterType():
	while True:
		print('Press L for encounter by location (city, forest, underground... ) or T for type (undead, monstrosity, humanoid... ):')
		answer = str(input())
		if answer == 'l' or answer == 'L':
			return 1
		if answer == 't' or answer == 'T':
			return 2

#specify the encounter (once we've defined if we're choosing among locations or types)

def specifyEncounter(monsterData,encounterChoice):
	specificType = []
	for i in range(len(monsterData)):
		if monsterData[i][encounterChoice] not in str(specificType):
			specificType.append(monsterData[i][encounterChoice])
	specificType.sort()
	print()
	print('Press the corresponding number to select encounter type:')
	for i in range(len(specificType)):
		print(str(i) + ' ' + str(specificType[i]))
	encounterType = int(input())
	print()
	print('Your choice is ' + str(specificType[encounterType]) + ' encounter.')
	print()
	return specificType[encounterType]	#returns the specific type of encounter

#create a new list of monsters defined by the type of encounter

def createMonsterList(monsterData,encounterType,encounterChoice):
	possibleMonsters = []
	for i in range(len(monsterData)):
		if encounterType in monsterData[i][encounterChoice]:
			possibleMonsters.append(monsterData[i])
	return possibleMonsters

#generate our combat encounter

def encounterGen(monsterList,xpThreshold):
	encounteredMonsters = []		#list for the encountered monsters
	monsterCounter = 0
	xpMonsters = 0
	xpLowerLimit = int(xpThreshold / 25)
	while xpMonsters <(xpThreshold - (3 * xpLowerLimit)):		#keep adding monsters until we get close enought to xpThreshold
		possibleMonsters = []
		for i in range(len(monsterList)):		#remove monsters with too high or too low xp values
			if xpLowerLimit < int(monsterList[i][4]) < (xpThreshold - xpMonsters):
				possibleMonsters.append(monsterList[i])		
		if not possibleMonsters:
			print('Ran out of suitable monsters :-(')		#this is just a warning that there might have been xp left over
			return encounteredMonsters 				
		r = random.randint(0, (len(possibleMonsters) - 1))
		encounteredMonsters.append(possibleMonsters[r])
		monsterCounter = len(encounteredMonsters)
		xpMonsters = 0
		for xp in range(len(encounteredMonsters)):
			xpMonsters += int(encounteredMonsters[xp][4])
		if monsterCounter == 2:			#these if statements take into account difficulty scaling with # of monsters
			xpMonsters = int(xpMonsters * 1.5)
		if 3 <= monsterCounter <= 6:
			xpMonsters = xpMonsters * 2
		if 7 <= monsterCounter <= 10:
			xpMonsters = int(xpMonsters * 2.5)
	return encounteredMonsters
	
#print out the monsters in a nicely formated way

def printEncounter(encounteredMonsters,encounterType):
	print('Our encounter consists of:')
	if encounterType == 1:
		for m in range(len(encounteredMonsters)):
			print(str(encounteredMonsters[m][0].capitalize()) + ', type ' + str(encounteredMonsters[m][2]) + ', XP value of ' + str(encounteredMonsters[m][4]) + ' (DMG pg. ' + encounteredMonsters[m][3] + ')')
	else:
		for m in range(len(encounteredMonsters) - 1):
			print(str(encounteredMonsters[m][0].capitalize()) + ', found in ' + str(encounteredMonsters[m][1]) + ', XP value of ' + str(encounteredMonsters[m][4]) + ' (DMG pg. ' + encounteredMonsters[m][3] + ')')			
	print()
	


def main():
	ourParty = party()
	xp = partyThreshold(ourParty[0], ourParty[1])
	monsterData = loadMonsters()
	encounterChoice = chooseEncounterType()
	encounterType = specifyEncounter(monsterData,encounterChoice)
	monsterList = createMonsterList(monsterData,encounterType,encounterChoice)
	encounteredMonsters = encounterGen(monsterList,xp)
	printEncounter(encounteredMonsters,encounterChoice)


while True:
	main()
	
