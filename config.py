class Config:
    """Configuration class to hold all adjustable parameters."""
    def __init__(self):
        # Material drop chances for Contracts
        self.contract_material_drop_chances = {'epic': 0.11, 'rare': 0.89}

        # Lootbox loot drop chances (should sum to 1.0)
        self.lootbox_loot_drop_chances = {
            'legendary': 0.02,
            'epic': 0.09,
            'rare': 0.15,
            'uncommon': 0.74  # Adjusted to sum up to 1.0
        }
        # Lootbox pet drop chance
        self.lootbox_pet_drop_chance = 0.01

        # Gear bonus values (now configurable)
        self.gear_bonus_values = {
            'legendary': 0.05,  
            'epic': 0.03,       
            'rare': 0.02,       
            'uncommon': 0.01    
        }

        # Dungeon win probabilities per tier (now configurable)
        self.dungeon_win_probabilities = {
            1: 0.8,  # Tier 1
            2: 0.6,  # Tier 2
            3: 0.3   # Tier 3
        }
        # Dungeon loot drop chances per tier (should sum to 1.0 per tier)
        self.dungeon_loot_drop_chances = {
            1: {'legendary': 0.02, 'epic': 0.09, 'rare': 0.15, 'uncommon': 0.74, 'common': 0.0},
            2: {'legendary': 0.02, 'epic': 0.09, 'rare': 0.15, 'uncommon': 0.74, 'common': 0.0},
            3: {'legendary': 0.02, 'epic': 0.09, 'rare': 0.15, 'uncommon': 0.74, 'common': 0.0}
        }
        # Dungeon material drop chances per tier
        self.dungeon_material_drop_chances = {
            1: {'legendary': 0.02, 'epic': 0.09, 'rare': 0.15, 'uncommon': 0.74, 'common': 0.0},
            2: {'legendary': 0.02, 'epic': 0.09, 'rare': 0.15, 'uncommon': 0.74, 'common': 0.0},
            3: {'legendary': 0.02, 'epic': 0.09, 'rare': 0.15, 'uncommon': 0.74, 'common': 0.0}
        }
        # Dungeon pet drop chances per tier
        self.dungeon_pet_drop_chances = {
            1: 0.001,
            2: 0.001,
            3: 0.001
        }

        # Gear tier values for comparison
        self.gear_tier_values = {
            'uncommon': 1,
            'rare': 2,
            'epic': 3,
            'legendary': 4
        }

        # Dungeon tier choice probabilities based on gear level thresholds
        self.dungeon_choice_probabilities = {
            'tier_1': {
    
                'probability': 10  # Base probability of choosing Tier 1
            },
            'tier_2': {
  
                'probability': 5  # Base probability of choosing Tier 2
            },
            'tier_3': {
     
                'probability': 1  # Base probability of choosing Tier 3
            }
        }

    def update_dungeon_choice_probabilities(self, tier, threshold, probability):
        """Update the dungeon choice probabilities for a specific tier."""
        if tier in self.dungeon_choice_probabilities:
            self.dungeon_choice_probabilities[tier]['probability'] = probability