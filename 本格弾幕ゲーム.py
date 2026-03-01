import pyxel

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
            pyxel.text(30, 100, "Enterキーでスタート", pyxel.COLOR_WHITE)

class Game:
    def __init__(self):
        pyxel.init(160, 240, title="Bullet Hell", fps=60)
        pyxel.load("myedit.pyxres")
        self.title = Title()
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.title.update()
    
    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 160, 240)  # マップ番号0を表示
        self.title.draw()

if __name__ == "__main__":
    Game()
