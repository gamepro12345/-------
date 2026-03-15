import pyxel
import random
import math


class Player:
    def __init__(self):
        self.x = 80
        self.y = 200
        self.width = 16
        self.height = 16
        self.speed = 2
        self.tile_size = 8

        self.img = 2
        self.u = 0
        self.v = 0
        self.w_img = 16
        self.h_img = 16
        self.colkey = 0

        self.hp = 5
        self.max_hp = 5

        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 60

        self.hitbox_size = 4

    def is_wall(self, x, y):

        if x < 0 or x >= 160 or y < 0 or y >= 240:
            return True

        color = pyxel.pget(x, y)

        return color == 2

    def can_move(self, new_x, new_y):

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

        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

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

        if getattr(self, 'invincible', False):
            if (pyxel.frame_count // 5) % 2 == 0:
                return

        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w_img, self.h_img, self.colkey)

    def start_invincible(self, duration=None):

        self.invincible = True
        self.invincible_timer = duration if duration is not None else self.invincible_duration

    def get_hitbox(self):

        s = max(1, int(getattr(self, 'hitbox_size', 4)))
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        x0 = cx - s / 2
        y0 = cy - s / 2
        x1 = x0 + s
        y1 = y0 + s
        return x0, y0, x1, y1


class Bullet:
    def __init__(self, x, y, vx=0, vy=0, color=7, size=3,
                 spiral=False, origin=None, angle=0.0, angvel=1.0, radius=1.0, radial=0.0, special=False):

        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.special = special

        self.spiral = spiral

        if origin is None:
            self.origin = (x, y)
        else:
            self.origin = origin

        self.angle = angle
        self.angvel = angvel
        self.radius = radius
        self.radial = radial

        init_r = self.radius if self.radius > 0.0 else 0.1
        self.tangential_speed = self.angvel * init_r

    def update(self):

        if self.spiral:

            next_radius = self.radius + self.radial
            angvel_eff = self.tangential_speed / max(0.1, next_radius)
            next_angle = self.angle + angvel_eff

            ox, oy = self.origin

            tx = ox + math.cos(next_angle) * next_radius
            ty = oy + math.sin(next_angle) * next_radius

            dx = tx - self.x
            dy = ty - self.y

            dist = math.hypot(dx, dy)

            max_speed = math.hypot(self.tangential_speed, self.radial)

            if dist > max_speed and dist > 0:
                scale = max_speed / dist
                self.x += dx * scale
                self.y += dy * scale
            else:
                self.x = tx
                self.y = ty

            rx = self.x - ox
            ry = self.y - oy

            self.radius = math.hypot(rx, ry)
            self.angle = math.atan2(ry, rx)

        else:

            self.x += self.vx
            self.y += self.vy

    def draw(self):

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

        self.turned = False
        self.turned_counted = False

        self.shoot_timer = random.randint(10, 60)

    def update(self):

        self.y += self.speed

        if (not self.turned) and self.y >= 120:
            self.speed = -abs(self.speed)
            self.turned = True

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

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.start = True

    def draw(self):
        if not self.start:
            pyxel.bltm(0, 0, 0, 0, 0, 160, 240)
            pyxel.text(20, 50, self.title, pyxel.COLOR_YELLOW)
            pyxel.text(60, 100, "Push Enter!", pyxel.COLOR_WHITE)


class Game:
    def __init__(self):

        pyxel.init(160, 240, title="Bullet Hell", fps=30)
        pyxel.load("myedit.pyxres")

        self.title = Title()
        self.player = Player()

        self.enemies = []
        self.bullets = []

        # ★追加
        self.player_bullets = []

        self.score = 0
        self.bgm_started = False

        pyxel.run(self.update, self.draw)

    def update(self):

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.title.update()

        if self.title.start:

            self.player.update()

            # ★プレイヤー弾
            if pyxel.btnp(pyxel.KEY_Z):

                bx = self.player.x + self.player.width / 2
                by = self.player.y

                self.player_bullets.append(
                    Bullet(bx, by, vx=0, vy=-4,
                           color=pyxel.COLOR_GREEN, size=4)
                )

            # ★弾更新
            alive_pb = []
            for pb in self.player_bullets:
                pb.update()
                if pb.y > -20:
                    alive_pb.append(pb)
            self.player_bullets = alive_pb

            # 敵生成
            if random.random() < 0.02 and len(self.enemies) < 1:
                ex = random.randint(0, 160 - 8)
                ey = random.randint(-40, 20)
                self.enemies.append(Enemy(ex, ey))

            for e in self.enemies:
                e.update()

            # ★敵とプレイヤー弾の当たり判定
            new_enemies = []

            for e in self.enemies:

                hit = False

                for pb in self.player_bullets:

                    if (e.x < pb.x < e.x + e.w and
                        e.y < pb.y < e.y + e.h):

                        self.score += 200
                        hit = True
                        break

                if not hit:
                    new_enemies.append(e)

            self.enemies = new_enemies

    def draw(self):

        pyxel.cls(0)

        if self.title.start:

            pyxel.bltm(0, 0, 1, 0, 0, 160, 240)

            for e in self.enemies:
                e.draw()

            for b in self.bullets:
                b.draw()

            # ★プレイヤー弾描画
            for pb in self.player_bullets:
                pb.draw()

            self.player.draw()

            pyxel.text(110, 14, f"SCORE: {self.score}", pyxel.COLOR_YELLOW)

        else:

            pyxel.bltm(0, 0, 0, 0, 0, 160, 240)

        self.title.draw()


if __name__ == "__main__":
    Game()