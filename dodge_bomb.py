import os
import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1000, 700
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def init_kk_imgs():
    kk_img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)#普通のこうかとん
    kk_img2 = pg.transform.flip(kk_img0, True, False)#逆向きのこうかとん
    kk_img3 = pg.transform.rotozoom(kk_img0, 0, 1.0)#それぞれの向きに合わせて角度を変更
    kk_img4 = pg.transform.rotozoom(kk_img0, 315, 1.0)
    kk_img5 = pg.transform.rotozoom(kk_img0, 45, 1.0)
    kk_img6 = pg.transform.rotozoom(kk_img2, 90, 1.0)
    kk_img7 = pg.transform.rotozoom(kk_img2, 270, 1.0)
    kk_img8 = pg.transform.rotozoom(kk_img2, 315, 1.0)
    kk_img9 = pg.transform.rotozoom(kk_img2, 45, 1.0)
    return {
        (0, 0): kk_img0,
        (0, -5): kk_img6,
        (0, +5): kk_img7,
        (-5, 0): kk_img3,
        (+5, 0): kk_img2,
        (-5, -5): kk_img4,
        (+5, +5): kk_img8,
        (+5, -5): kk_img9,
        (-5, +5): kk_img5,
    }


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect，または，爆弾Rect
    戻り値：真理値タプル（横方向，縦方向）
    画面内ならTrue／画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_imgs = init_kk_imgs()
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))  # 1辺が20の空のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 空のSurfaceに赤い円を描く
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の横方向速度，縦方向速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # 衝突判定
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in  DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        kk_img = kk_imgs[tuple(sum_mv)]

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
