# test_dinosaur_with_plants.py - 測試有植物時恐龍模式是否能運作

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 測試恐龍模式空間需求 ===")
print("")

# 檢查當前農場狀態
farm_size = get_world_size()
print("農場大小:", farm_size)
print("")

# 統計當前植物數量
reset_position()
plant_count = 0
empty_count = 0
grass_count = 0

print("掃描農場狀態...")
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
        
        # 檢查狀態
        entity = get_entity_type()
        ground = get_ground_type()
        
        if entity == Entities.Grass:
            grass_count += 1
            plant_count += 1
        elif entity != None:
            plant_count += 1
        else:
            # 檢查是草地還是土地
            if ground == Grounds.Soil:
                empty_count += 1
            else:
                # 草地但沒長草，算作可用空間
                empty_count += 1

reset_position()

total_tiles = farm_size * farm_size
print("")
print("=== 農場現況 ===")
print("總格子數:", total_tiles)
print("有植物:", plant_count, "格")
print("  - 其中草:", grass_count, "格")
print("空地:", empty_count, "格")
print("空地比例:", (empty_count * 100) / total_tiles, "%")
print("")

# 提示是否需要除草
if grass_count > 0:
    print("警告：發現", grass_count, "格草地")
    print("建議：執行恐龍模式前先除草並翻地")
    print("")

# 建議
print("=== 空間評估 ===")
print("")

# 計算建議的尾巴長度
if empty_count >= 200:
    recommended = 200
    print("空地充足，建議尾巴長度: 200")
    print("預期收益: 40,000 骨頭")
elif empty_count >= 150:
    recommended = 150
    print("空地適中，建議尾巴長度: 150")
    print("預期收益: 22,500 骨頭")
elif empty_count >= 100:
    recommended = 100
    print("空地有限，建議尾巴長度: 100")
    print("預期收益: 10,000 骨頭")
elif empty_count >= 50:
    recommended = 50
    print("空地較少，建議尾巴長度: 50")
    print("預期收益: 2,500 骨頭")
else:
    recommended = empty_count / 2
    print("警告：空地不足，建議尾巴長度:", recommended)
    print("預期收益:", recommended * recommended, "骨頭")
    print("")
    print("建議：先清空部分區域再執行恐龍模式")

print("")
print("=== 測試建議 ===")
print("")

if empty_count >= 100:
    print("可以安全執行恐龍模式")
    print("建議設定: dinosaur_target_tail_length =", recommended)
else:
    print("空地不足，恐龍模式可能受限")
    print("建議：")
    print("1. 先清空部分區域")
    print("2. 或降低目標長度")
    print("3. 或等待更好的時機")

print("")
print("測試完成！")
