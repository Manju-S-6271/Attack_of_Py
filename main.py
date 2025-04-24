# 初期化
import random
import os
import platform
import inquirer
import pygame

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
    def run(cls, command:str):
        """指定されたコマンドを実行する関数

        Args:
            command (str): 実行するコマンド
        """
        # OS名 [Windows / MacOS / etc] を取得
        os_name = cls.os_name
        
        if os_name in ["Windows", "Darwin"]:
            os.system(command)
        else:
            print("[Ran:" + command + "]")

    @classmethod
    def os_check(cls) -> str:
        """OSチェックを行う関数

        Returns:
            os_name (str): OS名 [Windows / MacOS / etc]
        """
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
        """OSに応じて画面をクリアする関数
        """
        # OS名 [Windows / MacOS / etc] を取得
        os_name = cls.os_name

        if os_name == "Windows":
            os.system("cls")
        elif os_name == "Darwin":
            os.system("clear")
        else:
            print("\n" * 100)

    @classmethod
    def title(cls, text:str, darwin_clear:bool=False):
        """OSに応じてタイトルを設定する関数

        Args:
            text (str): タイトルに設定する文字列
            darwin_clear (bool): MacOSの場合、タイトル設定後にクリアするかどうか (Falseだと、-neが残るため)
        """
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
    def battle_frame_count(player_name, enemy_name) -> list:
        """バトル枠の表示個数計算を行う関数

        Args:
            player_name (str): プレイヤーの名前
            enemy_name (str): 敵の名前
        
        Returns:
            returns (list): バトル枠の表示個数計算結果 [frame_count, bigger_name, diff]
        """
        # 名前の字数を取得
        player_name_count = len(player_name)
        enemy_name_count = len(enemy_name)

        # 多い方の字数と20(各種数値の表示枠分)を取得
        frame_count = max(player_name_count, enemy_name_count) + 20

        # Player + "Easy"(100, 20, 25, 100, "Slime", 80, 20, 25)の時
        # +-----------------------+
        # | NAME   HP   ATK  MP   | (下の計算により、プレイヤー字数の方が1字多いことがわかるため、出力は[25, "Player", 1]となる。)
        # | Player 100  025  100  | (この場合、プレイヤー名(6)+定数(19)=25)
        # | Slime  080  ???  ???  | (この場合、敵名(5)+定数(19)=24)
        # +-----------------------+ (25-24=1)
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
    def battle_frame(battle_data:dict, battle_frame_data):
        # # すべてを個別に変数化
        # player_name = battle_data["player"]
        # player_hp = battle_data["player_hp"]
        # player_min_attack = battle_data["player_min_attack"]
        # player_mp = battle_data["player_mp"]
        # enemy_name = battle_data["enemy_name"]
        # enemy_hp = battle_data["enemy_hp"]
        # frame_count, bigger_name, diff = battle_frame_data

        # # プレイヤー名もしくは敵名に空白を追加
        # s_player_name = f"{player_name}{' ' * diff}" if bigger_name == "enemy" else player_name
        # s_enemy_name = f"{enemy_name}{' ' * diff}" if bigger_name == "player" else enemy_name
        # v_bigger_name = max(len(player_name), len(enemy_name))

        # # 各種数字を3桁化し、1空白を追加する (HP4桁の場合はそのまま表示)
        # s_player_hp = f"{player_hp:03} " if len(str(player_hp)) != 4 else str(player_hp)
        # s_enemy_hp = f"{enemy_hp:03} " if len(str(enemy_hp)) != 4 else str(enemy_hp)
        # s_player_min_attack = f"{player_min_attack:03}"
        # s_player_mp = f"{player_mp:03}"

        # # バトル枠の表示
        # print(f"+{'-' * (frame_count - 2)}+")
        # print(f"| Name{' ' * (v_bigger_name - 3)}HP   ATK   MP   |")
        # print(f"| {s_player_name} {s_player_hp} {s_player_min_attack}   {s_player_mp}  |")
        # print(f"| {s_enemy_name} {s_enemy_hp} ???   ???  |")
        # print(f"+{'-' * (frame_count - 2)}+")

        """バトルのステータスを表示する関数

        Args:
            battle_data (dict): バトルデータ
            battle_frame_data (tuple): バトルフレームデータ
        """
        frame_count, bigger_name, diff = battle_frame_data
        v_bigger_name = max(len(battle_data["player"]), len(battle_data["enemy_name"]))

        # Format names with proper spacing
        player_spacing = ' ' * diff if bigger_name == "enemy" else ''
        enemy_spacing = ' ' * diff if bigger_name == "player" else ''

        # Format HP values with proper padding
        player_hp_str = f"{battle_data['player_hp']:03} " if len(str(battle_data['player_hp'])) < 4 else str(battle_data['player_hp'])
        enemy_hp_str = f"{battle_data['enemy_hp']:03} " if len(str(battle_data['enemy_hp'])) < 4 else str(battle_data['enemy_hp'])

        # Create battle frame
        print(f"+{'-' * (frame_count - 2)}+")
        print(f"| Name{' ' * (v_bigger_name - 3)}HP   ATK   MP   |")
        print(f"| {battle_data['player']}{player_spacing} {player_hp_str} {battle_data['player_min_attack']:03}   {battle_data['player_mp']:03}  |")
        print(f"| {battle_data['enemy_name']}{enemy_spacing} {enemy_hp_str} ???   ???  |")
        print(f"+{'-' * (frame_count - 2)}+")
    
    def battle_choice(battle_data:dict, items:list) -> str:
        """バトルの選択肢を表示する関数
        
        Args:
            battle_data (dict): バトルデータ
            items (list): アイテムリスト
        
        Returns:
            choice (str): 選択されたアクション
        """
        # 選択肢を作成
        choices = ["Attack", "Defend"]

        # MPの有無とアイテムの有無を確認
        if battle_data["player_mp"] > 25:
            choices.append("Magic")
        elif len(items) > 0:
            choices.append("Item")
        

        # 選択肢を表示
        choice = inquirer.list_input(
            message="Select your action",
            choices=choices,
            default="Attack",
        )
        
        if choice == "Magic":
            # Magicの選択肢を表示
            choices = []

            # 可能な魔法を確認
            if battle_data["player_mp"] > 50:
                choices.append("Attack with Magic")
            if battle_data["player_mp"] > 25:
                choices.append("Heal myself")

            choice = inquirer.list_input(
                message="Select your magic",
                choices=choices
            )
        elif choice == "Item":
            # アイテムの選択肢を表示
            choices = []

            # アイテムがある場合は選択肢を追加
            for item in items:
                choices.append(item)

            choice = inquirer.list_input(
                message="Select your item",
                choices=choices
            )

        return choice

    class battle_attack:
            def player(battle_data:dict) -> str:
                """攻撃を行う関数
                Args:
                    battle_data (dict): バトルデータ
                
                Returns:
                    battle_data (dict): 攻撃後のバトルデータ
                """

                # 攻撃の宣誓
                print(f"{battle_data['player']} is attacking {battle_data['enemy_name']}...")

                # プレイヤーの攻撃力をランダムに決定
                attack_power = random.randint(battle_data["player_min_attack"], battle_data["player_max_attack"])
                successed = random.randint(0, 100)
                critical_hit = random.randint(0, 100)

                # 攻撃が成功した場合
                if successed != 1:
                    # 攻撃力をランダムに決定
                    attack_power = random.randint(battle_data["player_min_attack"], battle_data["player_max_attack"])
                else:
                    # 攻撃が失敗した場合
                    attack_power = 0
                    print("Attack missed!")
                    return battle_data
                
                # 敵のHPを減少
                battle_data["enemy_hp"] -= attack_power


                if critical_hit <= 90:
                    print(f"{battle_data['player']} attacked {battle_data['enemy_name']} for {attack_power} damage!")
                else:
                    # クリティカルヒット
                    attack_power *= 1.5
                    print(f"Critical Hit! {battle_data['player']} attacked {battle_data['enemy_name']} for {attack_power} damage!")

                # 敵のHPが0以下になった場合
                if battle_data["enemy_hp"] <= 0:
                    print(f"{battle_data['enemy_name']} has been defeated!")
                    # 敵のHPを0にする
                    battle_data["enemy_hp"] = 0
                    # 戦闘終了
                    inquirer.confirm("Press Enter to continue...")
                    # 終了
                    exit()

                return battle_data
            
            def enemy(battle_data:dict) -> dict:
                


