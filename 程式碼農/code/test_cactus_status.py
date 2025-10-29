# test_cactus_status.py - 檢查仙人掌狀態
# 查看仙人掌是否存在、是否成熟、大小分布

# 回到起始位置
def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 仙人掌狀態檢查 ===")

reset_position()

# 檢查仙人掌區狀態
cactus_data = []
entity_counts = {}

print("掃描仙人掌區 (6,6) 到 (15,15)...")

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
        entity = get_entity_type()
        ground = get_ground_type()
        
        # 統計實體類型
        if entity == None:
            entity_name = "空地"
        elif entity == Entities.Cactus:
            entity_name = "仙人掌"
            size = measure()
            can_harv = can_harvest()
            cactus_data.append((x, y, size, can_harv))
        elif entity == Entities.Grass:
            entity_name = "雜草"
        else:
            entity_name = "其他"
        
        if entity_name in entity_counts:
            entity_counts[entity_name] += 1
        else:
            entity_counts[entity_name] = 1

# 顯示統計結果
print("")
print("=== 仙人掌區統計 ===")
print("總格數: 100")
for name in entity_counts:
    count = entity_counts[name]
    print(name, ":", count, "個")

# 顯示仙人掌詳細資訊
if len(cactus_data) > 0:
    print("")
    print("=== 仙人掌詳細資訊 ===")
    print("總共", len(cactus_data), "個仙人掌")
    
    # 統計成熟數量
    mature_count = 0
    for data in cactus_data:
        x, y, size, can_harv = data
        if can_harv:
            mature_count += 1
    
    print("成熟仙人掌:", mature_count, "個")
    print("未成熟仙人掌:", len(cactus_data) - mature_count, "個")
    
    # 統計大小分布
    print("")
    print("=== 仙人掌大小分布 ===")
    size_counts = {}
    for data in cactus_data:
        x, y, size, can_harv = data
        if size in size_counts:
            size_counts[size] += 1
        else:
            size_counts[size] = 1
    
    for size in range(10):
        if size in size_counts:
            count = size_counts[size]
            print("大小", size, ":", count, "個")
    
    # 檢查是否需要排序
    print("")
    print("=== 排序需求檢查 ===")
    need_swap_count = 0
    
    for data in cactus_data:
        x, y, size, can_harv = data
        if y < 15:
            # 移動到該位置
            while get_pos_x() < x:
                move(East)
            while get_pos_x() > x:
                move(West)
            while get_pos_y() < y:
                move(North)
            while get_pos_y() > y:
                move(South)
            
            # 檢查北方
            north_size = measure(North)
            if north_size != None and size > north_size:
                need_swap_count += 1
                if need_swap_count <= 3:
                    print("位置 (", x, ",", y, ") 大小", size, "北方", north_size, "需要交換")
    
    print("需要交換的仙人掌數量:", need_swap_count)
    
    if need_swap_count == 0:
        print("所有仙人掌已經排序完成！")
    else:
        print("建議執行排序程式")
else:
    print("")
    print("仙人掌區沒有仙人掌")
    print("請先運行主策略程式種植仙人掌")

print("")
print("檢查完成！")
