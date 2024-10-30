import random

import streamlit as st
from config import Config
from classes import Contract,Lootbox,Player,Dungeon,Game

# Function to create a Streamlit sidebar for user input
def normalize_probabilities(probabilities):
    """Normalize probabilities to sum to 1.0"""
    total = sum(probabilities.values())
    if total == 0:
        # If all values are 0, set equal probabilities
        num_items = len(probabilities)
        return {k: 1.0/num_items for k in probabilities}
    return {k: v/total for k, v in probabilities.items()}

def user_input():
    st.sidebar.header("Game Configuration")

    # Add simulation settings
    with st.sidebar.expander("Simulation Settings", expanded=False):
        rounds_per_day = st.slider("Rounds Per Day", 1, 48, 10)
        simulation_days = st.slider("Number of Days", 1, 180, 10)

    # Input fields for Contract drop chances
    with st.sidebar.expander("Contract Drop Chances", expanded=False):
        contract_probs = {
            'epic': st.slider("Contract: Epic Material Drop Chance", 0.0, 1.0, 0.11),
            'rare': st.slider("Contract: Rare Material Drop Chance", 0.0, 1.0, 0.89)
        }
        contract_material_drop_chances = normalize_probabilities(contract_probs)
        st.text("Normalized probabilities (sum = 1.0):")
        for k, v in contract_material_drop_chances.items():
            st.text(f"{k}: {v:.3f}")

    # Input fields for Lootbox drop chances
    with st.sidebar.expander("Lootbox Drop Chances", expanded=False):
        lootbox_probs = {
            'legendary': st.slider("Lootbox: Legendary Drop Chance", 0.0, 1.0, 0.02),
            'epic': st.slider("Lootbox: Epic Drop Chance", 0.0, 1.0, 0.09),
            'rare': st.slider("Lootbox: Rare Drop Chance", 0.0, 1.0, 0.15),
            'uncommon': st.slider("Lootbox: Uncommon Drop Chance", 0.0, 1.0, 0.74),
            'common': st.slider("Lootbox: Common Drop Chance", 0.0, 1.0, 0.0)
        }
        lootbox_loot_drop_chances = normalize_probabilities(lootbox_probs)
        st.text("Normalized probabilities (sum = 1.0):")
        for k, v in lootbox_loot_drop_chances.items():
            st.text(f"{k}: {v:.3f}")

    # Base completion rates per tier
    with st.sidebar.expander("Base Completion Rates", expanded=False):
        base_completion_rates = {
            1: st.slider("Tier 1 Base Completion Rate", 0.0, 1.0, 0.8),
            2: st.slider("Tier 2 Base Completion Rate", 0.0, 1.0, 0.6),
            3: st.slider("Tier 3 Base Completion Rate", 0.0, 1.0, 0.3)
        }
        
    # Gear bonus values in separate dropdown
    with st.sidebar.expander("Gear Bonus Values", expanded=False):
        gear_bonus_values = {
            'legendary': st.slider("Legendary Gear Bonus", 0.0, 0.25, 0.05),
            'epic': st.slider("Epic Gear Bonus", 0.0, 0.20, 0.03),
            'rare': st.slider("Rare Gear Bonus", 0.0, 0.15, 0.02),
            'uncommon': st.slider("Uncommon Gear Bonus", 0.0, 0.10, 0.01)
        }

    # Input fields for Dungeon drop chances
    st.sidebar.subheader("Dungeon Drop Chances")
    
    # Dungeon Material Drop Chances per Tier
    dungeon_material_drop_chances = {}
    for tier in [1, 2, 3]:
        with st.sidebar.expander(f"Tier {tier} Material Drop Chances", expanded=False):
            tier_probs = {
                'legendary': st.slider(f"T{tier} Material: Legendary", 0.0, 1.0, 0.02),
                'epic': st.slider(f"T{tier} Material: Epic", 0.0, 1.0, 0.09),
                'rare': st.slider(f"T{tier} Material: Rare", 0.0, 1.0, 0.15),
                'uncommon': st.slider(f"T{tier} Material: Uncommon", 0.0, 1.0, 0.74),
                'common': st.slider(f"T{tier} Material: Common", 0.0, 1.0, 0.0)
            }
            dungeon_material_drop_chances[tier] = normalize_probabilities(tier_probs)
            st.text("Normalized probabilities (sum = 1.0):")
            for k, v in dungeon_material_drop_chances[tier].items():
                st.text(f"{k}: {v:.3f}")

    # Dungeon Loot Drop Chances per Tier
    dungeon_loot_drop_chances = {}
    for tier in [1, 2, 3]:
        with st.sidebar.expander(f"Tier {tier} Loot Drop Chances", expanded=False):
            tier_probs = {
                'legendary': st.slider(f"T{tier} Loot: Legendary", 0.0, 1.0, 0.02),
                'epic': st.slider(f"T{tier} Loot: Epic", 0.0, 1.0, 0.09),
                'rare': st.slider(f"T{tier} Loot: Rare", 0.0, 1.0, 0.15),
                'uncommon': st.slider(f"T{tier} Loot: Uncommon", 0.0, 1.0, 0.74),
                'common': st.slider(f"T{tier} Loot: Common", 0.0, 1.0, 0.0)
            }
            dungeon_loot_drop_chances[tier] = normalize_probabilities(tier_probs)
            st.text("Normalized probabilities (sum = 1.0):")
            for k, v in dungeon_loot_drop_chances[tier].items():
                st.text(f"{k}: {v:.3f}")

    
    return {
        'simulation_settings': {
            'rounds_per_day': rounds_per_day,
            'simulation_days': simulation_days
        },
        'contract_material_drop_chances': contract_material_drop_chances,
        'lootbox_loot_drop_chances': lootbox_loot_drop_chances,
        'dungeon_material_drop_chances': dungeon_material_drop_chances,
        'dungeon_loot_drop_chances': dungeon_loot_drop_chances,
        'gear_bonus_values': gear_bonus_values,
        'dungeon_win_probabilities': base_completion_rates
    }

