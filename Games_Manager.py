from New_Game import New_Game 
import datetime


class Player:
    def __init__(self, name, age, group=None):
        self.name = name
        self.age = age
        self.group = group # Group object or None
        self.score = 0
        
        print(f"\nPlayer {self.name} created successfully.\n")

    def current_score(self):
        return self.score
    
    def update_score(self, points):
        new_score = self.score + points

        if new_score >= 0:
            self.score = new_score

        else:
            self.score = 0

    def print_player_score(self):
        print(f"\nPlayer: {self.name}, Score: {self.score}")

    def __str__(self):
        return f"\nPlayer(Name: {self.name}, Age: {self.age}, Group: {self.group}, score: {self.score}\n"


class Group:
    def __init__(self, group_name, mother_group=None):
        self.group_name = group_name
        self.mother_group = mother_group  # Group object or None
        self.sub_groups = []  # List of sub-groups (group objects)
        self.players = []   # List of Player objects

        print(f"\nGroup {self.group_name} created successfully.\n")

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_total_score(self):
            # get the score of players in the current group
            current_total = sum(player.score for player in self.players)
            
            # get the total score of sub-groups recursively
            for sub_group in self.sub_groups:
                current_total += sub_group.get_total_score() 
                
            return current_total

    def __str__(self):
        return f"\nGroup(Name: {self.group_name}, Players: {[str(player) for player in self.players]})\n"


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.date = datetime.datetime.now()
        self.formatted_date = self.date.strftime("%d/%m/%Y %H:%M")

        self.duration = 0
        self.rounds_played = 0
        self.players = [player1, player2]  # List of Player objects
        self.draw = False

        self.winner:Player = None
        self.loser:Player = None

    
    def start_game(self):        

        new_game_instance =  New_Game(self.players[0].name, self.players[1].name)
        game_result, self.rounds_played, self.duration = new_game_instance.play() # 

        if game_result != 0: # if not a draw
            self.winner = self.players[game_result - 1]
            self.loser = self.players[1 - (game_result - 1)]

            self.winner.update_score(3)  # Winner gets 3 points
            self.loser.update_score(-1)    # Loser lose 1 points

        else: # draw
            self.draw = True
            for player in self.players:
                player.update_score(1)  # Both players get 1 points for a draw

        self._game_summary()
    
    def _game_summary(self):
        print("\n===============Game Summary===============\n")

        print(f"Date: {self.formatted_date}")

        if self.draw:
            print(f"Game ended in a draw, Rounds Played: {self.rounds_played}, Duration: {self.duration} sec")
            
        else:
            print(f"Winner: {self.winner.name}, Loser: {self.loser.name}, Rounds Played: {self.rounds_played}, Duration: {self.duration} sec")
        
        for player in self.players:
            player.print_player_score()

        print("\n=================================\n")

    def game_info(self, index):

        print(f"{index}. Date: {self.formatted_date}\n"
                    f"Duration: {self.duration} sec\n"
                    f"Rounds: {self.rounds_played}\n")
        if self.draw:
            print(f"Draw ({self.players[0].name} VS {self.players[1].name})")              
            
        else:
            print(f"Winner: {self.winner.name} , Loser: {self.loser.name}")


class Game_Manager:

    def __init__(self):
            self.players_dict: dict[str, Player] = {} # key: player_name, value: Player object
            self.groups_dict: dict[str, Group] = {} # key: group_name, value: Group object
            self.games_history_list: list[Game] = [] # list of Game objects

            print("\n================================= Welcome to the Board Game! =================================\n")


    def launch_game(self):
        self._main_menu()


