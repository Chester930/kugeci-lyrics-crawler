# test_cactus_swap.py - 測試仙人掌交換功能
# 檢查 swap() 和 measure(direction) 是否正常工作

# 回到起始位置
def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 測試仙人掌交換功能
def test_cactus_swap():
    print("=== 仙人掌交換測試 ===")
    
    reset_position()
    
    # 移動到仙人掌區 (6, 6)
    for i in range(6):
        move(East)
    for i in range(6):
        move(North)
    
    print("當前位置:", get_pos_x(), get_pos_y())
    
    # 檢查當前位置是否有仙人掌
    current_entity = get_entity_type()
    print("當前實體:", current_entity)
    
    if current_entity == Entities.Cactus:
        # 測量當前仙人掌大小
        current_size = measure()
        print("當前仙人掌大小:", current_size)
        
        # 測量北方仙人掌大小
        north_size = measure(North)
        print("北方仙人掌大小:", north_size)
        
        # 測量東方仙人掌大小
        east_size = measure(East)
        print("東方仙人掌大小:", east_size)
        
        # 測量南方仙人掌大小
        south_size = measure(South)
        print("南方仙人掌大小:", south_size)
        
        # 測量西方仙人掌大小
        west_size = measure(West)
        print("西方仙人掌大小:", west_size)
        
        # 嘗試交換北方仙人掌
        if north_size != None:
            print("")
            print("嘗試與北方仙人掌交換...")
            print("交換前 - 當前:", current_size, "北方:", north_size)
            
            if current_size > north_size:
                swap(North)
                print("執行 swap(North)")
                
                # 檢查交換後的結果
                new_current_size = measure()
                new_north_size = measure(North)
                print("交換後 - 當前:", new_current_size, "北方:", new_north_size)
                
                if new_current_size == north_size and new_north_size == current_size:
                    print("✓ 交換成功！")
                else:
                    print("✗ 交換失敗或未發生")
            else:
                print("當前仙人掌不大於北方，不需要交換")
        else:
            print("北方沒有仙人掌")
    else:
        print("當前位置沒有仙人掌")
        print("請先在仙人掌區種植仙人掌")

# 測試仙人掌區遍歷
def test_cactus_zone_scan():
    print("")
    print("=== 仙人掌區掃描測試 ===")
    
    reset_position()
    cactus_count = 0
    cactus_info = []
    
    # 掃描仙人掌區 (6, 6) 到 (15, 15)
    for x in range(6, 16):
        for y in range(6, 16):
            # 移動到指定位置
            while get_pos_x() < x:
                move(East)
            while get_pos_x() > x:
                move(West)
            while get_pos_y() < y:
                move(North)
            while get_pos_y() > y:
                move(South)
            
            # 檢查當前位置
            if get_entity_type() == Entities.Cactus:
                cactus_count += 1
                size = measure()
                cactus_info.append((x, y, size))
    
    print("仙人掌區總共有", cactus_count, "個仙人掌")
    
    if cactus_count > 0:
        print("")
        print("前10個仙人掌資訊:")
        count = 0
        for info in cactus_info:
            if count >= 10:
                break
            x, y, size = info
            print("  位置 (", x, ",", y, ") 大小:", size)
            count += 1
    else:
        print("仙人掌區沒有仙人掌，請先種植")
    
    return cactus_count

# 執行測試
print("=== 仙人掌交換功能測試程式 ===")

# 測試1: 掃描仙人掌區
cactus_count = test_cactus_zone_scan()

# 測試2: 測試交換功能
if cactus_count > 0:
    test_cactus_swap()
else:
    print("")
    print("請先在仙人掌區種植仙人掌後再測試交換功能")

print("")
print("測試完成！")
