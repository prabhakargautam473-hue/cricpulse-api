import pandas as pd
import numpy as np
from collections import OrderedDict


#ipl_matches = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRy2DUdUbaKx_Co9F0FSnIlyS-8kp4aKv_I0-qzNeghiZHAI_hw94gKG22XTxNJHMFnFVKsO4xWOdIs/pub?gid=1655759976&single=true&output=csv"
matches=pd.read_csv("ipl_matches.csv")
#ipl_ball = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRu6cb6Pj8C9elJc5ubswjVTObommsITlNsFy5X0EiBY7S-lsHEUqx3g_M16r50Ytjc0XQCdGDyzE_Y/pub?output=csv"
ipl=pd.read_csv("ipl_ball.csv")

def teamsapi():
    teams=list(set(list(matches["Team1"]) + list(matches["Team2"])))
    team_dict={
        "teams":teams,
    }
    return team_dict
def playersapi():
    players=list(set(list(matches["Team1Players"])+list(matches["Team2Players"])))
    players_dict={
        "players":players
    }
    return players_dict
def teamVteamapi(team,team2):
    temp_df = matches[(matches['Team1'] == team) & (matches['Team2'] == team2) | (matches['Team1'] == team2) & ( matches['Team2'] == team)]
    total_matches = temp_df.shape[0]
    if total_matches==0:
        return {
            "total_matches":"No matches played yet",
            "matches_won_by_team1":"No matches played yet",
            "matches_won_by_team2":"No matches played yet",
        }
    matches_won_by_team1 = temp_df["WinningTeam"].value_counts().get(team,0)
    matches_won_by_team2 = temp_df["WinningTeam"].value_counts().get(team2,0)
    draws = total_matches - (matches_won_by_team1 + matches_won_by_team2)
    toss_won_team1=temp_df["TossWinner"].value_counts().get(team,0)
    toss_won_team2=temp_df["TossWinner"].value_counts().get(team2,0)
    pom_player=temp_df["Player_of_Match"].value_counts().to_dict()
    sorted_items=sorted(pom_player.items(),key=lambda x:x[1],reverse=True)
    ordered_pom=OrderedDict(sorted_items)
    response={
        "total_matches_played":str(total_matches),
        "matches_won_by_team1":str(matches_won_by_team1),
        "matches_won_by_team2":str(matches_won_by_team2),
        "draws":str(draws),
        "toss won by team1":str(toss_won_team1),
        "toss won by team2":str(toss_won_team2),
        "list of player of match between theses two teams":ordered_pom
    }
    return response
def teamrecordapi(team):
    df = matches[(matches["Team1"] == team) | (matches["Team2"] == team)]
    total_matches = df.shape[0]
    won = df[df["WinningTeam"] == team].shape[0]
    no_result = df[df['WinningTeam'].isnull()].shape[0]
    loss = won - no_result
    final_winner = df[(df["MatchNumber"] == 'Final') & (df["WinningTeam"] == team)].shape[0]
    response={
        "total_matches_played":str(total_matches),
        "matches_won_by_team":str(won),
        "matches_loss_by_team":str(loss),
        "draws":str(no_result),
        "final won by team":str(final_winner),
    }
    return response
def teamagainstrecordapi(team):
    df = matches[(matches["Team1"] == team) | (
                matches["Team2"] == team)]
    TEAMS = matches["Team1"].unique()


    against ={}
    for team2 in TEAMS:
        if team2!=team:
            against[team2]=teamVteamapi(team,team2)
    response={
        "against":against
    }
    return response

def  batsmantrackapi(batter,team=None):
    merge = matches.merge(ipl, on="ID")
    new_df = merge[merge["batter"] == batter]
    if team is not None:
        new_df = new_df[((new_df["Team1"] == team) | (new_df["Team2"] == team)) &
                        (new_df["BattingTeam"] != team)]
    if new_df.empty:
        return None
    batsman_run = new_df["batsman_run"].sum()
    batsman_out = new_df["isWicketDelivery"].sum()
    six_hit = new_df[new_df["batsman_run"] == 6].shape[0]
    four_hit = new_df[new_df["batsman_run"] == 4].shape[0]
    new_df = new_df.sort_values(by=["ID", "innings", "overs", "ballnumber"])
    new_df["batter_ball_faced"] = new_df.groupby(["ID", "batter"]).cumcount() + 1
    bd = new_df[(new_df["batter_ball_faced"] == 1) & (new_df["isWicketDelivery"] == 1) & (new_df["batsman_run"] == 0)]
    golden_duck = bd[bd["player_out"] == batter]["isWicketDelivery"].sum()
    ball_faced = new_df["ballnumber"].shape[0]

    batsman_strike_rate =( batsman_run / ball_faced) * 100
    batsman_average=(batsman_run/batsman_out)

    df = new_df.groupby('ID').sum()

    fifties = df[(df["batsman_run"] >= 50) & (df["batsman_run"] < 100)].shape[0]
    hundreds = df[(df["batsman_run"] >= 100)].shape[0]
    highest_score = df["batsman_run"].sort_values(ascending=False).head(1).values[0]

    response={
        "batsman_run":str(batsman_run),
        "batsman_out":str(batsman_out),
        "six_hit":str(six_hit),
        "four_hit":str(four_hit),
        "golden_duck":str(golden_duck),
        "ball_faced":str(ball_faced),
        "batsman_strike_rate":batsman_strike_rate,
        "batsman_average":batsman_average,
        "fifties":str(fifties),
        "hundreds":str(hundreds),
        "highest_score":str(highest_score)

    }
    return response