# main menu 
    def _main_menu(self):

        while True:
            print("\n=========================Main Menu=========================\n")
            print("1. New Game")
            print("2. Players Manager")
            print("3. View Glory Hall")
            print("4. View Games History")
            print("5. Exit")
            
            choice = input("\nPlease select an option:\n")
            
            if choice == '1':
                self.create_new_game()   
                 
            elif choice == '2':
                self._player_manager_menu()

            elif choice == '3':
                self.glory_hall()

            elif choice == '4':
                self.games_history()

            elif choice == '5':
                print("\n=================================Exiting the Game. Goodbye!=================================\n")
                break        

            else:
                print("\nInvalid choice. Please try again.\n")

    def create_new_game(self):
        print("\n===============Starting a new game===============\n")

        while True:

            if len(self.players_dict) < 2:
                print("Not enough players to start a new game. Please add more players.\n")
                break

            print("\nChoose player1 for the new game\n")
            self._print_players()

            player1_number = input("Enter the player number for player1: ")
            player2_number = input("Enter the player number for player2: ")

            if player1_number == '0' or player2_number == '0':
                print("\nNew game cancelled.\n")
                break

            elif player1_number == player2_number:
                print("\nPlayer1 and Player2 cannot be the same. Please try again.\n")

            elif not player1_number.isdigit() or int(player1_number) < 1 or int(player1_number) > len(self.players_dict):
                print("\nInvalid player1 number. Please try again.\n")
            
            elif not player2_number.isdigit() or int(player2_number) < 1 or int(player2_number) > len(self.players_dict):
                print("\nInvalid player2 number. Please try again.\n")

            else:
                player1 = list(self.players_dict.values())[int(player1_number) - 1]
                player2 = list(self.players_dict.values())[int(player2_number) - 1]
                
                if max(player1.age, player2.age) - min(player1.age, player2.age) > 10:
                    print("\nThe age difference between players cannot exceed 10 years. New game cancelled.\n")
                    break

                else:
                    new_game_obj = Game(player1, player2)
                    new_game_obj.start_game()
                    self.games_history_list.append(new_game_obj)   
                    break          

    def glory_hall(self):
        print("\n===============Hall of fame===============\n")

        print("\n=====Top 5 Players=====")
        if not self.players_dict:
            print("No players yet.\n")
        else:
            index = 1
            for player in self._sort_players_by_score():
                indent = ('-')*(20-len(player.name))
                print(f"{index}. {player.name} {indent} {player.score} pts")
                index += 1
            
        print("\n=====Top 5 Groups=====")
        if not self.groups_dict:
            print("No groups yet.\n")
        else:
            index = 1
            for group in self._sort_groups_by_score():
                indent = ('-')*(20-len(group.group_name))
                print(f"{index}. {group.group_name} {indent} {group.get_total_score()} pts")
                index += 1
        
        print("\n=================================\n")

    def games_history(self):
        print("\n===============Game history===============\n")

        if not self.games_history_list:
            print("No games played yet.\n")
        else:
            index = 1
            for game in self.games_history_list:
                game.game_info(index)
                index += 1
        
        print("\n=================================\n")


