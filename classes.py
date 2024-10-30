import random 
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class Contract:
    def __init__(self, config):
        self.config = config
        self.material_drop_chances = self.config.contract_material_drop_chances

    def complete(self, player, game):
        """Complete a contract."""
        if player.pioneer_points < 3:
            game.log_action(f"{player.name} does not have enough pioneer points to complete a contract")
            return
        player.pioneer_points -= 3
        player.yoku += 1
        game.log_action(f"{player.name} completed a contract and earned 1 yoku")
        # Roll for material
        material_rarity = self.roll_material()
        player.materials[material_rarity] += 1
        game.log_action(f"{player.name} received {material_rarity} material from the contract")

    def roll_material(self):
        """Roll for material reward."""
        result = random.random()
        cumulative = 0.0
        for rarity, chance in self.material_drop_chances.items():
            cumulative += chance
            if result < cumulative:
                return rarity
        # Default to 'rare' if no other rarity is selected
        return 'rare'

class Lootbox:
    def __init__(self, config):
        self.config = config
        self.loot_drop_chances = self.config.lootbox_loot_drop_chances
        self.pet_drop_chance = self.config.lootbox_pet_drop_chance

    def open(self, player, game):
        """Open the lootbox and grant rewards to the player."""
        # Roll for loot
        loot_rarity = self.roll_loot()
        player.add_gear(loot_rarity, game)
        # Roll for pet
        pet_received = self.roll_pet()
        if pet_received:
            player.pets.append(pet_received)
            game.log_action(f"{player.name} received a pet from the lootbox: {pet_received}")

    def roll_loot(self):
        """Roll to determine loot received from a lootbox."""
        result = random.random()
        cumulative = 0.0
        for rarity, chance in self.loot_drop_chances.items():
            cumulative += chance
            if result < cumulative:
                return rarity
        # Default to 'uncommon' if no other rarity is selected
        return 'uncommon'

    def roll_pet(self):
        """Roll to determine if a pet is received from a lootbox."""
        result = random.random()
        if result < self.pet_drop_chance:
            return 'Lootbox Pet'
        else:
            return None
