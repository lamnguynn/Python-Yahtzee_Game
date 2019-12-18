'''
Author: Lam Nguyen
Date: 12/15/2019
Contact: lam65nguyen@tamu.edu
Notes: Any questions or confusions please let me know!
'''

from random import randint

players_and_score = {}                                                  #Stores the player's name as a key, and score as a value
player_name = []                                                        #Stores the names of the players

def roll_dice():
    '''
    Purpose: Rolls the dice
    :return: a list containing five randomly generated numbers. List acts like the dice.
    '''
    return [randint(1, 6) for i in range(5)]

def show_instructions():
    '''Instructions for the game. Done in function because it needs to be repeated multiple times'''
    return ["-----Instructions-----",
                     "There are 13 rounds to the game.",
                     "Each player rolls the five dice to determine who goes first (highest total goes first). On your turn you may roll up to three times, and you may pick and choose which dice you wish to reroll after the initial roll.",
                     "You may fill in any single box you wish and use any sequence of dice you wish that are shown on your final roll.",
                     "Once one player has finished their turn by marking something on their score card, the next player begins their turn.",
                     "This continues until all players have filled in all 13 boxes on their score card and a final point tally is taken, with the highest score revealing the winner."]

def show_how_to_score():
    '''Shows how to score in the game'''
    return ["-----How to score-----",
            "This code plays the game Yahtzee!",
            "Aces: Sum of #1 dices",
            "Twos: Sum of #2 dices",
            "Threes: Sum of #3 dices",
            "Fours: Sum of #4 dices",
            "Fives: Sum of #5 dices",
            "Sixes: Sum of #6 dices",
            "If you score over 63 points in these 6 boxes then a bonus of 35 is added",
            "",
            "Three of a kind: 3 dice are the same, sum the dice",
            "Four of a kind: 4 dice are the same, sum the dice",
            "Full House: 3 of 1 and 2 of another, 25",
            "Small straight: 1-2-3-4, 2-3-4-5, 3-4-5-6, 30",
            "Large straight: 1-2-3-4-5, 2-3-4-5-6, 40",
            "Yahtzee: All 5 dice are the same, 50",
            "Chance: Any combo, sum dice"]

#Three of a kind
#Four of a kind
#Since Three of a Kind and Four of a Kind are the same code essentially, there only needs to be passed in the dice list and the type of kind/
def a_kind(dice_roll, num_of_kind):
    '''
    :purpose: finds if the dice roll has a x of a kind (x can be any number)
    :param dice_roll:
    :param num_of_kind:
    :return: a sum of all the rolls if there is a x of a kind (x can be any number).
    :comments: since the for Three of a kind and Four of a kind are similar, it is reasonable to write one function and catch the differences in if statements.
    '''
    occur = 0               # how many times a number occurs
    occur_type = 0          # stores the number that occurs 3 times
    # Loops through the list passed in and checks to see if a number occurs num_of_kind or more times.
    for i in range(len(dice_roll)):
        occur = 0
        for r in range(len(dice_roll)):
            if i != r:                                  #does not do a comparison with itself
                if dice_roll[i] == dice_roll[r]:        #checking to see if two numbers are the same
                    occur += 1
                    occur_type = dice_roll[i]
        if occur == num_of_kind - 1:
            return sum(dice_roll)           #if a number occurs num_of_kind - 1 times, immediately return the value and the sum of the list

#Full House
def full_house(dice_roll):
    '''
    :purpose: Finds if the dice roll has a full house
    :param dice_roll:
    :return: a score if there is a full house
    :comments: uses both three of a kind and two of a kind, and if both are not None, then there is a full house.
    '''
    if a_kind(dice_roll, 2) != None and a_kind(dice_roll, 3) != None:
        return 25
    else:
        return None

def n_straight(dice_roll):
    '''
    :purpose: Finds if the dice roll has either a small or large straight, or none.
    :param dice_roll:
    :return: score depending on what kind of straight is found in the dice roll.
    :comments: Counts the number times there is a sequence. Code works for both large and small straight
       Since the code for Small Straight and Large Straight are similar, it is reasonable to write function and catch the differences in if statements.
    '''
    count = 0
    for i in range(len(dice_roll)-1):
        if dice_roll[i] == dice_roll[i+1]-1:
            count+=1
    if count == 3:      #Small straight
        return 30
    elif count == 4:    #Large straight
        return 40
    else:
        return None

def yahtzee(dice_roll):
    '''
    :purpose: Finds if all five dice are the same.
    :param dice_roll:
    :return: score depending on if-else statement
    '''
    for i in range(len(dice_roll)-1):
        if dice_roll[i] != dice_roll[i+1]:              #Simply checks if the number in the next index is not the same as the number in the current index, there is no yahtzee.
            return None
    return 50

def chance(dice_roll):
    '''
    :purpose: Finds the score for chance
    :param dice_roll:
    :return: the sum of all the dice rolls
    '''
    '''Any combination will yield a chance and the score is the sum of all the dices'''
    return sum(dice_roll)

def upper_section(dice_roll,n):
    '''
    :purpose: Finds the upper section score (Aces, Twos, Threes, Fours, Fives, Sixes)
    :param dice_roll:
    :param n: the value you want to see occur in the dice roll
    :return: score: the length of the list created from finding the value "n" in the dice_roll list
    '''
    val = []
    for i in dice_roll:
        if i == n:              #Finds all the numbers in the roll equal to the 'n' argument
           val.append(i)
    if len(val) == 0:           #If the list is empty (none found), then return None
        return None
    else:
        return sum(val)
    #return sum([(i) for i in dice_roll if i == n])