# players manager menu
    def _player_manager_menu(self):
        while True:
            print("\n=========================Players Manager=========================\n")
            print("1. Add Player")
            print("2. Remove Player")
            print("3. Add Group")
            print("4. Remove Group")
            print("5. Players and groups tree")
            print("6. Exit Players Manager")
            
            choice = input("\nPlease select an option:\n")
            
            if choice == '1': 
                print("\n===============Adding a new player===============\n")
                self.add_player()

            elif choice == '2':
                print("\n===============Removing a player===============\n")
                self.remove_player()

            elif choice == '3':
                print("\n===============Adding a new group===============\n")
                self.add_group()

            elif choice == '4':
                print("\n===============Removing a group===============\n")
                self.remove_group()

            elif choice == '5':
                print("\n===============Players and groups tree===============\n")
                self.players_and_groups_tree()   

            elif choice == '6':
                print("\n===============Exiting Players Manager......\n")
                break

            else:
                print("\nInvalid choice. Please try again.\n")

    def add_player(self):
        while True:

            exit = input("Enter '0' to cancel adding a new player or press Enter to continue: ")
            if exit == '0':
                print("\nAdding new player cancelled.\n")
                break

            player_name = input("Enter player name: ")
            player_age = input("Enter player age (Years only): ")

            if not self.groups_dict: # check if there are no groups befor asking the player to choose a group
                print("\nNo groups available\n")
                print("\nPlayer will be created without a group\n")
                player_group_choice = 'n'
            else:
                player_group_choice = input("Would you like to assign the player to a group ? (y/n): ")

            if player_name in self.players_dict:
                print("\nPlayer already exists. Please choose a different name.\n")

            elif not self._validate_name(player_name):
                print("\nInvalid name. Please enter a valid name.\n")

            elif (player_age is None or not player_age.isdigit()
                        or int(player_age) < 1 or int(player_age) > 120):

                print("\nInvalid age. Please enter a valid age between 1 and 120.\n")
            
            elif player_group_choice == "n":
                print("The player will not be assigned to any group")
                new_player = Player(player_name, int(player_age), None) #create obj player without group
                self.players_dict[player_name] = new_player # add player obj to players dict
                break
            
            elif player_group_choice == 'y':
                self._print_groups()
                group_number = input("Enter the group number to assign the player to: ")

                if not group_number.isdigit() or int(group_number) < 1 or int(group_number) > len(self.groups_dict):
                    print("\nInvalid group number. Please try again.\n")
        
                else:
                    group_name = list(self.groups_dict.keys())[int(group_number) - 1]
                    new_player = Player(player_name, int(player_age), self.groups_dict[group_name]) # create obj player with group
                    self.groups_dict[group_name].add_player(new_player) # add player obj to group
                    self.players_dict[player_name] = new_player # add player obj to players dict
                    break

            else:
                print("\nInvalid choice. Please enter 'y' or 'n'.\n")

    def remove_player(self):
        while True:

            self._print_players()
            player_number = input("Enter the player number to remove: ")

            if player_number == '0':
                print("\nPlayer removal cancelled.\n")
                break

            elif not player_number.isdigit() or int(player_number) < 1 or int(player_number) > len(self.players_dict):
                print("\nInvalid player number. Please try again.\n")
    
            else:
                player_name = list(self.players_dict.keys())[int(player_number) - 1]
                player = self.players_dict[player_name]
                player_group = player.group
                
                if player_group is not None:
                    player_group.remove_player(player)  # Remove player from their group

                del self.players_dict[player_name]
                print(f"\nPlayer {player_name} removed successfully.\n")
                break

    def add_group(self):
        while True:

            exit = input("Enter '0' to cancel adding a new group or press Enter to continue: ")
            if exit == '0':
                print("\nAdding new group cancelled.\n")
                break

            group_name = input("Enter the new group name: ")

            if not self.groups_dict: # check if there are no groups befor asking the player to choose a group
                print("\nNo groups available\n")
                print("\nGroup will be created without mother group\n")

                mother_group_choice = 'n'
            else:
                mother_group_choice = input("Would you like to assign a mother group ? (y/n): ")

            if group_name in self.groups_dict:
                print("\nGroup already exists. Please choose a different name.\n")

            elif not self._validate_name(group_name):
                print("\nInvalid group name. Please enter a valid name.\n")
            
            elif mother_group_choice == 'n':
                new_group = Group(group_name) #create obj group without mother group
                self.groups_dict[group_name] = new_group # add group obj to groups dict
                break

            elif mother_group_choice == 'y':
                self._print_groups()
                group_number = input("Enter the group number to assign as mother group: ")

                if not group_number.isdigit() or int(group_number) < 1 or int(group_number) > len(self.groups_dict):
                    print("\nInvalid group number. Please try again.\n")
        
                else:
                    mother_group_name = list(self.groups_dict.keys())[int(group_number) - 1]
                    new_group = Group(group_name, self.groups_dict[mother_group_name]) # create obj group with mother group
                    self.groups_dict[group_name] = new_group # add group obj to groups dict

                    mother_group = self.groups_dict[mother_group_name]
                    mother_group.sub_groups.append(new_group)  # Add new group as a sub-group to mother group
                    
                    break

            else:
                print("\nInvalid choice. Please enter 'y' or 'n'.\n")

    def remove_group(self):
        while True:
            self._print_groups()
            group_number = input("Enter the group number to remove: ")

            if group_number == '0':
                print("\nGroup removal cancelled.\n")
                break

            elif not group_number.isdigit() or int(group_number) < 1 or int(group_number) > len(self.groups_dict):
                print("\nInvalid group number. Please try again.\n")
    
            else:
                group_name = list(self.groups_dict.keys())[int(group_number) - 1]

                group = self.groups_dict[group_name]

                for player in group.players:
                    player.group = None  # Remove group association from players

                mother_group = group.mother_group

                if mother_group is not None:
                    mother_group.sub_groups.remove(group)  # Remove from mother group's sub-groups
                
                if group.sub_groups is not None:
                    for sub_group in group.sub_groups:
                        sub_group.mother_group = None  # Remove mother group association from sub-groups
                


                del self.groups_dict[group_name]
                print(f"\nGroup {group_name} removed successfully.\n")
                break
    
    def players_and_groups_tree(self):
        print("\n===============Players and Groups Tree===============\n")
        if not self.players_dict and not self.groups_dict:
            print("No players or groups available.\n")

        else:
            for player in self.players_dict.values():
                if player.group is None:
                    print(f"|-- {player.name} (Score: {player.score})")
            
            for group in self.groups_dict.values():
                if group.mother_group is None:
                    self._print_group_tree(group, 0)


