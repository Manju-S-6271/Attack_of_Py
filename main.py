# 初期化
import random
import os
import platform
import inquirer
import pprint

# デバッグモード
class debug:
    enabled = False
    if enabled == True:
        # デバッグ追加モジュール
        # OSチェックをスキップ
        oscheck_bypass_enabled = True
        # 設定後の内容表示モード (内容表示後に終了)
        show_setting_mode_enabled = True

# OS関係
class os_command:
    os_name = platform.system()

    def os_check():
        # OS名 [Windows / MacOS / etc] を取得
        os_name = platform.system()

        # OSがネイティブサポートされていないOSの場合は確認
        native_support_os = ["Windows", "Darwin"]
        if os_name not in native_support_os and oscheck_bypass == False:
            print("ご利用のOS(" + os_name + ")はネイティブサポートされていません。")
            print("ネイティブサポートされていないOSでの動作は保証されません。")
            print("また、一部の機能は制限されます。")
            inquirer.confirm("続行しますか？", default=True)
            if not inquirer.prompt:
                exit()
        return os_name
    
    def clear():
        # OS名 [Windows / MacOS / etc] を取得
        os_name = platform.system()

        if os_name == "Windows":
            os.system("cls")
        elif os_name == "Darwin":
            os.system("clear")
        else:
            print("\n" * 100)

    def title(text):
        # OS名 [Windows / MacOS / etc] を取得
        os_name = platform.system()

        if os_name == "Windows":
            os.system("title " + text)
        elif os_name == "Darwin":
            os.system(f'echo -ne "\\033]0;{text}\\007"')
        else:
            print("[" + text + "]")

if os_command.os_name == "Windows":
    os.system("chcp 65001")

os_command.title("Attack of Python")

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

if debug.show_setting_mode_enabled == True:
    print("player_name: ", player_name)
    print("player_hp: ", player_hp)
    print("player_min_attack: ", player_min_attack)
    print("player_max_attack: ", player_max_attack)
    print("player_mp: ", player_mp)
    print("enemy_name: ", enemy_name)
    print("enemy_hp: ", enemy_hp)
    print("enemy_min_attack: ", enemy_min_attack)
    print("enemy_max_attack: ", enemy_max_attack)
    print("os_name: ", os_command.os_name)
    exit()
    
# バトル