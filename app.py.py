

import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd

st.title("Fake News Spread Simulation")

st.markdown("""
This simulation demonstrates how fake news spreads in a social
network. Each node represents a user and connections represent
information sharing links.
""")

# ---------------- THEORY ----------------

with st.expander("Project Theory"):
    st.write("""
Fake news spreads rapidly on social media platforms when users
share information without verifying authenticity.

In this simulation:
- Nodes represent users
- Edges represent communication links
- Fake news spreads with a probability value
- Fact checkers stop misinformation
""")

# ---------------- USER INPUT ----------------

st.sidebar.header("Simulation Parameters")

num_users = st.sidebar.number_input(
    "Number of Users", 5, 100, 20
)

connection_prob = st.sidebar.number_input(
    "Connection Probability (0-1)", 0.0, 1.0, 0.3
)

spread_prob = st.sidebar.number_input(
    "Fake News Spread Probability (0-1)", 0.0, 1.0, 0.4
)

fact_ratio = st.sidebar.number_input(
    "Fact Checker Ratio", 0.0, 0.5, 0.2
)

# ---------------- NETWORK ----------------

if "graph" not in st.session_state:

    G = nx.erdos_renyi_graph(num_users, connection_prob)

    types = {}

    for node in G.nodes():
        if random.random() < fact_ratio:
            types[node] = "FactChecker"
        else:
            types[node] = "Normal"

    st.session_state.graph = G
    st.session_state.types = types
    st.session_state.infected = set()

G = st.session_state.graph
types = st.session_state.types
infected = st.session_state.infected

# ---------------- BUTTONS ----------------

st.sidebar.header("Simulation Controls")

if st.sidebar.button("Start Fake News"):

    start = random.choice(list(G.nodes()))
    infected.add(start)

if st.sidebar.button("Spread Fake News"):

    new_infected = set()

    for node in infected:

        for neighbor in G.neighbors(node):

            if neighbor not in infected:

                if types[neighbor] != "FactChecker":

                    if random.random() < spread_prob:
                        new_infected.add(neighbor)

    infected.update(new_infected)

if st.sidebar.button("Reset Simulation"):

    st.session_state.infected = set()

# ---------------- GRAPH ----------------

st.subheader("Network Graph")

color_map = []

for node in G.nodes():

    if node in infected:
        color_map.append("red")

    elif types[node] == "FactChecker":
        color_map.append("green")

    else:
        color_map.append("skyblue")

fig, ax = plt.subplots(figsize=(8,6))

pos = nx.spring_layout(G)

nx.draw(
    G,
    pos,
    node_color=color_map,
    with_labels=True,
    node_size=800,
    font_size=9,
    ax=ax
)

# Legend
from matplotlib.lines import Line2D

legend_elements = [
Line2D([0],[0],marker='o',color='w',label='Fake News Believer',
markerfacecolor='red',markersize=10),

Line2D([0],[0],marker='o',color='w',label='Fact Checker',
markerfacecolor='green',markersize=10),

Line2D([0],[0],marker='o',color='w',label='Normal User',
markerfacecolor='skyblue',markersize=10)
]

ax.legend(handles=legend_elements,loc="upper right")

st.pyplot(fig)

# ---------------- STATISTICS ----------------

st.subheader("Simulation Statistics")

total_users = len(G.nodes())
infected_users = len(infected)
fact_checkers = list(types.values()).count("FactChecker")

data = {
    "Metric":[
        "Total Users",
        "Fake News Believers",
        "Fact Checkers"
    ],
    "Value":[
        total_users,
        infected_users,
        fact_checkers
    ]
}

df = pd.DataFrame(data)

st.table(df)

# ---------------- INTERPRETATION ----------------

st.subheader("Interpretation")

st.write("""
Red nodes represent users who believe fake news.

Green nodes represent fact checkers who help stop
misinformation from spreading.

Blue nodes represent normal users in the network.

As the simulation runs, fake news spreads to connected
users depending on the spread probability.
""")