class Player:
    def __init__(self, name, config, activity_level=1.0, play_frequency=1):
        self.name = name
        self.config = config
        self.activity_level = activity_level  # % of rounds played (0.0 to 1.0)
        self.play_frequency = play_frequency  # Days between play sessions
        self.last_play_day = 0  # Track the last day played
        self.rounds_played = 0  # Track number of rounds played
        
        # Initialize resources
        self.yoku = 3
        self.pioneer_points = 6
        self.skull_tokens = 0  # Pity system
        # Materials - Updated to include all rarities
        self.materials = {
            'legendary': 0,
            'epic': 0,
            'rare': 0,
            'uncommon': 0,
            'common': 0
        }
        # Gear inventory, max 5 items
        self.gear = []  # List to hold gear items
        self.pets = []
        # Dungeon stats
        self.dungeon_attempts = {1: 0, 2: 0, 3: 0}
        self.dungeon_completions = {1: 0, 2: 0, 3: 0}
        # Data over time
        self.turns = []
        self.gear_levels_over_time = []
        # Also update the materials_over_time tracking
        self.materials_over_time = {
            'legendary': [],
            'epic': [],
            'rare': [],
            'uncommon': [],
            'common': []
        }
        self.completions_over_time = []
        self.win_rates_over_time = {1: [], 2: [], 3: []}

    def reset_daily_resources(self):
        """Reset daily resources - no longer used."""
        pass  # Removed the daily reset since we use round based system

    def add_periodic_resources(self, game):
        """Add resources every 6 rounds."""
        self.yoku += 1
        self.pioneer_points += 2
        game.log_action(f"{self.name} received 1 yoku and 2 pioneer points")

    def attempt_dungeon(self, dungeon, game):
        """Attempt a dungeon run."""
        if self.yoku < 1:
            game.log_action(f"{self.name} does not have enough yoku to enter the dungeon")
            return
        self.yoku -= 1  # Spend 1 yoku to enter dungeon
        self.dungeon_attempts[dungeon.tier] += 1  # Increment attempts

        success = dungeon.attempt(self, game)
        if success:
            self.dungeon_completions[dungeon.tier] += 1  # Increment completions

            game.log_action(f"{self.name} successfully completed Tier {dungeon.tier} dungeon!")
            # Loot roll
            loot_rarity = dungeon.roll_loot()
            self.add_gear(loot_rarity, game)
            # Material roll
            material_rarity = dungeon.roll_material()
            self.materials[material_rarity] += 1
            game.log_action(f"{self.name} received {material_rarity} material")
            # Pet roll
            pet_received = dungeon.roll_pet()
            if pet_received:
                self.pets.append(pet_received)
                game.log_action(f"{self.name} received a pet: {pet_received}")
            # Guaranteed currency for completing dungeon
            self.skull_tokens += 1
            self.pioneer_points += 1
            game.log_action(f"{self.name} received a skull token and a pioneer credit")
        else:
            game.log_action(f"{self.name} failed to complete Tier {dungeon.tier} dungeon")

    def complete_contract(self, game):
        """Complete a contract using pioneer points."""
        contract = Contract(self.config)
        contract.complete(self, game)

    def purchase_lootbox(self, game):
        """Purchase a pity lootbox."""
        if self.skull_tokens < 5 or self.materials['epic'] < 5 or self.materials['rare'] < 5:
            print(f"{self.name} does not have enough resources to purchase a lootbox.")
            return
        self.skull_tokens -= 1
        self.materials['rare'] -= 1
        self.materials['epic'] -= 1
        print(f"{self.name} purchased a lootbox.")
        # Open the lootbox
        lootbox = Lootbox(self.config)
        lootbox.open(self, game)

    def add_gear(self, gear_rarity, game):
        """Add gear to inventory, replacing lowest tier if full."""
        gear_tier_values = self.config.gear_tier_values
        print(f"{self.name} received {gear_rarity} gear.")
        if len(self.gear) < 5:
            # Add the new gear
            self.gear.append(gear_rarity)
            print(f"{self.name} equipped {gear_rarity} gear.")
            game.log_action(f"{self.name} equipped {gear_rarity} gear")
        else:
            # Find the lowest-tier gear
            lowest_tier_gear = min(self.gear, key=lambda x: gear_tier_values[x])
            if gear_tier_values[gear_rarity] > gear_tier_values[lowest_tier_gear]:
                # Replace the lowest-tier gear
                self.gear.remove(lowest_tier_gear)
                self.gear.append(gear_rarity)
                print(f"{self.name} replaced {lowest_tier_gear} gear with {gear_rarity} gear.")
                game.log_action(f"{self.name} replaced {lowest_tier_gear} gear with {gear_rarity} gear")
            else:
                print(f"{self.name}'s gear slots are full. {gear_rarity} gear was discarded.")
                game.log_action(f"{self.name}'s gear slots are full. {gear_rarity} gear was discarded")

    def calculate_gear_bonus(self):
        """Calculate gear bonus based on equipped gear."""
        gear_bonus_values = self.config.gear_bonus_values
        total_bonus = 0.0
        for gear_rarity in self.gear:
            bonus_per_gear = gear_bonus_values.get(gear_rarity, 0)
            total_bonus += bonus_per_gear
        return total_bonus

    def record_stats(self, turn_number):
        """Record stats for plotting."""
        # Record the turn number
        self.turns.append(turn_number)
        # Record gear level (sum of gear tier values)
        gear_tier_values = self.config.gear_tier_values
        gear_level = sum([gear_tier_values[gear] for gear in self.gear])
        self.gear_levels_over_time.append(gear_level)
        # Record materials - Updated to include all rarities
        for material in ['legendary', 'epic', 'rare', 'uncommon', 'common']:
            self.materials_over_time[material].append(self.materials[material])
        # Record total dungeon completions
        total_completions = sum(self.dungeon_completions.values())
        self.completions_over_time.append(total_completions)
        # Record win rates per tier
        for tier in [1, 2, 3]:
            attempts = self.dungeon_attempts[tier]
            completions = self.dungeon_completions[tier]
            win_rate = (completions / attempts * 100) if attempts > 0 else 0
            self.win_rates_over_time[tier].append(win_rate)

    def should_play_today(self, current_day):
        """Determine if the player should play on the current day"""
        # If it's day 1, always play
        if current_day == 1:
            self.last_play_day = 1
            return True
            
        # Check if enough days have passed since last play day
        days_since_last_play = current_day - self.last_play_day
        if days_since_last_play >= self.play_frequency:
            # Only update last_play_day at the start of a new day, not every round
            if current_day > self.last_play_day:
                self.last_play_day = current_day - 1  # Set to previous day
            return True
        return False

    def should_play_round(self):
        """Determine if the player should play this round based on activity level"""
        # If activity level is 100%, always play
        if self.activity_level >= 1.0:
            return True
            
        # For other activity levels, calculate rounds between plays
        if self.activity_level <= 0:
            return False
            
        rounds_between_plays = int(1 / self.activity_level)
        should_play = (self.rounds_played % rounds_between_plays) == 0
        self.rounds_played += 1
        return should_play
