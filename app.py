import random

import streamlit as st
from config import Config
from classes import Contract,Lootbox,Player,Dungeon,Game

# Function to create a Streamlit sidebar for user input
def user_input():
    st.sidebar.header("Game Configuration")

    # Add simulation settings
    st.sidebar.subheader("Simulation Settings")
    rounds_per_day = st.sidebar.slider("Rounds Per Day", 1, 20, 10)
    simulation_days = st.sidebar.slider("Number of Days", 1, 30, 10)

    # Input fields for the parameters in Config
    st.sidebar.subheader("Drop Chances")
    contract_material_drop_epic = st.sidebar.slider("Epic Material Drop Chance", 0.0, 1.0, 0.11)
    contract_material_drop_rare = st.sidebar.slider("Rare Material Drop Chance", 0.0, 1.0, 0.89)

    lootbox_loot_drop_legendary = st.sidebar.slider("Legendary Loot Drop Chance", 0.0, 1.0, 0.02)
    lootbox_loot_drop_epic = st.sidebar.slider("Epic Loot Drop Chance", 0.0, 1.0, 0.09)
    lootbox_loot_drop_rare = st.sidebar.slider("Rare Loot Drop Chance", 0.0, 1.0, 0.15)
    lootbox_loot_drop_uncommon = st.sidebar.slider("Uncommon Loot Drop Chance", 0.0, 1.0, 0.74)

    return {
        'simulation_settings': {
            'rounds_per_day': rounds_per_day,
            'simulation_days': simulation_days
        },
        'contract_material_drop_chances': {
            'epic': contract_material_drop_epic,
            'rare': contract_material_drop_rare
        },
        'lootbox_loot_drop_chances': {
            'legendary': lootbox_loot_drop_legendary,
            'epic': lootbox_loot_drop_epic,
            'rare': lootbox_loot_drop_rare,
            'uncommon': lootbox_loot_drop_uncommon
        }
    }

def main():
    st.title("Dungeon Game Simulator")

    # Get user input
    user_config = user_input()
    
    # Create Config object with user-defined parameters
    config = Config()
    config.contract_material_drop_chances = user_config['contract_material_drop_chances']

    config.lootbox_loot_drop_chances = user_config['lootbox_loot_drop_chances']

    players = [Player("Alice", config), Player("Bob", config)]
    game = Game(players, config, rounds_per_day=user_config['simulation_settings']['rounds_per_day'])

    if st.button("Run Simulation"):
        game.run(days=user_config['simulation_settings']['simulation_days'])
        game.display_stats()
        game.plot_stats()

if __name__ == "__main__":
    main()