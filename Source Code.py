import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
% matplotlib
notebook


def players_df():
    players = pd.read_csv("atp_players.csv")
    players_col_keep = ["full_name", "flag_code"]
    players = players.loc[:, players_col_keep]

    players = players[players["flag_code"] == "USA"]

    return players


def matches_df():
    matches = pd.read_csv("atp_matches_combined.csv")
    matches_col_keep = ["match_date", "round", "winner", "wrank"]
    matches = matches.loc[:, matches_col_keep]

    matches["winner"] = matches["winner"].str.replace(".", "")
    matches = matches[matches["round"] == "The Final"]
    matches["match_date"] = pd.to_datetime(matches["match_date"])
    matches["Year"] = matches["match_date"].dt.year

    matches_US = pd.merge(matches, players, left_on="winner", right_on="full_name")

    return matches, matches_US


def years():
    years = []

    for i in range(2001, 2020):
        years.append("'" + str(i)[2:])
    return years


players = players_df()
matches, matches_US = matches_df()

best_player = matches["winner"].value_counts().index[0]
best_player_wins = int(matches["winner"].value_counts().values[0])
matches = matches[matches["winner"] == best_player]
wins_per_year = matches.groupby("Year").size()
matches = matches.drop_duplicates(subset="Year").loc[:, ["Year", "wrank"]]

best_US_player = matches_US["winner"].value_counts().index[0]
best_US_player_wins = int(matches_US["winner"].value_counts().values[0])
matches_US = matches_US[matches_US["winner"] == best_US_player]
US_wins_per_year = matches_US.groupby("Year").size()
matches_US = matches_US.drop_duplicates(subset="Year").loc[:, ["Year", "wrank"]]

plt.figure(figsize=(11, 7))
tennis = gridspec.GridSpec(4, 4)
plt.suptitle("World's Best Tennis Player vs. USA's Best Tennis Player \n(According to ATP Tournament Wins between"
             + " 2001 and 2019)\n", size=10, weight="bold", ha="center")

side_bar = plt.subplot(tennis[1:, 3])
center_bar = plt.subplot(tennis[1:, 0:3])
top_line = plt.subplot(tennis[0, :3])

top_line.set_title("World Rank", size="medium")
top_line.set_ylabel("Rank")
side_bar.set_title("ATP Tournament Wins", size="medium")
center_bar.set_title("ATP Tournament Wins Over Time", size="medium")
center_bar.set_xlabel("Year", weight="bold")
center_bar.set_ylabel("No. of Wins")

center_bar.spines['top'].set_visible(False)
center_bar.spines["right"].set_visible(False)

side_bar.spines['top'].set_visible(False)
side_bar.spines["left"].set_visible(False)
side_bar.spines["right"].set_visible(False)
side_bar.tick_params(axis="both", bottom=False, labelbottom=False, left=False, labelleft=False)

top_line.spines['top'].set_visible(False)
top_line.spines["right"].set_visible(False)
top_line.spines["bottom"].set_visible(False)
top_line.tick_params(axis="x", bottom=False, labelbottom=False)

years = years()
c = center_bar.bar(US_wins_per_year.index, US_wins_per_year.values, width=0.25, color="black")
c += center_bar.bar(wins_per_year.index + 0.25, wins_per_year.values, width=0.25, color="grey")
center_bar.set_xticks(range(2001, 2020))
center_bar.set_xticklabels(years, weight="bold")
plt.setp(center_bar.xaxis.get_majorticklabels(), rotation=45)

s = side_bar.bar(1, best_US_player_wins, color="black")
s += side_bar.bar(2, best_player_wins, color="grey")
for bar in s:
    side_bar.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 10,
                  (int(bar.get_height())), ha="center", color="w", fontsize=10, weight="bold")

top_line.set_ylim(99, 1)
top_line.set_yticks([99, 75, 50, 25, 1])
top_line.plot(matches_US["Year"], matches_US["wrank"], "-", color="black")
top_line.plot(matches["Year"], matches["wrank"], "-", color="grey")

plt.legend(s, labels=(best_US_player + " (US)", best_player + " (World)"), loc=1, frameon=False,
           bbox_to_anchor=(1.35, 1.2))

plt.savefig("Ass4.jpg")
