import random 
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class Contract:
    def __init__(self, config):
        self.config = config
        self.material_drop_chances = self.config.contract_material_drop_chances

    def complete(self, player):
        """Complete a contract."""
        if player.pioneer_points < 3:
            print(f"{player.name} does not have enough pioneer points to complete a contract.")
            return
        player.pioneer_points -= 3  # Costs 3 pioneer points
        player.yoku += 1  # Rewards 1 yoku
        print(f"{player.name} completed a contract and earned 1 yoku.")
        # Roll for material
        material_rarity = self.roll_material()
        player.materials[material_rarity] += 1
        print(f"{player.name} received {material_rarity} material from the contract.")

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

    def open(self, player):
        """Open the lootbox and grant rewards to the player."""
        # Roll for loot
        loot_rarity = self.roll_loot()
        player.add_gear(loot_rarity)
        # Roll for pet
        pet_received = self.roll_pet()
        if pet_received:
            player.pets.append(pet_received)
            print(f"{player.name} received a pet from the lootbox: {pet_received}.")

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
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.yoku = 3  # Starting yoku
        self.pioneer_points = 6  # Starting pioneer points
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
        pass  # Remove the daily reset since we're using a round-based system

    def add_periodic_resources(self):
        """Add resources every 6 rounds."""
        self.yoku += 1
        self.pioneer_points += 2
        print(f"{self.name} received 1 yoku and 2 pioneer points.")

    def attempt_dungeon(self, dungeon):
        """Attempt a dungeon run."""
        if self.yoku < 1:
            print(f"{self.name} does not have enough yoku to enter the dungeon.")
            return
        self.yoku -= 1  # Spend 1 yoku to enter dungeon
        self.dungeon_attempts[dungeon.tier] += 1  # Increment attempts

        success = dungeon.attempt(self)
        if success:
            self.dungeon_completions[dungeon.tier] += 1  # Increment completions

            print(f"{self.name} successfully completed Tier {dungeon.tier} dungeon!")
            # Loot roll
            loot_rarity = dungeon.roll_loot()
            self.add_gear(loot_rarity)
            # Material roll
            material_rarity = dungeon.roll_material()
            self.materials[material_rarity] += 1
            print(f"{self.name} received {material_rarity} material.")
            # Pet roll
            pet_received = dungeon.roll_pet()
            if pet_received:
                self.pets.append(pet_received)
                print(f"{self.name} received a pet: {pet_received}.")
            # Guaranteed currency for completing dungeon
            self.skull_tokens += 1
            self.pioneer_points += 1
            print(f"{self.name} received a skull token and a pioneer credit.")
        else:
            print(f"{self.name} failed to complete Tier {dungeon.tier} dungeon.")

    def complete_contract(self):
        """Complete a contract using pioneer points."""
        contract = Contract(self.config)
        contract.complete(self)

    def purchase_lootbox(self):
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
        lootbox.open(self)

    def add_gear(self, gear_rarity):
        """Add gear to inventory, replacing lowest tier if full."""
        gear_tier_values = self.config.gear_tier_values
        print(f"{self.name} received {gear_rarity} gear.")
        if len(self.gear) < 5:
            # Add the new gear
            self.gear.append(gear_rarity)
            print(f"{self.name} equipped {gear_rarity} gear.")
        else:
            # Find the lowest-tier gear
            lowest_tier_gear = min(self.gear, key=lambda x: gear_tier_values[x])
            if gear_tier_values[gear_rarity] > gear_tier_values[lowest_tier_gear]:
                # Replace the lowest-tier gear
                self.gear.remove(lowest_tier_gear)
                self.gear.append(gear_rarity)
                print(f"{self.name} replaced {lowest_tier_gear} gear with {gear_rarity} gear.")
            else:
                print(f"{self.name}'s gear slots are full. {gear_rarity} gear was discarded.")

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
class Dungeon:
    def __init__(self, tier, config):
        self.tier = tier
        self.config = config
        self.win_probabilities = self.config.dungeon_win_probabilities
        self.loot_drop_chances = self.config.dungeon_loot_drop_chances[tier]
        self.material_drop_chances = self.config.dungeon_material_drop_chances[tier]
        self.pet_drop_chances = self.config.dungeon_pet_drop_chances

    def attempt(self, player):
        """Check if player wins, factoring in gear bonus."""
        base_win_chance = self.win_probabilities[self.tier]
        gear_bonus = player.calculate_gear_bonus()
        total_win_chance = base_win_chance + gear_bonus
        # Cap the total win chance at 95%
        total_win_chance = min(total_win_chance, 0.95)
        result = random.random()
        success = result < total_win_chance
        print(f"{player.name}'s chance to win was {total_win_chance * 100:.2f}% "
              f"(Base: {base_win_chance * 100:.2f}%, Gear Bonus: {gear_bonus * 100:.2f}%)")
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

    def start_day(self):
        """Initialize resources at the start of each day."""
        print(f"\nStarting Day {self.current_day}")
        self.current_round = 1

    def play_round(self):
        """Execute a single round."""
        print(f"\nRound {self.current_round} of Day {self.current_day}")
        
        # Add periodic resources every 6 rounds
        if self.total_turns > 0 and self.total_turns % 6 == 0:
            for player in self.players:
                player.add_periodic_resources()
        
        for player in self.players:
            self.play_turn(player)
            # Record stats after each player's turn
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
            tier = random.choice([1, 2, 3])
            dungeon = Dungeon(tier, self.config)
            player.attempt_dungeon(dungeon)
        elif action == 'contract':
            player.complete_contract()
        # Attempt to purchase lootboxes after the main action
        while (player.skull_tokens >= 5 and player.materials['epic'] >= 5 and player.materials['rare'] >= 5):
            player.purchase_lootbox()

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