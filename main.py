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
            os.system(f'echo -ne "\\033]0;{text}\\007"')
            if darwin_clear:
                os.system("clear")
        else:
            print("[" + text + "]")

# キャラクター関係
class character:
    # 初期キャラクター設定
    settings = [
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
    
    # レベルごとのパラメータ
    level_power = {
        # ["プレイヤーのHP", "プレイヤーの最小攻撃力", "プレイヤーの最大攻撃力", "プレイヤーのMP", "敵の名前", "敵のHP", "敵の最小攻撃力", "敵の最大攻撃力"]
        "Easy": [100, 20, 25, 100, "スライム", 80, 20, 25],
        "Normal": [150, 25, 30, 150, "エアーマン", 120, 30, 35],
        "Hard": [200, 50, 60, 200, "竜王", 300, 40, 50], 
        "SAORI": [1000, 100, 120, 500, "サオリ・ヨシダ", 9999, 9999, 9999]
    }

# Windowsの場合のみ文字化け対策(文字コードをUTF-8に変更)
if os_command.os_name == "Windows":
    os_command.run("echo off")
    os_command.run("chcp 65001")
    os_command.clear()


# タイトル設定
os_command.title("Attack of Python", True)

# キャラクター設定
player_select = inquirer.prompt(character.settings)

# プレイヤーの名前・パラメータを取得
player_name = player_select['Player']
player_hp, player_min_attack, player_max_attack, player_mp, enemy_name, enemy_hp, enemy_min_attack, enemy_max_attack = character.level_power[player_select['Level']]

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
    
# バトル