# helper methods
    def _print_group_tree(self, group, level):

        indent_group = "    " * level
        indent_player = "    " * (level + 1)

        print(f"{indent_group}|-- [Group] {group.group_name} (Total Score: {group.get_total_score()})")
        
        for player in group.players:
            print(f"{indent_player}|-- {player.name} (Score: {player.score})")
        
        for sub_group in group.sub_groups:
            self._print_group_tree(sub_group, level + 1)

    def _print_groups(self):
        print("\n Available Groups: \n")

        if not self.groups_dict:
            print("No groups available.\n")

        else:   
            print("0. Cancel\n")
            number = 1
            for group in self.groups_dict.values():
                print(f"{number}. {group.group_name}")
                number += 1
        
    def _print_players(self):
        if not self.players_dict and not self.groups_dict:
            print("No players available.\n")

        else:
            print("\n Available Players: \n")
            print("0. Cancel\n")
            number = 1
            for player in self.players_dict.values():
                print(f"{number}. {player.name}")
                number += 1
        
    def _validate_name(self, name):
        
        if not name:
            return False

        elif len(name) < 2 or len(name) > 15:
            return False
        
        for char in name:
            if not char.isalpha() and not char.isspace() and not char.isdigit():
                return False
        
        return True

    def _sort_players_by_score(self):
        player_list = list(self.players_dict.values())


        player_len = len(player_list)
        for i in range(player_len):
            max_index = i

            for j in range(i + 1, player_len):
                if player_list[j].score > player_list[max_index].score:
                    max_index = j
            player_list[i], player_list[max_index] = player_list[max_index], player_list[i]

        return player_list[:5]  # Return top 5 players
     
    def _sort_groups_by_score(self):
        groups_list = list(self.groups_dict.values())

        group_len = len(groups_list)

        for i in range(group_len):
            max_index = i

            for j in range(i + 1, group_len):
                if groups_list[j].get_total_score() > groups_list[max_index].get_total_score():
                    max_index = j
            groups_list[i], groups_list[max_index] = groups_list[max_index], groups_list[i]
        
        return groups_list[:5]  # Return top 5 groups

