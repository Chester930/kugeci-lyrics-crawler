# strategy_harvest_optimized.py - 優化雜草採收策略
# 智能檢測 + 縱向S型 + 橫向S型交互採收

# 策略參數
farm_size = get_world_size()
harvest_count = 0
round_count = 0

# 回到起始位置
def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 檢查農場是否有可收穫的雜草
def check_harvestable():
    reset_position()
    for x in range(farm_size):
        for y in range(farm_size):
            if can_harvest():
                return True
            if y < farm_size - 1:
                move(North)
        if x < farm_size - 1:
            move(East)
            while get_pos_y() > 0:
                move(South)
    return False

# 縱向S型採收
def harvest_vertical_s():
    local_harvests = 0
    for x in range(farm_size):
        for y in range(farm_size):
            if can_harvest():
                harvest()
                local_harvests += 1
            if y < farm_size - 1:
                if x % 2 == 0:
                    move(North)  # 偶數列：從下到上
                else:
                    move(South)  # 奇數列：從上到下
        if x < farm_size - 1:
            move(East)
            # 根據下一列的奇偶性調整位置
            if (x + 1) % 2 == 0:
                # 下一列是偶數列，需要回到底部
                while get_pos_y() > 0:
                    move(South)
            else:
                # 下一列是奇數列，需要回到頂部
                while get_pos_y() < farm_size - 1:
                    move(North)
    return local_harvests

# 橫向S型採收
def harvest_horizontal_s():
    local_harvests = 0
    for y in range(farm_size):
        for x in range(farm_size):
            if can_harvest():
                harvest()
                local_harvests += 1
            if x < farm_size - 1:
                if y % 2 == 0:
                    move(East)
                else:
                    move(West)
        if y < farm_size - 1:
            move(North)
    return local_harvests

# 主策略執行
reset_position()

# 主採收循環
while True:
    round_count += 1
    
    # 檢查是否有可收穫的雜草
    if not check_harvestable():
        for i in range(5):  # 等待5秒
            do_a_flip()
        continue
    
    # 縱向S型採收
    vertical_harvests = harvest_vertical_s()
    harvest_count += vertical_harvests
    
    reset_position()
    
    # 橫向S型採收
    horizontal_harvests = harvest_horizontal_s()
    harvest_count += horizontal_harvests
    
    reset_position()
    
    # 如果本輪沒有收穫，等待更長時間
    if vertical_harvests + horizontal_harvests == 0:
        for i in range(10):  # 等待10秒
            do_a_flip()
