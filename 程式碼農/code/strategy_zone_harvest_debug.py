# strategy_zone_harvest_debug.py - 帶調試輸出的版本
# 只保留核心邏輯和排序功能，添加調試信息

farm_size = 22
round_count = 0

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

def safe_cactus_sorting_horizontal():
    reset_position()
    swap_count = 0
    cactus_count = 0
    
    for x in range(6, 16):
        for y in range(6, 16):
            while get_pos_x() < x:
                move(East)
            while get_pos_x() > x:
                move(West)
            while get_pos_y() < y:
                move(North)
            while get_pos_y() > y:
                move(South)
            
            if get_entity_type() == Entities.Cactus:
                cactus_count += 1
                current_size = measure()
                
                if y < 15:
                    north_size = measure(North)
                    if north_size != None and current_size > north_size:
                        swap(North)
                        swap_count += 1
    
    return swap_count

def safe_cactus_sorting_vertical():
    reset_position()
    swap_count = 0
    cactus_count = 0
    
    for y in range(6, 16):
        for x in range(6, 16):
            while get_pos_x() < x:
                move(East)
            while get_pos_x() > x:
                move(West)
            while get_pos_y() < y:
                move(North)
            while get_pos_y() > y:
                move(South)
            
            if get_entity_type() == Entities.Cactus:
                cactus_count += 1
                current_size = measure()
                
                if x < 15:
                    east_size = measure(East)
                    if east_size != None and current_size > east_size:
                        swap(East)
                        swap_count += 1
    
    return swap_count

# 簡化的主循環
reset_position()

while True:
    round_count += 1
    
    # 每10輪執行一次排序
    if round_count % 10 == 0:
        if round_count % 20 == 0:
            swap_count = safe_cactus_sorting_horizontal()
        else:
            swap_count = safe_cactus_sorting_vertical()
        
        reset_position()
    
    # 簡單等待
    for i in range(10):
        do_a_flip()
    
    # 每10輪重置
    if round_count % 10 == 0:
        round_count = 0

