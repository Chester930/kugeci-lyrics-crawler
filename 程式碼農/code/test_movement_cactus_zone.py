# test_movement_cactus_zone.py - 測試無人機能否進入仙人掌區

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 測試無人機進入仙人掌區 ===")
print("")

reset_position()

# 仙人掌區定義：x: 6-15, y: 6-15
cactus_zone_visited = 0
cactus_found = 0
move_failed = 0

print("開始遍歷農場，檢查是否能進入仙人掌區...")
print("")

# 使用簡單的縱向S型移動
farm_size = get_world_size()

for x in range(farm_size):
    for y in range(farm_size):
        # 檢查當前位置
        current_x = get_pos_x()
        current_y = get_pos_y()
        
        # 如果在仙人掌區
        if 6 <= current_x <= 15 and 6 <= current_y <= 15:
            cactus_zone_visited += 1
            entity = get_entity_type()
            
            if entity == Entities.Cactus:
                cactus_found += 1
                # 每10個仙人掌報告一次
                if cactus_found % 10 == 0:
                    print("找到第", cactus_found, "個仙人掌，位置: (", current_x, ",", current_y, ")")
        
        # 嘗試移動
        if y < farm_size - 1:
            result = move(North)
            if not result:
                move_failed += 1
                print("移動失敗！位置: (", current_x, ",", current_y, ")")
    
    if x < farm_size - 1:
        move(East)
        # 回到下方
        while get_pos_y() > 0:
            move(South)

print("")
print("=== 測試結果 ===")
print("農場大小:", farm_size)
print("進入仙人掌區次數:", cactus_zone_visited)
print("找到仙人掌數量:", cactus_found)
print("移動失敗次數:", move_failed)
print("")

if cactus_zone_visited == 0:
    print("問題：無人機完全沒有進入仙人掌區！")
    print("可能原因：仙人掌區定義或移動邏輯有問題")
elif cactus_found == 0:
    print("無人機進入了仙人掌區，但沒有找到仙人掌")
    print("可能原因：仙人掌還未種植")
else:
    print("無人機成功進入仙人掌區並找到仙人掌！")
    print("預期可以進行排序操作")

print("")
print("測試完成！")
