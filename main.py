import random 

class Player:
    def __init__(self, name, bowling, batting, fielding, running, experience):
        self.name = name 
        self.bowling = bowling 
        self.batting = batting 
        self.fielding = fielding 
        self.running = running 
        self.experience = experience

class Team:
    def __init__(self, name, players):
        self.name = name 
        self.players = players 
        self.captain = None 
        self.batting_order = players.copy()
        self.bowlers = []

    def select_captain(self, captain):
        self.captain = captain

    def sending_next_player(self):
        if len(self.batting_order)>0:
            return self.batting_order.pop(0)
        return None 
    
    def choose_bowler(self):
        return random.choice(self.bowlers)
    

class Field:
    def __init__(self, size, fan_ratio, pitch_conditions, home_advantage):
        self.size = size
        self.fan_ratio = fan_ratio
        self.pitch_conditions = pitch_conditions
        self.home_advantage = home_advantage


class Umpire:
    def __init__(self, field):
        self.field = field
        self.scores = 0
        self.wickets = 0
        self.overs = 0

    def update_score(self, runs):
        """
        Updates the score based on the runs scored.
        """
        self.scores += runs

    def update_wickets(self):
        """
        Updates the wickets count.
        """
        self.wickets += 1

    def update_overs(self):
        """
        Updates the overs count.
        """
        self.overs += 1

    def predict_outcome(self, batsman, bowler):
        """
        Predicts the outcome of a ball based on batsman and bowler stats.
        """
        batting_prob = batsman.batting * self.field.pitch_conditions * random.random()
        bowling_prob = bowler.bowling * self.field.pitch_conditions * random.random()
        if batting_prob > bowling_prob:
            return "OUT"
        return "NOT OUT"

class Commentator:
    def __init__(self, umpire):
        self.umpire = umpire

    def describe_ball(self, batsman, bowler):
        """
        Generates a description of the ball played by the batsman.
        """
        outcome = self.umpire.predict_outcome(batsman, bowler)
        print("Outcome: ", outcome)
        if outcome == "OUT":
            description = f"{batsman.name} is OUT!"
        else:
            description = f"{batsman.name} plays the shot."

        return description

    def describe_game(self, captain1, captain2, country1, country2, over):
        print("\n--------- Game Information ---------\n")
        print(f"{country1} Vs {country2}")
        print(f"Captain 1 : {captain1}, Captain 2 : {captain2}")
        print(f"Over : {over}")
        print("\n---------------------------------------------\n")

    def describe_start(self, team):
        print("\n------------- GAME STARTED ------------------\n")
        print(f"Team {team} playing: ")
    
    def describe_end(self):
        print(f"\n\nFinal Run: {self.umpire.scores} Wicket: {self.umpire.wickets} Overs: {self.umpire.overs}")
        print("\n---------------------------------------------\n")

    
    def current_info(self, ball_count):
        print(f"Balls: {ball_count} Over: {self.umpire.overs} Run: {self.umpire.scores}  Wicket: {self.umpire.wickets}")

    def describe_final_result(self, name, scores):
        print("--------------- Winner -----------------------")
        print(f"TEAM : {name} WON BY SCORE: {scores}")
        print("\n---------------------------------------------\n")

class Match:
    def __init__(self, team1, team2, field, total_overs):
        self.team1 = team1
        self.team2 = team2
        self.field = field
        self.umpire = Umpire(field)
        self.commentator = Commentator(self.umpire)
        self.total_overs = total_overs

    def start_match(self):
        """
        Starts the cricket match.
        """
        self.team1.select_captain(random.choice(self.team1.players))
        self.team2.select_captain(random.choice(self.team2.players))
        self.team1.batting_order = self.team1.players.copy()
        self.team2.batting_order = self.team2.players.copy()
        self.team1.bowlers = self.team1.players.copy()
        self.team2.bowlers = self.team2.players.copy()

        self.commentator.describe_game(self.team1.captain.name, self.team2.captain.name, self.team1.name, self.team2.name, over=5)

        # Team 1 playing    
        self.commentator.describe_start(self.team1.name)
        self.play_innings(self.team1, self.team2)
        self.commentator.describe_end()
        lastScores = self.commentator.umpire.scores


        # Team 2 playing    
        self.commentator.umpire.scores = 0
        self.commentator.umpire.wickets = 0
        self.commentator.describe_start(self.team2.name)
        self.play_innings(self.team2, self.team1)
        self.commentator.describe_end()
        newScores = self.commentator.umpire.scores

        # final outcome
        if lastScores > newScores:
            self.commentator.describe_final_result(team1.name, lastScores)
        else:
            self.commentator.describe_final_result(team2.name, newScores)


    def play_innings(self, batting_team, bowling_team):
        """
        Simulates the innings of a team.
        """
        ball_count = 1
        over = 0
        bowler = bowling_team.choose_bowler() 
        batsman = batting_team.sending_next_player()
        
        while over < self.total_overs:
            print("\n")
            self.commentator.current_info(ball_count)
            ball_description = self.commentator.describe_ball(batsman, bowler)
            
            print(ball_description)
            if ball_description.endswith("OUT!"):
                batsman = batting_team.sending_next_player()
                if batsman is None:
                    break
                self.umpire.update_wickets()
                print(f"Wickets: {self.umpire.wickets} , Overs: {self.umpire.overs}")
                print(f"New player {batsman.name} is playing...")
            else:
                runs = random.randint(0, 6)
                self.umpire.update_score(runs)

            if ball_count > 5:
                over += 1
                print(f"Over {over} Starting...")
                self.umpire.update_overs()
                bowler = bowling_team.choose_bowler()
                ball_count = 0

            self.commentator.current_info(ball_count)
            ball_count += 1


# Adding the players
player1 = []
for i in range(10):
    player1.append(Player("Player1_"+str(i+1), round(random.random(),1), round(random.random(),1),round(random.random(),1), round(random.random(),1), round(random.random(),1)))

player2 = []
for i in range(10):
    player2.append(Player("Player2_"+str(i+1), round(random.random(),1), round(random.random(),1),round(random.random(),1), round(random.random(),1), round(random.random(),1)))

# Adding players to team
team1 = Team("Country1", player1)
team2 = Team("Country2", player2)

# showing the field
field = Field("Large", 0.7, 0.8, 0.9)

# starting match simulation
total_overs = 20
match = Match(team1, team2, field, total_overs)
match.start_match()
