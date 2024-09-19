import pandas as pd
import requests
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import pygame
import time
import random

# Step 1: 抓取网页内容
url = "https://www.hko.gov.hk/tide/WAGtextPH2025.htm"
response = requests.get(url)

# 检查是否成功获取网页内容
if response.ok:
    tables = pd.read_html(response.text)
    df = tables[0]
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    exit()

# Step 2: 清理数据
df.columns = ['Date MM', 'Date DD', 'Unused', 'Hour 01', 'Hour 02', 'Hour 03', 'Hour 04', 'Hour 05', 'Hour 06',
              'Hour 07', 'Hour 08', 'Hour 09', 'Hour 10', 'Hour 11', 'Hour 12', 'Hour 13', 'Hour 14', 'Hour 15',
              'Hour 16', 'Hour 17', 'Hour 18', 'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24']

df['Date'] = df['Date MM'].astype(str) + '-' + df['Date DD'].astype(str)
df_cleaned = df.drop(columns=['Date MM', 'Date DD', 'Unused'])

# 音频参数
duration = 1000  # 每个音符的持续时间（毫秒）


# 创建音频生成器
def generate_tone(frequency, duration):
    sine_wave = Sine(frequency)
    audio_segment = sine_wave.to_audio_segment(duration=duration, volume=-20)  # 调整音量以变得更柔和
    return audio_segment


# 生成音频文件
def generate_audio(df_cleaned):
    combined = AudioSegment.silent(duration=0)

    # 遍历每一行数据
    for _, row in df_cleaned.iterrows():
        tide_heights = row[1:-1]

        for i, height in enumerate(tide_heights):
            if not np.isnan(height):
                frequency = 440 + height * 50  # 基于潮汐高度的频率
                tone = generate_tone(frequency, duration)
                combined += tone  # 追加到音频中

    # 保存音频文件
    combined.export("generated_tide_audio.wav", format="wav")


# 生成音频文件
generate_audio(df_cleaned)

# 播放音频
pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound("generated_tide_audio.wav")
sound.play()

# 创建一个简单的粒子系统
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tidal Data Visualization")

black = (0, 0, 0)

# 定义莫兰迪色系
def get_random_color():
    return (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))

class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.lifespan = 100
        self.color = get_random_color()  # 生成随机颜色
        self.vertical_movement = random.uniform(-10, 10)  # 随机上下波动

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

    def update(self):
        self.y += self.vertical_movement  # 更新上下位置
        if self.y < 0 or self.y > screen_height:
            self.vertical_movement = -self.vertical_movement  # 遇到边界时反弹
        return True


particles = []

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清空屏幕
    screen.fill(black)

    # 添加粒子
    tide_data_length = len(df_cleaned)
    for current_row in range(tide_data_length):
        tide_heights = df_cleaned.iloc[current_row, 1:-1]

        for i, height in enumerate(tide_heights):
            if not np.isnan(height):
                x = (i + 1) * (screen_width / len(tide_heights))
                y = screen_height - height * 100
                size = height * 5  # 增加粒子大小
                particles.append(Particle(x, y, size))

        # 处理所有粒子
        particles = [particle for particle in particles if particle.update()]
        for particle in particles:
            particle.draw()

        pygame.display.flip()
        pygame.time.wait(100)  # 减少暂停时间以使动画更流畅

pygame.quit()