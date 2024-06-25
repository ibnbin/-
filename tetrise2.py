import random
import sys
import pygame
import time



class Tetrise():
    def __init__(self):
        # 初始化
        pygame.mixer.init()
        # 加载音乐文件
        pygame.mixer.music.load('resource/sound/background.mp3')
        # 开始播放音乐流
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

        # 1.初始化pygame
        pygame.init()

        # 2.设置主屏幕窗口，4.设置背景颜色，拿到窗口对象
        self.screen = pygame.display.set_mode((250, 500))

        # 8设置得分
        self.score = [0]

        # 9 游戏结束标志
        self.gameover = []

        # 10.2帧数统计变量
        self.speeds = 0

        # 13 是否按下下键
        self.press = False

        # 文字
        font = pygame.font.SysFont('Times', 30)
        # 创建文字对象
        self.text = font.render('GameOver', True, (200, 30, 30))

        # 5.创建元素块
        # 根据左上角定坐标 ,方块大小23 间隙2
        self.all_block = [
            [[0, 0], [0, -1], [0, 1], [0, 2]],  # I
            [[0, 0], [0, 1], [1, 1], [1, 0]],  # 田
            [[0, 0], [0, -1], [-1, 0], [-1, 1]],  # Z
            [[0, 0], [0, 1], [-1, -1], [-1, 0]],  # 倒Z
            [[0, 0], [0, 1], [1, 0], [0, -1]],  # 接地线
            [[0, 0], [1, 0], [-1, 0], [1, -1]],  # L
            [[0, 0], [1, 0], [-1, 0], [1, 1]]  # 倒L
        ]
        # 5.1返回任意一项，选择一个方块
        self.select_block = list(random.choice(self.all_block))

        # 5.2创建背景 20行10列（从顶部掉落上面还需两行-四行）
        self.background = [[0 for column in range(0, 10)]for row in range(0, 22)]
        # 5.3 0不上色 将第0行（底部）置位1，防止落出页面
        self.background[0] = [1 for column in range(0, 10)]


        # 5.4规定初始掉落位置  (21行第5列)
        self.block_initial_position = [21, 5]

        # 4.设置标题
        pygame.display.set_caption('俄罗斯方块')

    # 5.5方块掉落
    def block_down_move(self):
        # 拿y和x的初始值  [21, 5],左下角为原点
        y_drop = self.block_initial_position[0]
        x_move = self.block_initial_position[1]
        # 下移
        y_drop -= 1

        # for 正常结束else里面内容正常执行，for被打断else不执行
        # 遍历选择的元素块的行列，选择一个方块
        for row, column in self.select_block:
            # 将元素块移动到选择的初始位置
            row += y_drop
            column += x_move

            # 碰到元素块或是底部 换一个元素
            if self.background[row][column] == 1:
                # 打断本次的for循环，进入下一次，重新选择
                break
        else:
            # for循环剩下的工作，if不满足for里面的if判断，就执行else
            # 元素块未触底
            # 清空初始化位置
            self.block_initial_position.clear()
            # 进入下一次循环位置更新
            self.block_initial_position.extend([y_drop, x_move])
            return

        # 针对元素块以及到达底部操作
        # break 退出for循环时执行
        # 6.1 把最底层的元素块背景设置为 其他颜色 ，数值0-->1
        # 因为上一步骤中改变了初始位置的值现在需要重新获取
        y_drop, x_move = self.block_initial_position
        for row, column in self.select_block:
            # 把背景置位1 == 底部防止下一个方块穿透
            self.background[row+y_drop][column+x_move] = 1

        # 6.2 判断是否该清空一行
        complete_row = []
        # 6.3在窗口的可视范围内1-20行，判断是否有一行全部占满
        for row in range(1, 21):
            # 6.4判断是否一行中还含有0，没有满了，要消除，反之不消除
            if 0 not in self.background[row]:
                # 6.5把当前行放入complete_row = []，要被消除的行
                complete_row.append(row)

        # 6.6使用列表的pop消除行，消除第一个，有返回值为被消除的值，所以要把列表的值逆序排列
        # 消除最新加入的
        complete_row.sort(reverse=True)

        # 7消除一行或多行
        for row in complete_row:
            self.background.pop(row)  # 消除操作
            self.background.append([0 for _ in range(0, 10)])  # 删除一行补充一个空行

        # 8 得分的变化
        # 8.1消几行，加几行
        self.score[0] += len(complete_row)
        # 8.2 设置标题的得分
        pygame.display.set_caption('得分为：'+str(self.score[0])+'分')

        # 9判断游戏是否结束
        # 9.1 要选择一个新的元素块要删除覆盖旧的元素快
        self.select_block.clear()
        # 9.2 随机下一个元素块
        self.select_block.extend(list(random.choice(self.all_block)))
        # 9.3 规定初始位置
        self.block_initial_position.clear()
        # 9.4 因为要参与判断游戏是否结束，所以要在屏幕内部
        # 掉落的初始位置和，拿到两个数值加入相对位置
        self.block_initial_position.extend([20, 5])
        # 9.5 重新引入初始位置
        y_drop, x_move = self.block_initial_position
        # 9.6 判断是否为最后一行元素
        for row, column in self.select_block:
            # 相对位置转换为实际位置
            # y_drop=row = 20,x_move=column = 5
            row += y_drop
            column += x_move
            # row = 20  column = 5
            # 是否满屏，一列满了,判断20行，（20,5）s是否有元素
            if self.background[row][column]:
                self.gameover.append(1)

    # 10绘制
    def draw_block(self):
        # 重新引入初始位置
        y_drop, x_move = self.block_initial_position
        # 遍历当前选择的元素块
        for row, column in self.select_block:
            row += y_drop
            column += x_move
            # 换算坐标 窗口250*500 -->（10*20） 所以方块25*25
            # row = 20  column = 5
            # 将坐标从下中--->上中， 图像会以x轴进行翻转，不影响
            point = (column * 25, 500 - row * 25)
            # 绘制
            # 参数：绘制位置 color（rgb） (位置,大小)
            pygame.draw.rect(self.screen, (205, 92, 92), (column * 25, 500 - row * 25, 23, 23))

        # 触底的行和列填充颜色
        for row in range(0, 20):
            for column in range(0, 10):
                bottom = self.background[row][column]
                if bottom:
                    # 为底部--1
                    pygame.draw.rect(self.screen, (160, 32, 240), (column * 25, 500 - row * 25, 23, 23))

    # 11移动
    def move_left_right(self,n):
        # n = 1右移 n = -1 左移
        y_drop, x_move = self.block_initial_position
        x_move += n
        for row, column in self.select_block:
            # 移动位置
            row += y_drop
            column += x_move
            # 边界判断 不能<0 or >9 or background[row][column]
            if column < 0 or column > 9 or self.background[row][column]:
                break
        # 正常移动更新坐标
        else:
            self.block_initial_position.clear()
            self.block_initial_position.extend([y_drop,x_move])

    # 12旋转
    def rotate(self):
        # 拿到初始位置
        y_drop, x_move = self.block_initial_position
        # 旋转变化
        # 交换旋转后的点位 重点
        rotate_position =[(-column,row) for row, column in self.select_block]
        for row, column in rotate_position:
            row += y_drop
            column += x_move
            # 边界判断
            if column < 0 or column > 9 or self.background[row][column]:
                break
        else:
            # 更新位置
            self.select_block.clear()
            # 设置旋转后的坐标
            self.select_block.extend(rotate_position)

    # 13设置音效
    # 13.1
    def sound(self):
        # 加载wave文件
        wave_down = pygame.mixer.Sound('resource/sound/click.mp3')
        # 播放音效
        wave_down.set_volume(0.1)
        wave_down.play()

    # 13.2
    def over_game(self):
        # 加载wave文件
        wave_down = pygame.mixer.Sound('resource/sound/gameover.mp3')
        # 播放音效
        wave_down.set_volume(0.2)
        wave_down.play()

    def main(self):
        # 3.有一个窗口一闪而过，之后程序退出
        # 在pygame中要有事件才能正常显示
        # 获取事件-->更新状态-->绘制图像（使用循环一直更新事件状态）
        while True:
            # 4.1将得到的对象设置,要刷新页面
            self.screen.fill(color=(187, 255, 255))

            # 遍历事件循环，捕获事件，判断处理事件
            # 能够拿到键盘和鼠标的操作 pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 当捕获退出键退出
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序
                    sys.exit()
                # 使用esc终止程序
                # 按键类型和esc键 （可以换为其他按键）或是让event.key == 对应数字
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # 11.1 左右移动，捕获左右键
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.move_left_right(-1)
                    self.sound()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.move_left_right(1)
                    self.sound()

                # 12旋转 变化
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.rotate()
                    self.sound()

                # 13按下键加速下落
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.press = True
                    self.sound()

                elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    self.press = False

            # 5.6 方块掉落
            # 10.1创建一个计数变量，每一帧都累加，加到一定数量后，执行掉落函数，执行之后还需将计数变量清零累加

            # 13 加速下落
            if self.press:
                self.speeds += 10

            if self.speeds >= 30:
                self.block_down_move()
                # 重置
                self.speeds = 0
            else:
                self.speeds+= 1

            if self.gameover:
                # 停止游戏 可自行扩充
                # 音乐
                self.over_game()
                pygame.mixer.music.stop()
                time.sleep(2)
                # 显示文字
                self.screen.blit(self.text, (60, 210))
                pygame.display.flip()
                time.sleep(2)
                sys.exit()


            # 绘制
            self.draw_block()
            # 控制游戏的整体帧数
            pygame.time.Clock().tick(100)

            # 4.2重新绘制窗口flip()或updata()
            pygame.display.flip()


if __name__ == '__main__':
    t = Tetrise()
    t.main()



