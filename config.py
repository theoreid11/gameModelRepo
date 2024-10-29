
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

        # Gear bonus values
        self.gear_bonus_values = {
            'legendary': 0.05,  
            'epic': 0.03,       
            'rare': 0.02,       
            'uncommon': 0.01    
        }
        self.max_gear_bonus = 0.20  # Max total gear bonus (e.g., 20%)

        # Dungeon win probabilities per tier
        self.dungeon_win_probabilities = {
            1: 0.8,  # Tier 1
            2: 0.6,  # Tier 2
            3: 0.3   # Tier 3
        }
        # Dungeon loot drop chances per tier (should sum to 1.0 per tier)
        self.dungeon_loot_drop_chances = {
            1: {'epic': 0.0, 'rare': 0.26, 'uncommon': 0.74},
            2: {'epic': 0.2, 'rare': 0.5, 'uncommon': 0.3},
            3: {'epic': 0.4, 'rare': 0.5, 'uncommon': 0.1}
        }
        # Dungeon material drop chances per tier
        self.dungeon_material_drop_chances = {
            1: {'epic': 0.1, 'rare': 0.9},
            2: {'epic': 0.2, 'rare': 0.8},
            3: {'epic': 0.4, 'rare': 0.6}
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