import random
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from config import Config
from classes import Contract,Lootbox,Player,Dungeon,Game

def plot_stats(player):
    """Plot the stats collected over time using matplotlib and seaborn."""
    sns.set_theme(style="darkgrid")
    
    # Gear Level Over Time
    plt.figure(figsize=(10, 6))
    plt.plot(player.turns, player.gear_levels_over_time, marker='o')
    plt.title(f"{player.name} - Gear Level Over Time")
    plt.xlabel("Turn")
    plt.ylabel("Gear Level (Sum of Gear Tiers)")
    st.pyplot(plt)
    plt.clf()  # Clear the figure

    # Materials Over Time
    plt.figure(figsize=(10, 6))
    for material in ['uncommon', 'rare', 'epic']:
        plt.plot(player.turns, player.materials_over_time[material], label=material.capitalize())
    plt.title(f"{player.name} - Materials Over Time")
    plt.xlabel("Turn")
    plt.ylabel("Quantity")
    plt.legend()
    st.pyplot(plt)
    plt.clf()

    # Dungeon Completions Over Time
    plt.figure(figsize=(10, 6))
    plt.plot(player.turns, player.completions_over_time, marker='o')
    plt.title(f"{player.name} - Total Dungeon Completions Over Time")
    plt.xlabel("Turn")
    plt.ylabel("Total Completions")
    st.pyplot(plt)
    plt.clf()

    # Win Rates Per Tier Over Time
    for tier in [1, 2, 3]:
        plt.figure(figsize=(10, 6))
        plt.plot(player.turns, player.win_rates_over_time[tier], marker='o')
        plt.title(f"{player.name} - Win Rate Over Time for Tier {tier}")
        plt.xlabel("Turn")
        plt.ylabel("Win Rate (%)")
        st.pyplot(plt)
        plt.clf()

def main():
    st.title("Dungeon Game Simulator")
    
    config = Config()
    players = [Player("Alice", config), Player("Bob", config)]
    game = Game(players, config, rounds_per_day=10)
    game.run(days=10)
    
    for player in players:
        st.subheader(f"Stats for {player.name}")
        st.write(f"Gear Equipped: {', '.join(player.gear) if player.gear else 'None'}")
        st.write("Materials:")
        for material, count in player.materials.items():
            st.write(f"  {material.capitalize()}: {count}")
        st.write("Pets Collected: ", ', '.join(player.pets) if player.pets else 'None')

        total_attempts = sum(player.dungeon_attempts.values())
        total_completions = sum(player.dungeon_completions.values())
        overall_completion_rate = (total_completions / total_attempts * 100) if total_attempts > 0 else 0
        st.write(f"Overall Dungeon Completion Rate: {overall_completion_rate:.2f}%")

        plot_stats(player)

if __name__ == "__main__":
    main()