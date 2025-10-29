# dinosaur_apple_spawn_test.py - 直接執行除草並翻土

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 檢查當前農場狀態
farm_size = get_world_size()
reset_position()

# 統計並執行除草翻土
grass_cleared = 0
land_tilled = 0

# 遍歷農場，清除草並翻土
for x in range(farm_size):
    for y in range(farm_size):
        # 移動到位置
        while get_pos_x() < x:
            move(East)
        while get_pos_x() > x:
            move(West)
        while get_pos_y() < y:
            move(North)
        while get_pos_y() > y:
            move(South)
        
        # 檢查並處理草地
        entity = get_entity_type()
        ground = get_ground_type()
        
        if ground == Grounds.Grassland:
            # 如果有草，收割
            if entity == Entities.Grass:
                harvest()
                grass_cleared += 1
            # 翻土，防止草再長
            till()
            land_tilled += 1
    
    # 移動到下一行
    if x < farm_size - 1:
        move(East)
        while get_pos_y() > 0:
            move(South)

reset_position()

# 顯示結果（使用 quick() 函數，因為遊戲沒有終端）
# 清除的草數量會顯示在背包中
# 翻土的數量可以從土地變化看出
