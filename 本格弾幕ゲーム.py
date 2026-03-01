import pyxel

class Player:
    def __init__(self):
        self.x = 80  # 画面中央（160/2 = 80）
        self.y = 200  # 画面下部
        self.width = 8
        self.height = 8
        self.speed = 2
        self.tile_size = 8  # タイルサイズ
    
    def is_wall(self, x, y):
        # 画面外チェック
        if x < 0 or x >= 160 or y < 0 or y >= 240:
            return True

    # タイル座標へ変換（1タイル=8px）
        tile_x = x // self.tile_size
        tile_y = y // self.tile_size

    # マップ1からタイル番号取得
        tile = pyxel.tilemap(1).pget(tile_x, tile_y)

    # (2,0) のタイルなら壁
        return tile == (2, 0)
    
    def can_move(self, new_x, new_y):
        """指定位置に移動できるか判定"""
        # プレイヤーの複数地点をチェック
        check_points = [
            (new_x, new_y),
            (new_x + self.width - 1, new_y),
            (new_x, new_y + self.height - 1),
            (new_x + self.width - 1, new_y + self.height - 1),
            (new_x + self.width // 2, new_y + self.height // 2)
        ]
        
        for px, py in check_points:
            if self.is_wall(px, py):
                return False
        
        return True
    
    def update(self):
        # 矢印キーで移動（当たり判定付き）
        if pyxel.btn(pyxel.KEY_LEFT):
            new_x = max(0, self.x - self.speed)
            if self.can_move(new_x, self.y):
                self.x = new_x
        
        if pyxel.btn(pyxel.KEY_RIGHT):
            new_x = min(160 - self.width, self.x + self.speed)
            if self.can_move(new_x, self.y):
                self.x = new_x
        
        if pyxel.btn(pyxel.KEY_UP):
            new_y = max(0, self.y - self.speed)
            if self.can_move(self.x, new_y):
                self.y = new_y
        
        if pyxel.btn(pyxel.KEY_DOWN):
            new_y = min(240 - self.height, self.y + self.speed)
            if self.can_move(self.x, new_y):
                self.y = new_y
    
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