def show_rules():
    st.header("Game Rules & Mechanics")

    st.subheader("Basic Resources")
    st.write("""
    - Players start with 3 Yoku and 6 Pioneer Points
    - Every 6 rounds, players receive:
        - 1 Yoku
        - 2 Pioneer Points
    """)

    st.subheader("Activities")
    with st.expander("Contracts"):
        st.write("""
        - Costs 3 Pioneer Points
        - Rewards:
            - 1 Yoku
            - 1 Material (Epic or Rare)
        """)

    with st.expander("Dungeons"):
        st.write("""
        - Costs 1 Yoku to attempt
        - Success rewards:
            - 1 Pioneer Point
            - 1 Skull Token
            - 1 Piece of Gear
            - 1 Material
            - Chance for a Pet
        - Success chance = Base Rate + Gear Bonus (capped at 95%)
        - Three difficulty tiers with different drop rates and success chances
        """)

    with st.expander("Lootboxes"):
        st.write("""
        - Costs:
            - 5 Skull Tokens
            - 5 Epic Materials
            - 5 Rare Materials
        - Rewards:
            - 1 Piece of Gear
            - Chance for a Pet
        """)

    st.subheader("Gear System")
    st.write("""
    - Maximum 5 gear pieces equipped
    - When receiving new gear:
        - If inventory not full: automatically equip
        - If full: replaces lowest tier gear if new gear is better
    - Each gear piece provides a bonus to dungeon success rate
    - Gear tiers (from lowest to highest):
        1. Uncommon
        2. Rare
        3. Epic
        4. Legendary
    """)

    st.subheader("Player Behavior")
    st.write("""
    - Players will attempt dungeons if they have Yoku
    - Players will complete contracts if they have enough Pioneer Points
    - Players will purchase lootboxes whenever they have enough resources
    - Dungeon tier selection is random
    """)

def player_input():
    """Function to handle player configuration settings"""
    st.header("Player Configuration")
    
    players = []
    num_players = st.number_input("Number of Players", min_value=1, max_value=5, value=2)
    
    for i in range(num_players):
        with st.expander(f"Player {i+1} Settings", expanded=True):
            name = st.text_input(f"Player {i+1} Name", 
                               value=f"Player {i+1}",
                               key=f"name_{i}")
            
            # Activity level (what % of possible rounds they play)
            activity_level = st.slider(
                "Activity Level (% of daily rounds played)", 
                min_value=0, 
                max_value=100, 
                value=100, 
                help="Percentage of available daily rounds the player will participate in",
                key=f"activity_{i}"  # Add unique key
            )
            
            # Play frequency (how often they play)
            play_frequency = st.slider(
                "Play Frequency (days between sessions)", 
                min_value=1, 
                max_value=7, 
                value=1, 
                help="1 = plays every day, 2 = plays every other day, etc.",
                key=f"frequency_{i}"  # Add unique key
            )
            
            players.append({
                'name': name,
                'activity_level': activity_level / 100.0,  # Convert to decimal
                'play_frequency': play_frequency
            })
    
    return players

def main():
    st.title("Game Loop Simulator")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Player Setup", "Simulation", "Rules"])
    
    with tab1:
        players_config = player_input()
    
    with tab2:
        # Your existing simulation code
        user_config = user_input()
        
        config = Config()
        config.contract_material_drop_chances = user_config['contract_material_drop_chances']
        config.lootbox_loot_drop_chances = user_config['lootbox_loot_drop_chances']
        config.dungeon_material_drop_chances = user_config['dungeon_material_drop_chances']
        config.dungeon_loot_drop_chances = user_config['dungeon_loot_drop_chances']
        config.gear_bonus_values = user_config['gear_bonus_values']
        config.dungeon_win_probabilities = user_config['dungeon_win_probabilities']

        # Create players with their individual settings
        game_players = []
        for p_config in players_config:
            player = Player(
                p_config['name'], 
                config,
                activity_level=p_config['activity_level'],
                play_frequency=p_config['play_frequency']
            )
            game_players.append(player)

        game = Game(
            game_players, 
            config, 
            rounds_per_day=user_config['simulation_settings']['rounds_per_day']
        )

        if st.button("Run Simulation"):
            game.run(days=user_config['simulation_settings']['simulation_days'])
            game.display_stats()
            game.plot_stats()
    
    with tab3:
        show_rules()

if __name__ == "__main__":
    main()