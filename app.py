import random

import streamlit as st
from config import Config
from classes import Contract,Lootbox,Player,Dungeon,Game

# Function to create a Streamlit sidebar for user input
def normalize_probabilities(probabilities):
    """Normalize probabilities to sum to 1.0"""
    total = sum(probabilities.values())
    if total == 0:
        return {k: 0.0 for k in probabilities}
    return {k: v/total for k, v in probabilities.items()}

def user_input():
    st.sidebar.header("Game Configuration")

    # Add simulation settings
    with st.sidebar.expander("Simulation Settings", expanded=False):
        rounds_per_day = st.slider("Rounds Per Day", 1, 20, 10)
        simulation_days = st.slider("Number of Days", 1, 30, 10)

    # Input fields for Contract drop chances
    with st.sidebar.expander("Contract Drop Chances", expanded=False):
        contract_probs = {
            'epic': st.slider("Contract: Epic Material Drop Chance", 0.0, 1.0, 0.11),
            'rare': st.slider("Contract: Rare Material Drop Chance", 0.0, 1.0, 0.89)
        }
        contract_material_drop_chances = normalize_probabilities(contract_probs)
        st.text(f"Normalized probabilities (sum = 1.0):")
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
        st.text(f"Normalized probabilities (sum = 1.0):")
        for k, v in lootbox_loot_drop_chances.items():
            st.text(f"{k}: {v:.3f}")

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
            st.text(f"Normalized probabilities (sum = 1.0):")
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
            st.text(f"Normalized probabilities (sum = 1.0):")
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
        'dungeon_loot_drop_chances': dungeon_loot_drop_chances
    }

def main():
    st.title("Dungeon Game Simulator")

    # Get user input
    user_config = user_input()
    
    # Create Config object with user-defined parameters
    config = Config()
    config.contract_material_drop_chances = user_config['contract_material_drop_chances']
    config.lootbox_loot_drop_chances = user_config['lootbox_loot_drop_chances']
    config.dungeon_material_drop_chances = user_config['dungeon_material_drop_chances']
    config.dungeon_loot_drop_chances = user_config['dungeon_loot_drop_chances']

    players = [Player("Alice", config), Player("Bob", config)]
    game = Game(players, config, rounds_per_day=user_config['simulation_settings']['rounds_per_day'])

    if st.button("Run Simulation"):
        game.run(days=user_config['simulation_settings']['simulation_days'])
        game.display_stats()
        game.plot_stats()

if __name__ == "__main__":
    main()