def battervteamapi(batter):
        TEAMS = matches["Team1"].unique()
        aginst = {}
        for t in TEAMS:
            res = batsmantrackapi(batter, t)
            if res is not None:
                aginst[t] = res
        response = {
            "aginst": aginst
        }
        return response
def bowlerstats(bowler,team=None):
    merge = matches.merge(ipl, on="ID")
    df = merge[merge["bowler"] == bowler]
    if team is not None:
            df = df[df["BattingTeam"] == team]
    if df.empty:
        return None

    total_wickets = df["isWicketDelivery"].sum()
    Runs_conceded = df["total_run"].sum()
    average = Runs_conceded / total_wickets
    total_matches_played = df["ID"].nunique()
    total_overs = df["ballnumber"].count() // 6
    total_balls = df["ballnumber"].count()
    economy = Runs_conceded / total_overs
    strike_rate = total_balls / total_wickets
    match_wicket = df.groupby("ID")["isWicketDelivery"].sum()
    three_w_hall = match_wicket[match_wicket == 3].count()
    four_w_hall = match_wicket[match_wicket == 4].count()
    match_stats = df.groupby("ID").agg(
        total_wickets=("isWicketDelivery", "sum"),
        runs_conceded=("total_run", "sum")
    ).reset_index()
    sorted_matches = match_stats.sort_values(by=["total_wickets", "runs_conceded"], ascending=[False, True])
    best_match_row = sorted_matches.iloc[0]
    bbi_wicket = best_match_row["total_wickets"]
    bbi_runs = best_match_row["runs_conceded"]

    best_bowling_figure = f"{bbi_wicket}/{bbi_runs}"
    fours = df[df["batsman_run"] == 4].shape[0]
    sixes = df[df["batsman_run"] == 6].shape[0]
    response={
        "total_wickets":str(total_wickets),
        "Runs_conceded":str(Runs_conceded),
        "average":str(average),
        "total_matches_played":str(total_matches_played),
        "total_overs":str(total_overs),
        "total_balls":str(total_balls),
        "economy":str(economy),
        "strike_rate":str(strike_rate),
        "three_w_hall":str(three_w_hall),
        "four_w_hall":str(four_w_hall),
        "best_bowling_figure":best_bowling_figure,
        "fours":str(fours),
        "sixes":str(sixes),
    }
    return  response
def bowlerVteamapi(bowler):
    TEAMS =  ipl["BattingTeam"].unique()
    aginst = {}
    for t in TEAMS:
        res = bowlerstats(bowler, t)
        if res is not None:
            aginst[t] = res
    response = {
        "aginst": aginst
    }
    return response
def battervbatter(batter1,batter2):
    first={}
    second={}
    res1=batsmantrackapi(batter1)
    res2=batsmantrackapi(batter2)
    if res1 is not None and res2 is not None:
        first[batter1]=res1
        second[batter2]=res2
        response = {
            "first":first,
            "second":second
        }
        return response
def bowlervbowler(bowler1,bowler2):
    first={}
    second={}
    res1=bowlerstats(bowler1)
    res2=bowlerstats(bowler2)
    if res1 is not None and res2 is not None:
        first[bowler1]=res1
        second[bowler2]=res2
        response = {
            "first":first,
            "second":second

        }

        return response
def orangecapapi():
    merge = matches.merge(ipl, on="ID")
    new_df = merge.sort_values(by=["Season", "batter", "bowler"], ascending=[True, True, True])
    temp_df = new_df.groupby(["Season", "batter"])["batsman_run"].sum().reset_index()
    df = temp_df.sort_values(by=["Season", "batsman_run"], ascending=[True, False])
    df.drop_duplicates(subset=["Season"], keep="first", inplace=True)
    df["Season"] = df["Season"].str.replace("2007/08", "2008")
    df["Season"] = df["Season"].str.replace("2009/10", "2010")
    orange_cap_holder = df.to_dict(orient="records")
    response={
        "orange_cap_holder":orange_cap_holder
    }
    return response
def purplecapapi():
    merge = matches.merge(ipl, on="ID")
    new_df = merge.sort_values(by=["Season", "batter", "bowler"], ascending=[True, True, True])
    temp_df = new_df.groupby(["Season", "bowler"])["isWicketDelivery"].sum().reset_index()
    df = temp_df.sort_values(by=["Season", "isWicketDelivery"], ascending=[True, False])
    df.drop_duplicates(subset=["Season"], keep="first", inplace=True)
    df["Season"] = df["Season"].str.replace("2007/08", "2008")
    df["Season"] = df["Season"].str.replace("2009/10", "2010")
    df.rename(columns={"isWicketDelivery": "wickets"}, inplace=True)
    purple_cap_holder = df.to_dict(orient="records")
    response={
        "purple_cap_holder":purple_cap_holder

    }
    return response






