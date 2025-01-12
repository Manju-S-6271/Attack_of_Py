# 初期化
import random
import os
import platform
import inquirer

# デバッグモード
class debug:
    enabled = False
    if enabled == True:
        # デバッグ追加モジュール (必要に応じて変更すること)
        # OSチェックをスキップ
        oscheck_bypass_enabled = True
        # 設定後の内容表示モード (内容表示後に終了)
        show_setting_mode_enabled = True
    else:
        # デバッグ追加モジュール (変更しないこと)
        oscheck_bypass_enabled = False
        show_setting_mode_enabled = False

# OS関係
class os_command:
    os_name = platform.system()

    @classmethod
    def run(cls, command):
        # OS名 [Windows / MacOS / etc] を取得
        os_name = cls.os_name
        
        if os_name in ["Windows", "Darwin"]:
            os.system(command)
        else:
            print("[Ran:" + command + "]")

    @classmethod
    def os_check(cls):
        # OS名 [Windows / MacOS / etc] を取得
        os_name = cls.os_name
        
        # OSがネイティブサポートされていないOSの場合は確認
        native_support_os = ["Windows", "Darwin"]
        if os_name not in native_support_os and debug.oscheck_bypass_enabled == False:
            print("ご利用のOS(" + os_name + ")はネイティブサポートされていません。")
            print("ネイティブサポートされていないOSでの動作は保証されません。")
            print("また、一部の機能は制限されます。")
            if not inquirer.confirm("続行しますか？", default=True):
                exit()
        return os_name
    
    @classmethod
    def clear(cls):
        # OS名 [Windows / MacOS / etc] を取得
        os_name = cls.os_name

        if os_name == "Windows":
            os.system("cls")
        elif os_name == "Darwin":
            os.system("clear")
        else:
            print("\n" * 100)

    @classmethod
    def title(cls, text, darwin_clear=False):
        # darwin_clear: MacOSの場合、タイトル設定後にクリアするかどうか (Falseだと、-neが残るため)
        # OS名 [Windows / MacOS / etc] を取得
        os_name = cls.os_name

        if os_name == "Windows":
            os.system("title " + text)
        elif os_name == "Darwin":
            os.system(f'printf "\\033]0;{text}\\007"')
            if darwin_clear:
                os.system("clear")
        else:
            print("[" + text + "]")

# バトル制御関係
class battle:
    # バトル枠の表示個数計算
    def battle_frame_count(player_name, enemy_name):
        # 名前の字数を取得
        player_name_count = len(player_name)
        enemy_name_count = len(enemy_name)

        # 多い方の字数と20(各種数値の表示枠分)を取得
        frame_count = max(player_name_count, enemy_name_count) + 20

        # Player + "Easy"(100, 20, 25, 100, "Slime", 80, 20, 25)の時
        # +--------------------+
        # | NAME   HP  ATK MP  | (下の計算により、プレイヤー字数の方が1字多いことがわかるため、出力は[20, "Player", 1]となる。)
        # | Player 100 025 100 | (この場合、プレイヤー名(6)+定数(14)=20)
        # | Slime  080 ??? ??? | (この場合、敵名(5)+定数(14)=19)
        # +--------------------+ (20-19=1)
        # (ATKは最大のみ表示, 敵ATKは??で表示, 名前はPlayerとSlimeのどちらかが多い方に合わせる)

        # 字数が多い方がどっちかを演算
        if player_name_count > enemy_name_count:
            bigger_name = "player"
            diff = player_name_count - enemy_name_count
        else:
            bigger_name = "enemy"
            diff = enemy_name_count - player_name_count
        
        # frame_count, bigger_name, diffを
        returns = [frame_count, bigger_name, diff]

        return returns
    
    # バトル枠の表示
    def battle_frame(battle_public_data, battle_frame_data):
        # すべてを個別に変数化
        player_name, player_hp, player_min_attack, player_mp, enemy_name, enemy_hp = battle_public_data
        frame_count, bigger_name, diff = battle_frame_data

        # プレイヤー名もしくは敵名に空白(字数が多い方は1つ・字数が少ない方は1+diffつ)を追加
        if player_name == bigger_name:
            s_player_name = f"{player_name} "
            s_enemy_name = f"{enemy_name}{" " * (1 + diff)}"
        else:
            s_ #次ここから 上のやつ見ればわかる

        # 各種数字を3桁化し、1空白を追加する。
        # ただし、4桁の場合は、そのまま表示する。

# キャラクター関係
class character:
    # 初期キャラクター設定
    settings = [
        inquirer.Text(
            "Player", 
            message="プレイヤーの名前を入力してください（英語のみ）"
        ),
        inquirer.List(
            "Level",
            message="レベルを選択してください",
            choices=["Easy", "Normal", "Hard", "SAORI"],
        ),
    ]
    
    # レベルごとのパラメータ
    level_power = {
        # ["プレイヤーのHP", "プレイヤーの最小攻撃力", "プレイヤーの最大攻撃力", "プレイヤーのMP", "敵の名前", "敵のHP", "敵の最小攻撃力", "敵の最大攻撃力", "敵のMP"]
        "Easy": [100, 20, 25, 100, "Slime", 80, 20, 25, 100],
        "Normal": [150, 25, 30, 150, "Air Man", 120, 30, 35, 100],
        "Hard": [200, 50, 60, 200, "Dragonlord", 300, 40, 50, 400], 
        "SAORI": [1000, 100, 120, 500, "SAORI YOSHIDA", 9999, 9999, 9999, 0]
    }

# Windowsの場合のみ文字化け対策(文字コードをUTF-8に変更)
if os_command.os_name == "Windows":
    os_command.run("echo off")
    os_command.run("chcp 65001")
    os_command.clear()


# タイトル設定
os_command.title("Attack of Python")

# キャラクター設定
player_select = inquirer.prompt(character.settings)

# プレイヤーの名前・パラメータを取得
player_name = player_select['Player']
player_hp, player_min_attack, player_max_attack, player_mp, enemy_name, enemy_hp, enemy_min_attack, enemy_max_attack = character.level_power[player_select['Level']]
battle_data = [player_name, player_hp, player_min_attack, player_max_attack, player_mp, enemy_name, enemy_hp, enemy_min_attack, enemy_max_attack]
battle_public_data = [player_name, player_hp, player_min_attack, player_mp, enemy_name, enemy_hp]

# もしデバッグモード・設定表示モードが有効ならすべての変数を表示・終了
if debug.enabled and debug.show_setting_mode_enabled:
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
    
# バトル枠
while True:
    battle_frame_data = battle.battle_frame_count(player_name, enemy_name)
    battle.battle_frame(battle_public_data, battle_frame_data)
    break