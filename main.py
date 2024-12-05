# 初期化
import random
import os
import inquirer
import pprint

os.system("title ATTACK OF PY")
os.system("cls")
level_power = {
    # ["プレイヤーのHP", "プレイヤーの最小攻撃力", "プレイヤーの最大攻撃力", "プレイヤーのMP", "敵の名前", "敵のHP", "敵の最小攻撃力", "敵の最大攻撃力"]
    "Easy": [100, 20, 25, 100, "スライム", 80, 20, 25],
    "Normal": [150, 25, 30, 150, "エアーマン", 120, 30, 35],
    "Hard": [200, 50, 60, 200, "竜王", 300, 40, 50], 
    "SAORI": [1000, 100, 120, 500, "サオリ・ヨシダ", 9999, 9999, 9999]
}


# レベル選択
questions = [
    inquirer.Text(
        "Player", 
        message="プレイヤーの名前を入力してください"
    ),
    inquirer.List(
        "Level",
        message="レベルを選択してください",
        choices=["Easy", "Normal", "Hard", "SAORI"],
    ),
]

player_select = inquirer.prompt(questions)

player_name = player_select['Player']
player_hp, player_min_attack, player_max_attack, player_mp, enemy_name, enemy_hp, enemy_min_attack, enemy_max_attack = level_power[player_select['Level']]

# debug: 全ての変数を表示
debug = False
if debug == True:
    print("player_name: ", player_name)
    print("player_hp: ", player_hp)
    print("player_min_attack: ", player_min_attack)
    print("player_max_attack: ", player_max_attack)
    print("player_mp: ", player_mp)
    print("enemy_name: ", enemy_name)
    print("enemy_hp: ", enemy_hp)
    print("enemy_min_attack: ", enemy_min_attack)
    print("enemy_max_attack: ", enemy_max_attack)
    exit()
    
# バトル