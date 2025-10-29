# test_cactus_debug.py - 仙人掌排序調試程式
# 詳細檢查排序邏輯是否正常執行

# 回到起始位置
def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 詳細測試排序邏輯
def debug_cactus_sorting():
    print("=== 仙人掌排序調試 ===")
    
    reset_position()
    swap_count = 0
    check_count = 0
    cactus_count = 0
    
    # 遍歷仙人掌區
    for y in range(6, 16):  # 仙人掌區 y 範圍
        for x in range(6, 16):  # 仙人掌區 x 範圍
            # 移動到指定位置
            while get_pos_x() < x:
                move(East)
            while get_pos_x() > x:
                move(West)
            while get_pos_y() < y:
                move(North)
            while get_pos_y() > y:
                move(South)
            
            # 檢查當前位置是否有仙人掌
            if get_entity_type() == Entities.Cactus:
                cactus_count += 1
                current_size = measure()
                
                # 橫向移動：檢查北方仙人掌
                if y < 15:  # 不在最上邊
                    check_count += 1
                    
                    # 使用 measure(North) 測量北方仙人掌大小
                    north_size = measure(North)
                    
                    # 若本體比較大，則使用 swap(North) 交換位置
                    if north_size != None and current_size > north_size:
                        print("位置 (", x, ",", y, ") - 當前:", current_size, "北方:", north_size, "-> 需要交換")
                        swap(North)
                        swap_count += 1
                        
                        # 驗證交換結果
                        new_current = measure()
                        new_north = measure(North)
                        print("  交換後 - 當前:", new_current, "北方:", new_north)
    
    print("")
    print("=== 排序結果 ===")
    print("仙人掌總數:", cactus_count)
    print("檢查次數:", check_count)
    print("交換次數:", swap_count)
    
    return swap_count

# 簡單測試
def simple_test():
    print("=== 簡單測試 ===")
    
    reset_position()
    
    # 移動到仙人掌區中心位置 (10, 10)
    for i in range(10):
        move(East)
    for i in range(10):
        move(North)
    
    print("當前位置: (10, 10)")
    print("當前實體:", get_entity_type())
    
    if get_entity_type() == Entities.Cactus:
        current = measure()
        north = measure(North)
        east = measure(East)
        south = measure(South)
        west = measure(West)
        
        print("當前大小:", current)
        print("北方大小:", north)
        print("東方大小:", east)
        print("南方大小:", south)
        print("西方大小:", west)
        
        # 測試交換
        if north != None and current > north:
            print("")
            print("測試 swap(North)...")
            swap(North)
            print("交換後當前:", measure())
            print("交換後北方:", measure(North))
    else:
        print("位置 (10, 10) 沒有仙人掌")

# 執行測試
print("=== 仙人掌排序調試程式 ===")

# 測試1: 簡單測試
simple_test()

print("")
print("==================================")

# 測試2: 完整排序測試
debug_cactus_sorting()

print("")
print("調試完成！")