class Dungeon:
    def __init__(self, tier, config):
        self.tier = tier
        self.config = config
        self.win_probabilities = self.config.dungeon_win_probabilities
        self.loot_drop_chances = self.config.dungeon_loot_drop_chances[tier]
        self.material_drop_chances = self.config.dungeon_material_drop_chances[tier]
        self.pet_drop_chances = self.config.dungeon_pet_drop_chances

    def attempt(self, player, game):
        """Check if player wins, factoring in gear bonus."""
        base_win_chance = self.win_probabilities[self.tier]
        gear_bonus = player.calculate_gear_bonus()
        total_win_chance = base_win_chance + gear_bonus
        result = random.random()
        success = result < total_win_chance
        game.log_action(
            f"{player.name}'s chance to win was {total_win_chance * 100:.2f}% "
            f"(Base: {base_win_chance * 100:.2f}%, Gear Bonus: {gear_bonus * 100:.2f}%)"
        )
        return success

    def roll_loot(self):
        """Roll to determine the loot rarity received."""
        result = random.random()
        cumulative = 0.0
        for rarity, chance in self.loot_drop_chances.items():
            cumulative += chance
            if result < cumulative:
                return rarity
        return 'uncommon'  # Default to 'uncommon'

    def roll_material(self):
        """Roll to determine the material rarity received."""
        result = random.random()
        cumulative = 0.0
        for rarity, chance in self.material_drop_chances.items():
            cumulative += chance
            if result < cumulative:
                return rarity
        return 'rare'  # Default to 'rare'

    def roll_pet(self):
        """Roll to determine if a pet is received."""
        chance = self.pet_drop_chances[self.tier]
        result = random.random()
        if result < chance:
            return f"Pet Tier {self.tier}"
        else:
            return None
