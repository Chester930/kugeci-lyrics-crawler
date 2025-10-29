# test_apple_smart.py - 智能移動，最大化蘋果收集

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 嘗試向指定方向移動，如果失敗則嘗試其他方向
def smart_move(preferred_direction):
    # 先嘗試首選方向
    if move(preferred_direction):
        return True
    
    # 首選方向失敗，嘗試其他三個方向
    directions = [North, South, East, West]
    directions.remove(preferred_direction)
    
    for direction in directions:
        if move(direction):
            return True
    
    # 所有方向都失敗
    return False

farm_size = get_world_size()

# 目標：盡可能長的尾巴
target_tail_length = 400  # 激進目標

# 檢查仙人掌
if num_items(Items.Cactus) < target_tail_length:
    target_tail_length = num_items(Items.Cactus)

reset_position()

# 裝備恐龍帽
change_hat(Hats.Dinosaur_Hat)

# 智能移動收集蘋果
apples_eaten = 0
completely_stuck = False

# 使用螺旋或填充式移動，而不是固定的S型
# 策略：優先向上/向右移動，填滿整個農場

x = 0
y = 0

while apples_eaten < target_tail_length and not completely_stuck:
    # 決定首選移動方向
    # 策略：螺旋式從內向外
    
    # 如果在底部，優先向上
    if y < farm_size // 2:
        preferred = North
    # 如果在頂部，優先向右或向下
    elif x < farm_size - 1:
        preferred = East
    else:
        preferred = South
    
    # 嘗試智能移動
    result = smart_move(preferred)
    
    if result:
        # 移動成功
        apples_eaten += 1
        x = get_pos_x()
        y = get_pos_y()
    else:
        # 完全被困住
        completely_stuck = True
        break

# 卸下恐龍帽
change_hat(Hats.Brown_Hat)

# 實際收集：apples_eaten 個
# 獲得骨頭：apples_eaten² 個
# 例如收集 350 個 → 350² = 122,500 骨頭
