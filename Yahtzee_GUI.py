import tkinter as tk
import Yahtzee_Background_Code as yah

'''
Author: Lam Nguyen
Date: 12/15/2019
Contact: lam65nguyen@tamu.edu
Notes: Any questions or confusions please let me know! 

Key concepts: Working to make a game from tkinter and handle all the pieces put together into one system; essentially practicing systems development.

Additional Features to be added: Open up a new GUI to reroll individual die. Currently rerolls the entire set of die

Known Bugs: The printing of the section score is buggy; could be fixed by just clearing the widgets existing there first and then placing new one. 
'''

gui = tk.Tk()
gui.title("Yahtzee Game")

num_player_entry = tk.Entry(gui)        #Entry to type in number of players. Have it exist for now and place it later.
player_name_entry = []                  #Stores entries to type in the player name. Have it exist for now and place it later.
pick_entry = tk.Entry(gui)              #Entry to type in option. Have it exist for now, and then place it later
score_options = {}                      #Stores the possible scoring options for a player
num_reroll = 0                          #Stores the number of rerolls. Created to make sure a player can reroll only twice.
num_roll = 0                            #Stores the number of rolls. Created to make sure a player can roll only once.
num_clicks = 0                          #Stores the number of clicks to submit number of players
winner = ''                             #Stores the winner of the game
highest_score = 0                       #Stores the highest score
total_num_player = 0                    #Total number of players
rounds = 0                              #The current round
player = 1                              #The current player

def roll_the_dice():
    '''The purpose of this function is to print out onto the GUI a roll. Used with the function "reroll" and "roll"'''
    roll = yah.roll_dice()          #Calls the roll dice function of Yahtzee_Background_Code.py and sets the variable equal to a list of numbers.
    c = 2                           #Column to place on grid
    tk.Label(gui, text = "Roll:").grid(row = 0,column = 2)
    tk.Label(gui,text = "     ").grid(row = 0, column =1)
    for i in range(len(roll)):      #Prints out the numbers rolled as labels
        tk.Label(gui, text = str(roll[i])).grid(row =1, column = c)
        c+=1
    options(roll)                   #Calls the option function to display the possible scoring options

def options(roll):
    '''The purpose of this function is to print out the possible scoring option for the player'''
    global score_options
    score_options = {'Ones': yah.upper_section(roll, 1),        #Stores the possible scoring option as a dictionary with the scoring type as the key and the score as the value.
                   'Twos': yah.upper_section(roll, 2),
                   'Threes': yah.upper_section(roll, 3),
                   'Fours': yah.upper_section(roll, 4),
                   'Fives': yah.upper_section(roll, 5),
                   'Sixes': yah.upper_section(roll, 6),
                   'Three of a kind': yah.a_kind(roll, 3),
                   'Four of a kind': yah.a_kind(roll, 4),
                   'Full House': yah.full_house(roll),
                   'Small straight': yah.n_straight(roll),
                   'Large straight': yah.n_straight(roll),
                   'Chance': yah.chance(roll),
                   'Yahtzee': yah.yahtzee(roll)}

    tk.Label(gui, text = "     ").grid(row = 0, column = 7)
    tk.Label(gui, text = "Possible scoring options").grid(row = 0, column =8)

    r = 0
    for key, value in score_options.items():
        tk.Label(gui, text = "                                 ").grid(row = r, column = 9) #Cover up the previous text
        tk.Label(gui, text = key+": "+str(value)).grid(row= r,column = 9)                   #Add a label on top
        r+=1

    pick_option()

def roll():
    '''The purpose of this function is display a dice roll'''
    global num_roll
    if num_roll > 0:            #If the num of rolls is greater than zero, then do nothing.
        return
    else:                       #Else, roll the dice
        roll_the_dice()
        num_roll+=1

def reroll():
    '''The purpose of this function is to display a new dice roll
    Extra Feature that could be implemented: Reroll individual die'''
    global num_reroll
    if num_reroll > 1:         #If the num of rerolls is greater than one, then do nothing.
        return
    else:                      #Else, reroll the entire dice
        roll_the_dice()
        num_reroll+=1

def pick_option():
    '''The purpose of this function is prompt the user to either reroll the dice or choose a section to score'''
    pick_label = tk.Label(gui, text="Pick a section").grid(row = 13, column = 8)            #Label to display to pick an option
    submit_button = tk.Button(gui, text = "Submit  ",width = 15, command = score)           #Button to submit the score
    reroll_button = tk.Button(gui, text = "Reroll  ", width = 15, command = reroll)         #Button to reroll the dice

    #Placing the widgets
    submit_button.grid(row = 14, column = 9)
    pick_entry.grid(row = 13, column = 9)
    reroll_button.grid(row = 15, column = 9)

