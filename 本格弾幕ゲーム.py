import pyxel

class Player:
    def __init__(self):
        self.x = 80  # 画面中央（160/2 = 80）
        self.y = 200  # 画面下部
        self.width = 8
        self.height = 8
        self.speed = 2
    
    def update(self):
        # 矢印キーで移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(0, self.x - self.speed)
        
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(160 - self.width, self.x + self.speed)
        
        if pyxel.btn(pyxel.KEY_UP):
            self.y = max(0, self.y - self.speed)
        
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y = min(240 - self.height, self.y + self.speed)
    
    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, pyxel.COLOR_WHITE)

class Title:
    def __init__(self):
        self.title = "Bullet Hell"
        self.start = False
        self.gameover = False
        self.clear = False
        self.time = 0
        

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.start = True

    def draw(self):
        if not self.start:
            pyxel.bltm(0, 0, 0, 0, 0, 160, 240)  # マップ番号0を表示
            # タイトルを大きく黄色で表示（複数行で拡大効果）
            pyxel.text(20, 50, self.title, pyxel.COLOR_YELLOW)
            pyxel.text(60, 100, "Push Enter!", pyxel.COLOR_WHITE)

class Game:
    def __init__(self):
        pyxel.init(160, 240, title="Bullet Hell", fps=60)
        pyxel.load("myedit.pyxres")
        self.title = Title()
        self.player = Player()
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.title.update()
        
        # ゲーム開始後、プレイヤーを更新
        if self.title.start:
            self.player.update()
    
    def draw(self):
        pyxel.cls(0)
        # ゲーム開始前はマップ0、開始後はマップ1を表示
        if self.title.start:
            pyxel.bltm(0, 0, 1, 0, 0, 160, 240)  # マップ番号1を表示（ゲーム画面）
            self.player.draw()  # プレイヤーを描画
        else:
            pyxel.bltm(0, 0, 0, 0, 0, 160, 240)  # マップ番号0を表示（タイトル）
        
        self.title.draw()

if __name__ == "__main__":
    Game()
