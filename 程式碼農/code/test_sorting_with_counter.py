# test_sorting_with_counter.py - 帶計數器的排序測試

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 排序執行計數測試 ===")
print("")

# 測試3輪，看看每輪的執行情況
for test_round in range(1, 4):
    print("--- 第", test_round, "輪測試 ---")
    
    reset_position()
    
    visited_count = 0  # 訪問的格子數
    cactus_count = 0   # 找到的仙人掌數
    check_count = 0    # 檢查比較的次數
    swap_count = 0     # 交換次數
    
    # 執行排序邏輯
    if test_round % 2 == 0:
        print("執行：橫向排序 (檢查北方)")
        for x in range(6, 16):
            for y in range(6, 16):
                visited_count += 1
                
                # 移動到指定位置
                while get_pos_x() < x:
                    move(East)
                while get_pos_x() > x:
                    move(West)
                while get_pos_y() < y:
                    move(North)
                while get_pos_y() > y:
                    move(South)
                
                # 檢查是否有仙人掌
                if get_entity_type() == Entities.Cactus:
                    cactus_count += 1
                    current_size = measure()
                    
                    if y < 15:
                        check_count += 1
                        north_size = measure(North)
                        
                        if north_size != None and current_size > north_size:
                            swap(North)
                            swap_count += 1
    else:
        print("執行：縱向排序 (檢查東方)")
        for y in range(6, 16):
            for x in range(6, 16):
                visited_count += 1
                
                # 移動到指定位置
                while get_pos_x() < x:
                    move(East)
                while get_pos_x() > x:
                    move(West)
                while get_pos_y() < y:
                    move(North)
                while get_pos_y() > y:
                    move(South)
                
                # 檢查是否有仙人掌
                if get_entity_type() == Entities.Cactus:
                    cactus_count += 1
                    current_size = measure()
                    
                    if x < 15:
                        check_count += 1
                        east_size = measure(East)
                        
                        if east_size != None and current_size > east_size:
                            swap(East)
                            swap_count += 1
    
    # 報告結果
    print("  訪問格子數:", visited_count)
    print("  找到仙人掌數:", cactus_count)
    print("  執行檢查次數:", check_count)
    print("  執行交換次數:", swap_count)
    print("")
    
    # 等待一下
    for i in range(5):
        do_a_flip()

print("=== 測試完成 ===")
print("")
print("如果:")
print("- 訪問格子數 = 100: 排序函數正常遍歷")
print("- 找到仙人掌數 > 0: 仙人掌已種植")
print("- 執行檢查次數 > 0: 仙人掌已成熟")
print("- 執行交換次數 > 0: 確實需要排序")
print("")
print("如果交換次數 = 0，可能原因:")
print("1. 仙人掌已經排序完成")
print("2. 所有仙人掌大小相同")
print("3. measure() 返回 None")
