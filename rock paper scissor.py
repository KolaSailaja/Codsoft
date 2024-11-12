import random
import time
import os

class RockPaperScissors:
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']
        self.symbols = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
        self.player_score = 0
        self.computer_score = 0
        self.winning_messages = [
            "🌟 AMAZING! You're a superstar! 🌟",
            "🎉 WONDERFUL! Keep shining! 🎉",
            "⭐ YOU DID IT! You're awesome! ⭐"
        ]
        # Modified losing messages to be more appreciative
        self.losing_messages = [
            "🌟 Great strategy! You're making this challenging! 🌟",
            "✨ Impressive move! You're a worthy opponent! ✨",
            "🎯 What a match! Your gameplay is fantastic! 🎯",
            "🌈 Amazing effort! You're making me better! 🌈",
            "💫 Brilliant play! Your skills are growing! 💫"
        ]
        self.tie_messages = [
            "🤝 It's a tie! Great minds think alike! 🤝",
            "🎨 Wow! You both chose the same! 🎨",
            "🎯 It's a draw! Let's play again! 🎯"
        ]

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_title(self):
        title = """
        🎮 ROCK PAPER SCISSORS 🎮
        ========================
        """
        print(title)

    def print_scores(self):
        score_display = f"""
        📊 SCORES 📊
        You: {self.player_score} 👤  |  Computer: {self.computer_score} 🤖
        """
        print(score_display)

    def get_player_choice(self):
        while True:
            print("\nMake your choice!")
            for i, choice in enumerate(self.choices, 1):
                print(f"{i}. {choice.title()} {self.symbols[choice]}")
            
            try:
                choice = input("\nEnter your choice (1-3): ")
                if choice.isdigit() and 1 <= int(choice) <= 3:
                    return self.choices[int(choice) - 1]
                else:
                    print("Oops! Please enter a number between 1 and 3!")
            except ValueError:
                print("Oops! Please enter a valid number!")

    def get_computer_choice(self):
        return random.choice(self.choices)

    def determine_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            return 'tie'
        elif ((player_choice == 'rock' and computer_choice == 'scissors') or
              (player_choice == 'paper' and computer_choice == 'rock') or
              (player_choice == 'scissors' and computer_choice == 'paper')):
            return 'win'
        else:
            return 'lose'

    def display_choices(self, player_choice, computer_choice):
        print(f"\nYour choice: {self.symbols[player_choice]} {player_choice.title()}")
        print(f"Computer's choice: {self.symbols[computer_choice]} {computer_choice.title()}")

    def display_result(self, result):
        if result == 'win':
            message = random.choice(self.winning_messages)
            print(f"\n{message}")
            self.player_score += 1
        elif result == 'lose':
            message = random.choice(self.losing_messages)
            print(f"\n{message}")
            self.computer_score += 1
        else:
            message = random.choice(self.tie_messages)
            print(f"\n{message}")

    def play_again(self):
        while True:
            choice = input("\nWould you like to play again? (yes/no): ").lower()
            if choice in ['yes', 'no', 'y', 'n']:
                return choice.startswith('y')
            print("Oops! Please enter 'yes' or 'no'!")

    def play_game(self):
        while True:
            self.clear_screen()
            self.print_title()
            self.print_scores()
            
            # Get choices
            player_choice = self.get_player_choice()
            print("\n🎮 Rock...")
            time.sleep(0.5)
            print("📄 Paper...")
            time.sleep(0.5)
            print("✂️ Scissors...")
            time.sleep(0.5)
            print("👾 Shoot!\n")
            time.sleep(0.5)
            
            computer_choice = self.get_computer_choice()
            
            # Show choices and result
            self.display_choices(player_choice, computer_choice)
            result = self.determine_winner(player_choice, computer_choice)
            self.display_result(result)
            
            # Ask to play again
            if not self.play_again():
                self.clear_screen()
                self.print_title()
                self.print_scores()
                print("\nThanks for playing! Come back soon! 👋")
                break

if __name__ == "__main__":
    game = RockPaperScissors()
    game.play_game()
