<h1> Dungeon Simulation Game </h1>

This repository contains a Streamlit-based web application designed to simulate dungeon exploration, loot collection, and player progression. Players engage in activities such as completing contracts, exploring dungeons of varying difficulties, collecting gear, pets, materials, and opening lootboxes.

<h3>Features</h3>

**Interactive Simulation**: Adjust game parameters and player settings dynamically via a user-friendly Streamlit interface.

**Configurable Drop Rates**: Customize probabilities for loot and materials across multiple dungeon tiers and lootboxes.

**Gear and Pets System**: Equip players with gear and pets to boost dungeon success rates.

**Player Customization**: Define activity levels and play frequencies to simulate various player types from casual to hardcore.

**Detailed Analytics**: Visualize player statistics, gear collection, and action logs for detailed insights.

<h2> Application Structure </h2>

**app.py**: Core Streamlit application with user interface and simulation logic.

**config.py**: Configuration parameters for adjusting gameplay dynamics.

**classes.py**: Contains class definitions for Contracts, Lootboxes, Players, Dungeons, and Game logic.

<h2>Getting Started </h2>

<h3> Installation </h3>

Clone this repository and install the required dependencies:
<code>
git clone [your-repo-url]
cd [your-repo-folder]
pip install -r requirements.txt
</code>

<h3> Running the App </h3>

Execute the Streamlit app locally:

streamlit run app.py

<h2> Features </h2>

<h3> Simulation Settings </h3>

Configure simulation duration and frequency of daily rounds.

Adjust drop rates and probabilities directly via an interactive sidebar.

<h3> Player Configuration </h3>

Customize multiple players with distinct profiles, activity levels, and play styles.

<h3> Gameplay Elements </h3>

Contracts: Collect materials through contracts.

Dungeons: Three tiers of dungeons with varying difficulty and loot drops.

Lootboxes: Obtain rare gear and pets through lootbox rewards.

<h2> Project Structure </h2>
<code>
project
├── app.py
├── config.py
├── classes.py
├── requirements.txt
└── README.md
</code>

<h2> Contributing </h2>

Feel free to fork this project and submit pull requests or open issues to propose improvements.
