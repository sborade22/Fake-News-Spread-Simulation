import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd

# ---------------- TITLE ----------------

st.title("Fake News Spread Simulation")

st.markdown("""
This application demonstrates how fake news spreads in a social
network using graph simulation.
""")

# ---------------- THEORY ----------------

with st.expander("Project Theory"):
    st.write("""
Fake news spreads rapidly in social media networks when users share
information without verifying its authenticity.

In this simulation:
• Nodes represent users  
• Edges represent communication connections  
• Fake news spreads with a probability value  
• Fact checkers stop misinformation
""")

# ---------------- USER INPUT ----------------

st.sidebar.header("Simulation Parameters")

num_users = st.sidebar.number_input("Number of Users", 5, 100, 20)
connection_prob = st.sidebar.number_input("Connection Probability", 0.0, 1.0, 0.3)
spread_prob = st.sidebar.number_input("Fake News Spread Probability", 0.0, 1.0, 0.4)
fact_ratio = st.sidebar.number_input("Fact Checker Ratio", 0.0, 0.5, 0.2)

# ---------------- NETWORK GENERATION ----------------

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

if st.sidebar.button("Generate Network"):

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

pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

color_map = []

for node in G.nodes():

    if node in infected:
        color_map.append("red")

    elif types[node] == "FactChecker":
        color_map.append("green")

    else:
        color_map.append("skyblue")

fig, ax = plt.subplots(figsize=(9,7))

nx.draw(
    G,
    pos,
    node_color=color_map,
    with_labels=True, # cleaner look
    node_size=600,
    font_size=8,
    edge_color="lightgray",
    ax=ax
)

plt.tight_layout()
st.pyplot(fig)

# ---------------- STATISTICS ----------------

st.subheader("Simulation Statistics")

total_users = len(G.nodes())
infected_users = len(infected)
fact_checkers = list(types.values()).count("FactChecker")

data = {
    "Metric": ["Total Users", "Fake News Believers", "Fact Checkers"],
    "Value": [total_users, infected_users, fact_checkers]
}

df = pd.DataFrame(data)
st.table(df)

# ---------------- BAR CHART ----------------

st.subheader("Final Analysis Chart")

labels = ["Total Users", "Fake News", "Fact Checkers"]
values = [total_users, infected_users, fact_checkers]

fig2, ax2 = plt.subplots(figsize=(5,4))
bars = ax2.bar(labels, values)
for bar in bars:
    yval=bar.get_height()
    ax2.text(bar.get_x()+bar.get_width()/2,yval+0.5,int(yval),
             ha='center',va='bottom',fontsize=8)


ax2.set_xlabel("Category",fontsize=9)  
ax2.set_ylabel("Number of Users" , fontsize=9)  
ax2.set_title("Fake News Spread Analysis",fontsize=10)

plt.tight_layout()
st.pyplot(fig2)

# ---------------- INTERPRETATION ----------------

st.subheader("Interpretation")

st.write("""
Red nodes represent users who believe fake news.

Green nodes represent fact checkers who stop misinformation.

Blue nodes represent normal users.

The bar chart clearly shows comparison between total users,
infected users, and fact checkers.
""")
