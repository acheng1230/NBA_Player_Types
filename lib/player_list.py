import pandas as pd

def load_total():
    total = pd.read_csv("/Users/alexcheng/dsi/dsi_workspace/projects/project-captsone/workspace/web_scraping/player_list/total_player_df.csv")
    total_list = list(total['url'])
    return total_list

def load_part1():
    part_1_df = pd.read_csv("/Users/alexcheng/dsi/dsi_workspace/projects/project-captsone/workspace/web_scraping/player_list/player_df_part1.csv")
    part_1_list = list(part_1_df['url'])
    return part_1_list

def load_part2():
    part_2_df = pd.read_csv("/Users/alexcheng/dsi/dsi_workspace/projects/project-captsone/workspace/web_scraping/player_list/player_df_part2.csv")
    part_2_list = list(part_2_df['url'])
    return part_2_list

def load_test():
    test_df = pd.read_csv("/Users/alexcheng/dsi/dsi_workspace/projects/project-captsone/workspace/web_scraping/player_list/test_players.csv")
    test_list = list(test_df['url'])
    return test_list
