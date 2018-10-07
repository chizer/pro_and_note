import pygame as pg
import sys
import random
import time
pg.init()#初始化
#设置窗口
game_window = pg.display.set_mode((600,500))
#设置窗口标题
pg.display.set_caption('jieqiu')
#设置窗口颜色
window_color = (0,255,255)
#设置球体颜色 接球板颜色
ball_color = (255,255,0)
rect_color = (255,0,0)
#初始化球的位置
ball_x = random.randint(10,590)
ball_y = 10
move_x = 1#用来表示球每次移动的多少位置
move_y = 1
score = 0#记分板
font = pg.font.Font(None,70)#字体 大小
point =1#计分
count = 0
while True:
    game_window.fill(window_color)
    #是窗口不断更新 不要退出
    for event in pg.event.get():
        if event.type ==pg.QUIT:
            sys.exit()
    #获取鼠标的位置
    mouse_x,mouse_y = pg.mouse.get_pos()
    #创建一个球 三个参数，在窗口里面画，颜色，(位置x,y),半径
    pg.draw.circle(game_window,ball_color,(ball_x,ball_y),10)
    #画一个矩形接球 在窗口里面，颜色，（位置x跟随鼠标移动，y只能在最下面，宽度，高度）
    pg.draw.rect(game_window,rect_color,(mouse_x,490,100,10))
    my_text = font.render(str(score),False,(255,255,255))#记分字体 抗拒值 字体颜色
    game_window.blit(my_text,(500,30))
    ball_x += move_x #让球动起来 每次移动
    ball_y += move_y
    if ball_x <= 10 or ball_x>=590:#球的位置左右检测
        move_x = -move_x
    if ball_y <=10:#球的位置到达最上端
        move_y = -move_y
    elif mouse_x-10 <ball_x <mouse_x+110 and ball_y>=480:
        move_y = -move_y
        score +=point
        count += 1
        if count == 3:
            count = 0
            point += point
            if mouse_x>0:
                move_x += 1
            else:
                move_x -= 1
            move_y -= 1
    elif ball_y >= 490 and (ball_x<=mouse_x-10 or ball_x>=mouse_x+100+10):
        break


    pg.display.update()
    time.sleep(0.005)#刷新速度