class Game:
    def __init__(self, players, config, rounds_per_day=10):
        self.players = players
        self.config = config
        self.current_day = 1
        self.current_round = 1
        self.rounds_per_day = rounds_per_day
        self.total_turns = 0  # To track the number of turns
        self.action_log = []  # Add this line

    def log_action(self, message):
        """Add a message to the action log."""
        self.action_log.append(f"[Day {self.current_day}, Round {self.current_round}] {message}")

    def start_day(self):
        """Initialize resources at the start of each day."""
        self.log_action(f"Starting Day {self.current_day}")
        self.current_round = 1

    def play_round(self):
        """Execute a single round."""
        self.log_action(f"Starting Round {self.current_round}")
        
        # Add periodic resources every 6 rounds
        if self.total_turns > 0 and self.total_turns % 6 == 0:
            for player in self.players:
                player.add_periodic_resources(self)
        
        for player in self.players:
            plays_today = player.should_play_today(self.current_day)
            
            if plays_today:
                if player.should_play_round():
                    self.play_turn(player)
                else:
                    print(f"{player.name} skipping round due to activity level")
            else:
                print(f"{player.name} not playing on day {self.current_day}")
            
            player.record_stats(self.total_turns)
        
        self.current_round += 1
        self.total_turns += 1
        if self.current_round > self.rounds_per_day:
            self.current_day += 1
            self.current_round = 1

    def play_turn(self, player):
        """Player's action for their turn."""
        choices = []
        if player.yoku >= 1:
            choices.append('dungeon')
        if player.pioneer_points >= 3:
            choices.append('contract') 

        if not choices:
            print(f"{player.name} has no actions to take this turn.")
            return
        
        action = random.choice(choices)
        if action == 'dungeon':
            # Determine dungeon tier based on gear level and probabilities
            gear_level = player.calculate_gear_bonus()
            tier_choice = self.choose_dungeon_tier(gear_level)
            dungeon = Dungeon(tier_choice, self.config)
            player.attempt_dungeon(dungeon, self)
        elif action == 'contract':
            player.complete_contract(self)
        
        # Attempt to purchase lootboxes after the main action
        while (player.skull_tokens >= 5 and player.materials['epic'] >= 5 and player.materials['rare'] >= 5):
            player.purchase_lootbox(self)

    def choose_dungeon_tier(self, gear_level):
        """Choose a dungeon tier based on gear level and defined probabilities."""
        gear_modifier_tier_1 = self.config.dungeon_choice_probabilities['tier_1']['gear_modifier']
        gear_modifier_tier_2 = self.config.dungeon_choice_probabilities['tier_2']['gear_modifier']
        gear_modifier_tier_3 = self.config.dungeon_choice_probabilities['tier_3']['gear_modifier']
        # Define base probabilities for each tier
        base_probabilities = {
            1: 10,  # High probability for Tier 1
            2: 5,  # Lower probability for Tier 2
            3: 1   # Lowest probability for Tier 3
        }

        # Scale probabilities based on gear level
        # The higher the gear level, the more likely to choose higher tiers
        probabilities = {
            1: base_probabilities[1],  # Increase for Tier 1
            2: base_probabilities[2] + (gear_modifier_tier_2* gear_level),  # Increase for Tier 2
            3: base_probabilities[3] + (gear_modifier_tier_3 * gear_level)   # Increase for Tier 3
        }

        # Normalize probabilities
        total_probability = sum(probabilities.values())
        if total_probability == 0:
            return 1  # Default to Tier 1 if no valid probabilities

        # Normalize the probabilities
        probabilities = {tier: prob / total_probability for tier, prob in probabilities.items()}

        # Choose a tier based on the calculated probabilities
        random_choice = random.uniform(0, 1)
        cumulative_probability = 0.0
        for tier, prob in probabilities.items():
            cumulative_probability += prob
            if random_choice < cumulative_probability:
                return tier

        return 1  # Default to Tier 1 if something goes wrong

    def run(self, days=1):
        """Run the game for a specified number of days."""
        self.start_day()
        total_rounds = days * self.rounds_per_day
        while self.current_day <= days and self.current_round <= self.rounds_per_day:
            self.play_round()

    def display_stats(self):
        """Display the stats for each player at the end of the game."""
        print("\n--- Game Stats ---")
        for player in self.players:
            print(f"\nPlayer Name: {player.name}")
            print(f"Gear Equipped ({len(player.gear)}/5): {', '.join(player.gear) if player.gear else 'None'}")
            print("Materials:")
            for material, count in player.materials.items():
                print(f"  {material.capitalize()}: {count}")
            print(f"Pets Collected: {', '.join(player.pets) if player.pets else 'None'}")
            print("Dungeon Attempts and Completions:")
            for tier in [1, 2, 3]:
                attempts = player.dungeon_attempts[tier]
                completions = player.dungeon_completions[tier]
                completion_rate = (completions / attempts * 100) if attempts > 0 else 0
                print(f"  Tier {tier} - Attempts: {attempts}, Completions: {completions}, Completion Rate: {completion_rate:.2f}%")
            total_attempts = sum(player.dungeon_attempts.values())
            total_completions = sum(player.dungeon_completions.values())
            overall_completion_rate = (total_completions / total_attempts * 100) if total_attempts > 0 else 0
            print(f"Overall Dungeon Completion Rate: {overall_completion_rate:.2f}%")
            
    def plot_stats(self):
        """Plot the stats collected over time using matplotlib and seaborn."""
        sns.set_theme(style="darkgrid")
        for player in self.players:
            # Split columns for side-by-side display
            col1, col2 = st.columns(2)

            # Plot Gear Level Over Time
            with col1:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(player.turns, player.gear_levels_over_time, marker='o')
                ax.set_title(f"{player.name} - Gear Level Over Time")
                ax.set_xlabel("Turn")
                ax.set_ylabel("Gear Level (Sum of Gear Tiers)")
                st.pyplot(fig)
                plt.clf()

            # Plot Materials Over Time
            with col2:
                fig, ax = plt.subplots(figsize=(10, 6))
                for material in ['legendary', 'epic', 'rare', 'uncommon', 'common']:
                    ax.plot(player.turns, player.materials_over_time[material], label=material.capitalize())
                ax.set_title(f"{player.name} - Materials Over Time")
                ax.set_xlabel("Turn")
                ax.set_ylabel("Quantity")
                ax.legend()
                st.pyplot(fig)
                plt.clf()

            # Plot Dungeon Completions Over Time
            with col2:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(player.turns, player.completions_over_time, marker='o')
                ax.set_title(f"{player.name} - Total Dungeon Completions Over Time")
                ax.set_xlabel("Turn")
                ax.set_ylabel("Total Completions")
                st.pyplot(fig)
                plt.clf()

            # Plot Win Rates Per Tier Over Time
            for tier in [1, 2, 3]:
                with col1:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(player.turns, player.win_rates_over_time[tier], marker='o')
                    ax.set_title(f"{player.name} - Win Rate Over Time for Tier {tier}")
                    ax.set_xlabel("Turn")
                    ax.set_ylabel("Win Rate (%)")
                    st.pyplot(fig)
                    plt.clf()

