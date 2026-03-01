import pyxel
import random
import math


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

        # ピクセルの色を取得
        color = pyxel.pget(x, y)

        # 灰色（色番号2）に当たったら壁
        return color == 2

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


class Bullet:
    def __init__(self, x, y, vx=0, vy=0, color=7, size=3,
                 spiral=False, origin=None, angle=0.0, angvel=0.0, radius=0.0, radial=0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size

        # spiral motion
        self.spiral = spiral
        if origin is None:
            self.origin = (x, y)
        else:
            self.origin = origin
        self.angle = angle
        self.angvel = angvel
        self.radius = radius
        self.radial = radial

    def update(self):
        if self.spiral:
            self.angle += self.angvel
            self.radius += self.radial
            ox, oy = self.origin
            self.x = ox + math.cos(self.angle) * self.radius
            self.y = oy + math.sin(self.angle) * self.radius
        else:
            self.x += self.vx
            self.y += self.vy

    def draw(self):
        # 四角で大きさを表現（中心合わせ）
        s = int(self.size)
        px = int(self.x) - s // 2
        py = int(self.y) - s // 2
        if s <= 1:
            pyxel.pset(int(self.x), int(self.y), self.color)
        else:
            pyxel.rect(px, py, s, s, self.color)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        self.speed = 0.3
        # 次に弾を撃つまでのフレーム数（ランダム）
        self.shoot_timer = random.randint(30, 120)

    def update(self):
        # 少し下へ移動する（動きが欲しい場合）
        self.y += self.speed
        # カウントダウン
        self.shoot_timer -= 1

    def can_shoot(self):
        return self.shoot_timer <= 0

    def reset_shoot_timer(self):
        self.shoot_timer = random.randint(30, 120)

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, pyxel.COLOR_RED)

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
        self.enemies = []
        self.bullets = []
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.title.update()
        
        # ゲーム開始後、プレイヤーを更新
        if self.title.start:
            self.player.update()
            # 敵生成（ランダム）
            # 毎フレーム0.02の確率でスポーン（調整可）
            if random.random() < 0.02 and len(self.enemies) < 120:
                ex = random.randint(0, 160 - 8)
                ey = random.randint(-40, 20)
                self.enemies.append(Enemy(ex, ey))

            # 敵更新・射撃
            for e in self.enemies:
                e.update()
                if e.can_shoot():
                    # らせん弾を生成（サイズ大きめ）
                    bx = e.x + e.w / 2
                    by = e.y + e.h / 2
                    origin = (bx, by)
                    angle = random.uniform(0, 2 * math.pi)
                    angvel = random.uniform(-0.15, 0.15)
                    radial = random.uniform(0.4, 1.2)
                    size = random.randint(2, 5)
                    self.bullets.append(
                        Bullet(bx, by, color=8, size=size, spiral=True,
                               origin=origin, angle=angle, angvel=angvel, radius=0.0, radial=radial)
                    )
                    e.reset_shoot_timer()

            # 弾更新・削除（画面外）
            alive_bullets = []
            for b in self.bullets:
                b.update()
                if 0 <= b.x < 160 and 0 <= b.y < 240:
                    alive_bullets.append(b)
            self.bullets = alive_bullets
            
            # 敵は画面下に出たら削除
            self.enemies = [e for e in self.enemies if e.y < 260]
    
    def draw(self):
        pyxel.cls(0)
        # ゲーム開始前はマップ0、開始後はマップ1を表示
        if self.title.start:
            pyxel.bltm(0, 0, 1, 0, 0, 160, 240)  # マップ番号1を表示（ゲーム画面）
            # 敵と弾を描画
            for e in self.enemies:
                e.draw()
            for b in self.bullets:
                b.draw()
            # プレイヤーを描画（最後に）
            self.player.draw()
        else:
            pyxel.bltm(0, 0, 0, 0, 0, 160, 240)  # マップ番号0を表示（タイトル）
        
        self.title.draw()

if __name__ == "__main__":
    Game()
