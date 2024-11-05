import random

import streamlit as st
from config import Config
from classes import Contract,Lootbox,Player,Dungeon,Game,PlayableGame
import pandas as pd
# Global variable for config
config = None

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

    # Dungeon tier choice probabilities
    st.sidebar.subheader("Dungeon Tier Choice Probabilities")
    
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

    # Dungeon tier choice probabilities
    st.sidebar.subheader("Dungeon Tier Choice Probabilities")
    
    # Dungeon tier choice probabilities in a collapsible section
    with st.sidebar.expander("Dungeon Tier Choice Probabilities", expanded=False):
        tier_1_probability = st.slider("Tier 1 Probability", 0, 50, 10)
        tier_2_probability = st.slider("Tier 2 Probability", 0, 50, 5)
        tier_3_probability = st.slider("Tier 3 Probability", 0, 50, 1)

        # Gear modifiers for dungeon tier probabilities
        gear_modifier_tier_1 = st.slider("Gear Modifier for Tier 1", 0.0, 2.0, 0.0)
        gear_modifier_tier_2 = st.slider("Gear Modifier for Tier 2", 0.0, 2.0, 0.5)
        gear_modifier_tier_3 = st.slider("Gear Modifier for Tier 3", 0.0, 2.0, 1.0)

        # Update the config with the new values
        config.dungeon_choice_probabilities['tier_1']['gear_modifier'] = gear_modifier_tier_1
        config.dungeon_choice_probabilities['tier_2']['gear_modifier'] = gear_modifier_tier_2
        config.dungeon_choice_probabilities['tier_3']['gear_modifier'] = gear_modifier_tier_3

    # Return the user configuration
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
        'dungeon_choice': {
            'tier_1': {'threshold': None, 'probability': tier_1_probability, 'gear_modifier': gear_modifier_tier_1},
            'tier_2': {'threshold': None, 'probability': tier_2_probability, 'gear_modifier': gear_modifier_tier_2},
            'tier_3': {'threshold': None, 'probability': tier_3_probability, 'gear_modifier': gear_modifier_tier_3}
        },
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
        - Success chance = Base Rate + Gear Bonus 
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
    - Dungeon tier selection is based on probability weighted by gear level. This can be configured in the sidebar.
    """)

def player_input():
    """Function to handle player configuration settings"""
    st.header("Player Configuration")
    
    players = []
    num_players = st.number_input("Number of Players", min_value=1, max_value=5, value=2)
    
    # Define archetypes
    archetypes = {
        "No-Life": (100, 1),
        "Hardcore": (70, 1),
        "Casual": (30, 2),
        "Ultra Casual": (20, 5)
    }
    
    for i in range(num_players):
        with st.expander(f"Player {i+1} Settings", expanded=True):
            name = st.text_input(f"Player {i+1} Name", 
                               value=f"Player {i+1}",
                               key=f"name_{i}")
            
            # Archetype selection
            archetype = st.selectbox(
                "Select Archetype", 
                options=list(archetypes.keys()), 
                index=0, 
                key=f"archetype_{i}"
            )
            activity_level, play_frequency = archetypes[archetype]
            
            # Activity level (what % of possible rounds they play)
            activity_level = st.slider(
                "Activity Level (% of daily rounds played)", 
                min_value=0, 
                max_value=100, 
                value=activity_level,  # Set default based on archetype
                help="Percentage of available daily rounds the player will participate in",
                key=f"activity_{i}"  # Add unique key
            )
            
            # Play frequency (how often they play)
            play_frequency = st.slider(
                "Play Frequency (days between sessions)", 
                min_value=1, 
                max_value=7, 
                value=play_frequency,  # Set default based on archetype
                help="1 = plays every day, 2 = plays every other day, etc.",
                key=f"frequency_{i}"  # Add unique key
            )
            
            players.append({
                'name': name,
                'activity_level': activity_level / 100.0,  # Convert to decimal
                'play_frequency': play_frequency
            })
    
    return players

def show_player_stats(game):
    # Initialize session state for game data if not exists
    if 'game_data' not in st.session_state:
        st.session_state.game_data = game
    
    # Create a dropdown to select player
    player_names = [player.name for player in st.session_state.game_data.players]
    selected_player_name = st.selectbox('Select Player', player_names, key='player_selector')
    
    # Find the selected player object
    selected_player = next((p for p in st.session_state.game_data.players if p.name == selected_player_name), None)
    
    if selected_player:
        # Create three columns for different stat categories
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Gear")
            gear_df = pd.DataFrame(
                [(gear, selected_player.config.gear_tier_values[gear]) 
                 for gear in selected_player.gear],
                columns=['Item', 'Tier']
            )
            st.dataframe(gear_df)
        
        with col2:
            st.subheader("Materials")
            materials_df = pd.DataFrame(
                selected_player.materials.items(),
                columns=['Material', 'Quantity']
            )
            st.dataframe(materials_df)
        
        with col3:
            st.subheader("Pets")
            pets_df = pd.DataFrame(
                [(pet, 1) for pet in selected_player.pets],  # Assuming level 1 for all pets
                columns=['Pet', 'Level']
            )
            st.dataframe(pets_df)

def main():
    global config
    config = Config()

    st.title("Game Loop Simulator")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Rules", "Player Setup", "Simulation", "Action Log", "Play Game"])
    
    # Initialize players in session state if not exists
    if 'players_config' not in st.session_state:
        st.session_state.players_config = []
    
    with tab2:
        st.session_state.players_config = player_input()
    
    with tab3:
        # Simulation tab
        user_config = user_input()
        
        # Create players with their individual settings
        game_players = []
        for p_config in st.session_state.players_config:
            player = Player(
                p_config['name'], 
                config,
                activity_level=p_config['activity_level'],
                play_frequency=p_config['play_frequency']
            )
            game_players.append(player)

        game = Game(game_players, config, rounds_per_day=user_config['simulation_settings']['rounds_per_day'])

        if st.button("Run Simulation"):
            game.run(days=user_config['simulation_settings']['simulation_days'])
            game.display_stats()
            game.plot_stats()
            # Store game state after simulation
            st.session_state.game_data = game
        
        # Show player stats if we have game data (separate from simulation run)
        if 'game_data' in st.session_state:
            show_player_stats(st.session_state.game_data)
    
    with tab1:
        show_rules()
    
    with tab4:
        if 'game_data' in st.session_state:
            st.header("Action Log")
            # Add a search/filter box
            search_term = st.text_input("Filter log messages", "")
            
            # Filter messages based on search term
            filtered_logs = st.session_state.game_data.action_log
            if search_term:
                filtered_logs = [msg for msg in filtered_logs if search_term.lower() in msg.lower()]
            
            # Display logs in a scrollable container
            log_container = st.container()
            with log_container:
                for message in filtered_logs:
                    st.text(message)
        else:
            st.info("Run a simulation to see the action log")
            

    with tab5:
        if not st.session_state.players_config:
            st.warning("Please set up players in the Player Setup tab first!")
        else:
            play_game(st.session_state.players_config)

def play_game(players_config):
    st.header("Play Game")
    
    # Initialize game state in session if not exists
    if 'play_state' not in st.session_state:
        st.session_state.play_state = {
            'initialized': False,
            'game': None,
            'players': [],
            'current_round': 1,
            'current_day': 1,
            'players_acted': set()
        }
    
    # Ensure players_acted exists
    if 'players_acted' not in st.session_state.play_state:
        st.session_state.play_state['players_acted'] = set()
    
    # Game initialization
    if not st.session_state.play_state['initialized']:
        # Create all players from config
        players = []
        for player_config in players_config:
            player = Player(
                player_config['name'], 
                config,
                activity_level=player_config['activity_level'],
                play_frequency=player_config['play_frequency']
            )
            players.append(player)
        
        if st.button("Start Game"):
            game = PlayableGame(players, config)
            st.session_state.play_state = {
                'initialized': True,
                'game': game,
                'players': players,
                'current_round': 1,
                'current_day': 1,
                'players_acted': set()
            }
            st.rerun()
    
    # Main game loop
    else:
        game = st.session_state.play_state['game']
        game.current_round = st.session_state.play_state.get('current_round', 1)
        game.current_day = st.session_state.play_state.get('current_day', 1)
        
        # Display round info
        game.display_round_info()
        
        # Create columns for each player
        cols = st.columns(len(game.players))
        
        for idx, player in enumerate(game.players):
            with cols[idx]:
                st.subheader(f"Player: {player.name}")
                
                # Check if player should play today
                plays_today = player.should_play_today(game.current_day)
                # Check if player should play this round
                plays_round = player.should_play_round()
                
                if not plays_today:
                    st.info(f"Not playing on day {game.current_day}")
                    st.session_state.play_state['players_acted'].add(player.name)
                elif not plays_round:
                    st.info("Skipping this round")
                    st.session_state.play_state['players_acted'].add(player.name)
                elif player.name in st.session_state.play_state['players_acted']:
                    st.info("Waiting for other players")
                else:
                    # Display player status and actions
                    game.display_player_status(player)
                    game.display_player_actions(player)
        
        # Check if all players have acted
        all_players_acted = len(st.session_state.play_state['players_acted']) == len(game.players)
        
        if all_players_acted:
            # Advance to next round
            game.current_round += 1
            if game.current_round > 10:  # Assuming 10 rounds per day
                game.current_day += 1
                game.current_round = 1
            
            # Reset players_acted for new round
            st.session_state.play_state['players_acted'] = set()
            
            # Add periodic resources if needed
            total_rounds = ((game.current_day - 1) * 10 + game.current_round)
            if total_rounds % 6 == 0:
                for player in game.players:
                    player.add_periodic_resources(game)
            
            # Update session state
            st.session_state.play_state['current_round'] = game.current_round
            st.session_state.play_state['current_day'] = game.current_day
            st.rerun()
        
        # Reset game button
        if st.button("Reset Game"):
            st.session_state.play_state['initialized'] = False
            st.rerun()

if __name__ == "__main__":
    main()