# キャラクター関係
class character:
    # 初期キャラクター設定
    settings = [
        inquirer.Text(
            "Player", 
            message="Enter your name (English Only)",
        ),
        inquirer.List(
            "Level",
            message="Select the level",
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

# 音楽関係
class music:
    wily = "/Users/manju/Documents/GitHub/Attack_of_Py/Wily_Stage_1_BGM.wav"

    def initialize(music_path):
        """音楽を初期化する関数

        Args:
            music_path (str): 音楽ファイルのパス
        """
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)

    @classmethod
    def play_bgm(self, music_name):
        """音楽を再生する関数

        Args:
            music_name (str): 音楽の名前
        """
        if music_name == "wily":
            music.initialize(self.wily)
            pygame.mixer.music.play(loops=-1)
    

# Windowsの場合のみ文字化け対策(文字コードをUTF-8に変更)
if os_command.os_name == "Windows":
    os_command.run("echo off")
    os_command.run("chcp 65001")
    os_command.clear()


# タイトル設定
os_command.title("Attack of Python")

# キャラクター設定
player_select = inquirer.prompt(character.settings)
items = []
defend_flagged = False

# プレイヤーの名前・パラメータを取得
player_name = player_select['Player']
player_hp, player_min_attack, player_max_attack, player_mp, enemy_name, enemy_hp, enemy_min_attack, enemy_max_attack, enemy_mp = character.level_power[player_select['Level']]
battle_data = {
    "player": player_name, 
    "player_hp": player_hp, 
    "player_min_attack": player_min_attack, 
    "player_max_attack": player_max_attack, 
    "player_mp": player_mp, 
    "enemy_name": enemy_name, 
    "enemy_hp": enemy_hp, 
    "enemy_min_attack" : enemy_min_attack, 
    "enemy_max_attack" : enemy_max_attack, 
    "enemy_mp": enemy_mp
}


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
    print("enemy_mp: ", enemy_mp)
    print("os_name: ", os_command.os_name)
    

# バトル枠
BGM_instance = music.play_bgm("wily")
while True:
    battle_frame_data = battle.battle_frame_count(battle_data["player"], battle_data["enemy_name"])
    battle.battle_frame(battle_data, battle_frame_data)
    choice = battle.battle_choice(battle_data, items)
    print("You selected: " + choice)
    inquirer.confirm("Press Enter to continue...")

    os_command.clear()