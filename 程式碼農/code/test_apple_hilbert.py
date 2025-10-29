# test_apple_hilbert.py - 希爾伯特曲線路徑

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 簡化版希爾伯特曲線生成器
def generate_path(size):
    # 為了簡化，使用改進的Z字型填充
    # 完整希爾伯特曲線較複雜，這裡用近似方案
    path = []
    
    # 按塊狀填充，避免交叉
    block_size = 4
    
    for block_y in range(0, size, block_size):
        for block_x in range(0, size, block_size):
            # 填充每個 4×4 的塊
            for y in range(block_size):
                for x in range(block_size):
                    if block_y + y < size and block_x + x < size:
                        path.append((block_x + x, block_y + y))
    
    return path

farm_size = get_world_size()
min_cactus_threshold = 100
target_tail_length = (farm_size * farm_size) - 10

# 生成路徑
path_plan = generate_path(farm_size)

while True:
    cactus_available = num_items(Items.Cactus)
    if cactus_available < min_cactus_threshold:
        for wait in range(50):
            do_a_flip()
        continue
    
    current_target = target_tail_length
    if cactus_available < current_target:
        current_target = cactus_available
    
    reset_position()
    change_hat(Hats.Dinosaur_Hat)
    
    apples_eaten = 0
    stuck_count = 0
    
    # 按照預定路徑移動
    for i in range(1, len(path_plan)):
        if apples_eaten >= current_target:
            break
        
        target_x = path_plan[i][0]
        target_y = path_plan[i][1]
        current_x = get_pos_x()
        current_y = get_pos_y()
        
        # 向目標移動
        moved = False
        
        if target_x > current_x:
            result = move(East)
            moved = result
        elif target_x < current_x:
            result = move(West)
            moved = result
        elif target_y > current_y:
            result = move(North)
            moved = result
        elif target_y < current_y:
            result = move(South)
            moved = result
        
        if moved:
            apples_eaten += 1
            stuck_count = 0
        else:
            stuck_count += 1
            if stuck_count >= 200:
                break
    
    change_hat(Hats.Brown_Hat)
    do_a_flip()

# 塊狀填充路徑：
# - 避免長距離跨越
# - 尾巴不會阻擋路徑
# - 更穩定的移動模式