def score():
    '''The purpose of this function is to score the player's section choice'''
    choice = pick_entry.get()                           #Get the user inputted score option

    '''Explanation: Run a try and except infinite times to get the user to input the right score option.'''
    if choice == "":                                                            #If there is nothing put in, just do nothing
        return
    elif score_options[choice] == None:                                         #If there is nothing to score in the inputted score option, then it is a throwaway: set the score option equal to zero
        yah.players_and_score[yah.player_name[player- 1]][choice] = 0
    elif yah.players_and_score[yah.player_name[player-1]][choice] != None:      #If there exist a score already, then do nothing
        return
    else:                                                                       #Else, then just add the score to the score option.
        yah.players_and_score[yah.player_name[player - 1]][choice] = score_options[choice]
    keep_track_of_progress()
    menu()

def keep_track_of_progress():
    '''The purpose of this function is to add keep track of the amount of rounds and what player's turn it is.'''
    global player
    global rounds
    global num_reroll
    global num_roll

    player+=1                               #Switch players turn to the next
    rounds+=1                               #Add one more to rounds done
    num_roll = 0                            #Resets the number of rolls
    num_reroll = 0                          #Resets the number of rerolls
    if player == total_num_player+1:        #If the last player has gone, switch back to the first player
        player=1
    if rounds == total_num_player*2:       #If the number of rounds done is equal to the total number of players times 13, then display the winner and all cores on a new GUI, and destroy all widgets
        clear_all_widgets()                 #Delete all existing widgets to signify the end of the game
        score = find_total_scores()         #Stores a list of all the total scores
        find_winner(score)                  #Finds the winner and highest score from the list of scores
        winner_gui = tk.Tk()                #Create a new frame
        winner_gui.title("Scores")          #Adding a title to the frame

        c = 0
        tk.Label(winner_gui, text = "The winner is " + winner + "!").grid(row = 0)        #Display the winner
        tk.Label(winner_gui, text = "Highest score: " + str(highest_score)).grid(row = 1) #Display the highest score
        tk.Label(winner_gui, text = 25*"-").grid(row = 2)                                 #Display 25 dashes for aesthetic purposes
        '''Explanation: The dictionary holding the player and their scores has the name as a key, and a dictionary as a value.
           First, display the name, which is just the key
           Second, travserse the dictionary, which is the value, and display it on the GUI
           Scores of each player is placed on each column.'''
        for k, v in yah.players_and_score.items():
            r = 3                           #Reset the row to display to 3
            tk.Label(winner_gui, text = 'Player: ' + k).grid(row = r, column = c)         #Display the players name on the GUI                                                                    #Row to place the widgets
            for score_type, score in v.items():
                tk.Label(winner_gui, text = score_type + ": " + str(score)).grid(row = r+1, column = c)
                r+=1
            c+=4                            #Print the next player's set of scores in the next column
        start_over_button = tk.Button(winner_gui, text = "Start Over", width = 15,command = get_num_player).grid(row = 0, column = 4)      #Button to start over the game
        exit_game_button = tk.Button(winner_gui, text = "Exit", width = 15,command = winner_gui.withdraw).grid(row = 1, column = 4)        #Button to exit the game
        winner_gui.mainloop()

def find_total_scores():
    '''The purpose of this function is add up all the scores.'''
    all_scores = []                         # Stores the values of the total score of all the players
    for v1 in yah.players_and_score.values():
        sum = 0
        for v2 in v1.values():
            if v2 != None:
                sum += v2
        all_scores.append(sum)

    return all_scores

def find_winner(scores):
    '''The purpose of this function is to find the winner from the list of scores given by argument.'''
    global highest_score
    global winner

    for i in range(len(scores)):            #Traversing the scores list.
        if scores[i] > highest_score:       #Finding max value by checking for values bigger than the current highest score
            highest_score = scores[i]
            winner = yah.player_name[i]

def view_score():
    '''The purpose of this function is to display the score of the player'''
    player_to_view_score = yah.player_name[player-1]
    tk.Label(gui, text = "Score").grid(row = 0, column = 10)
    r = 0
    for key, value in yah.players_and_score.items():
        if key == player_to_view_score:
            for k, v in yah.players_and_score[key].items():
                tk.Label(gui, text = "                                      ").grid(row=r, column=11)
                tk.Label(gui, text=k + ": " + str(v)).grid(row=r, column=11)
                r+=1

def show_instruct():
    '''The purpose of this function is to create a new GUI to show the instructions of the game'''
    a = tk.Tk()                                                                             #Create a new GUI to view
    instructions = yah.show_instructions()                                                  #Pull the list containing the instructions from Yahtzee_Background_Code.py
    for i in range(len(instructions)):                                                      #Traverse the list to print out the instructions via label
        tk.Label(a, text = instructions[i]).grid(row = i, column = 0)

    tk.Button(a, text = "Return", command = a.withdraw).grid(row = len(instructions)+1)     #Add a button to get rid of the GUI
    a.mainloop()


def clear_all_widgets():
    '''The purpose of this function is to clear out any widgets on the GUI'''
    for widget in gui.winfo_children():                 #Traverse through all the widgets
        widget.destroy()                                #Destroy them

def menu():
    '''The purpose of this function is to display the menu on the GUI'''
    clear_all_widgets()                                 #Clear all the widgets
    global pick_entry                                   #Bring back the deleted pick_entry widget

    pick_entry = tk.Entry(gui)                                                                                              #Create another entry since the last one was deleted.
    player_label = tk.Label(gui, text = "Player "+str(player)+" turn").grid(row = 0)                                        #Label for whose turn it is
    Roll_dice_button = tk.Button(gui, text = "Roll dice",width = 15,command = roll).grid(row = 1)                           #Button to press to roll the dice
    view_score_button = tk.Button(gui, text = 'View Score', width = 15, command = view_score).grid(row = 2)                 #Button to view scores
    show_instruction_button = tk.Button(gui, text = 'Show Instruction', width = 15, command = show_instruct).grid(row =3)   #Button to view how to play
    how_to_score_button = tk.Button(gui, text='How to score', width=15, command  = show_how_score).grid(row=4)              #Button to view how to score
    quit_button = tk.Button(gui, text = 'Quit', width = 15, command = quit).grid(row = 5)                                   #Button to quit the game

def show_how_score():
    '''The purpose of this function is to create a new GUI to show how to score'''
    a = tk.Tk()                                                                             #Create a new GUI to view
    how_score = yah.show_how_to_score()                                                     #Pull the list containing the scoring from Yahtzee_Background_Code.py
    for i in range(len(how_score)):                                                         #Traverse the list to print out the scoring via label
        tk.Label(a, text = how_score[i]).grid(row = i, column = 0)

    tk.Button(a, text = "Return", command = a.withdraw).grid(row = len(how_score)+1)        #Add a button to get rid of the GUI
    a.mainloop()

def add_player_name():
    '''The purpose of this function is to take the names from the list of names, and add it to the data structures in the Yahtzee_Background_Code.py files'''
    for i in range(len(player_name_entry)):
        yah.player_name.append(player_name_entry[i].get())                                                                  #Add names to the player_name list of Yahtzee_Background_Code.py
        yah.players_and_score[yah.player_name[i]] = {'Ones': None, 'Twos': None, 'Threes': None, 'Fours': None,             #Create a new key and value entry in the dictionary of Yahtzee_Background_Code.py
                                                    'Fives': None,
                                                     'Sixes': None, 'Three of a kind': None, 'Four of a kind': None,
                                                     'Full House': None, 'Small straight': None,
                                                     'Large straight': None,
                                                     'Chance': None, 'Yahtzee': None}

    menu()
    gui.mainloop()

def get_player_name():
    '''The purpose of this function is to get the users to input their names'''
    global total_num_player
    global player_name_entry
    global num_clicks
    player_name_entry = []                          #Resets the player_name_entry if players want to play again.

    total_num_player = int(num_player_entry.get())  #Stores the number of players

    if total_num_player == 1:                       #If the number of players is one, then display an error message.
        tk.Label(gui, text = "Two plus players only").grid(row = 2, column = 0)
    elif total_num_player > 1 and num_clicks <1:    #Else, create new labels, entries, and a button to get the players to input their names
        r = 4
        num_clicks+=1
        for i in range(total_num_player):
            player_name_entry.append(tk.Entry(gui))
            tk.Label(gui, text='Enter player name:').grid(row=r)
            player_name_entry[i].grid(row = r, column = 1)
            r += 1
        tk.Button(gui, text = "Submit", width = 15, command = add_player_name).grid(row = r, column = 1)


    gui.mainloop()

def get_num_player():
    '''The purpose of this function is to ask the user to enter the amount of players there are'''
    global num_player_entry
    global num_clicks
    yah.player_name = []                            #Clears all data in the player_name list of the Yahtzee_Background_Code.py file so the game can function properly when starting over
    yah.players_and_score = {}                      #Clears all data in the player_and_score list of the Yahtzee_Background_Code.py file so the game can function properly when starting over

    num_player_entry = tk.Entry(gui)
    num_clicks = 0                                  #Resets the number of clicks to submit the number of players

    tk.Label(gui, text = "Enter the number of players: ").grid(row = 0)
    num_player_entry.grid(row = 0, column = 1)
    tk.Button(gui, text = "Submit", width = 15, command = get_player_name).grid(row =1, column = 1)
    tk.Button(gui, text = "Exit", width = 15,command = quit).grid(row = 2, column = 1)
    tk.Label(gui, text = 25*'-').grid(row = 3)
    gui.mainloop()


#####################
'''Main Code Below'''
#####################

'''Comments: There is no need for any loop since the functions above are coded to be in a loop'''
get_num_player()








