# test_dinosaur.py - 恐龍帽子功能測試程式
# 測試恐龍帽子的基本功能：裝備、吃蘋果、尾巴增長、骨頭收穫

# 測試參數
test_farm_size = 10  # 使用較小的農場進行測試
max_apples = 20  # 最多吃20個蘋果
test_mode = "basic"  # 測試模式：basic, advanced, full

# 設定農場大小
set_world_size(test_farm_size)

# 回到起始位置
def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 檢查是否可以移動
def can_move_direction(direction):
    current_x = get_pos_x()
    current_y = get_pos_y()
    
    # 嘗試移動
    if direction == North:
        move(North)
        if get_pos_y() > current_y:
            move(South)  # 回到原位置
            return True
    elif direction == South:
        move(South)
        if get_pos_y() < current_y:
            move(North)  # 回到原位置
            return True
    elif direction == East:
        move(East)
        if get_pos_x() > current_x:
            move(West)  # 回到原位置
            return True
    elif direction == West:
        move(West)
        if get_pos_x() < current_x:
            move(East)  # 回到原位置
            return True
    
    return False

# 基本測試：裝備帽子、吃蘋果、收穫骨頭
def basic_dinosaur_test():
    print("=== 基本恐龍測試 ===")
    
    # 1. 裝備恐龍帽子
    print("1. 裝備恐龍帽子...")
    change_hat(Hats.Dinosaur_Hat)
    print("   恐龍帽子已裝備")
    
    # 2. 檢查初始狀態
    print("2. 檢查初始狀態...")
    print("   當前位置:", get_pos_x(), get_pos_y())
    print("   農場大小:", test_farm_size, "x", test_farm_size)
    
    # 3. 移動吃蘋果
    print("3. 開始移動吃蘋果...")
    apple_count = 0
    moves = 0
    
    # 簡單的S型移動
    for x in range(test_farm_size):
        for y in range(test_farm_size):
            # 檢查是否有蘋果
            if get_entity_type() == Entities.Apple:
                print("   找到蘋果在位置:", get_pos_x(), get_pos_y())
                apple_count += 1
            
            # 移動到下一個位置
            if y < test_farm_size - 1:
                if x % 2 == 0:
                    move(North)
                else:
                    move(South)
                moves += 1
                
                # 檢查是否吃到蘋果
                if get_entity_type() == Entities.Apple:
                    print("   吃到蘋果！尾巴長度:", apple_count + 1)
                    apple_count += 1
            
        if x < test_farm_size - 1:
            move(East)
            moves += 1
    
    print("4. 移動完成")
    print("   總移動次數:", moves)
    print("   吃到的蘋果數:", apple_count)
    
    # 5. 脫下帽子收穫骨頭
    print("5. 脫下帽子收穫骨頭...")
    change_hat(Hats.Normal_Hat)
    
    # 檢查骨頭數量
    bones = num_items(Items.Bone)
    print("   獲得骨頭數量:", bones)
    print("   預期骨頭數量:", apple_count ** 2)
    
    return apple_count, bones

# 進階測試：查詢蘋果位置
def advanced_dinosaur_test():
    print("\n=== 進階恐龍測試 ===")
    
    # 1. 裝備恐龍帽子
    change_hat(Hats.Dinosaur_Hat)
    print("1. 恐龍帽子已裝備")
    
    # 2. 查詢蘋果位置
    print("2. 查詢蘋果位置...")
    if get_entity_type() == Entities.Apple:
        next_x, next_y = measure()
        print("   下一個蘋果位置:", next_x, next_y)
    else:
        print("   當前位置沒有蘋果")
    
    # 3. 移動到蘋果位置
    print("3. 移動到蘋果位置...")
    if get_entity_type() == Entities.Apple:
        # 移動到下一個位置
        move(East)
        print("   移動後位置:", get_pos_x(), get_pos_y())
    
    # 4. 脫下帽子
    change_hat(Hats.Normal_Hat)
    print("4. 測試完成")

# 完整測試：覆蓋整個農場
def full_dinosaur_test():
    print("\n=== 完整恐龍測試 ===")
    
    # 1. 裝備恐龍帽子
    change_hat(Hats.Dinosaur_Hat)
    print("1. 恐龍帽子已裝備")
    
    # 2. 覆蓋整個農場的S型移動
    print("2. 開始覆蓋整個農場...")
    apple_count = 0
    moves = 0
    
    # 重置位置
    reset_position()
    
    # S型移動覆蓋整個農場
    for x in range(test_farm_size):
        for y in range(test_farm_size):
            # 檢查是否可以移動
            if not can_move_direction(North if x % 2 == 0 else South):
                print("   無法移動，尾巴可能已佔滿農場")
                break
            
            # 移動
            if y < test_farm_size - 1:
                if x % 2 == 0:
                    move(North)
                else:
                    move(South)
                moves += 1
                
                # 檢查是否吃到蘋果
                if get_entity_type() == Entities.Apple:
                    apple_count += 1
                    print("   吃到蘋果！當前尾巴長度:", apple_count)
            
        if x < test_farm_size - 1:
            move(East)
            moves += 1
    
    print("3. 移動完成")
    print("   總移動次數:", moves)
    print("   吃到的蘋果數:", apple_count)
    
    # 4. 脫下帽子收穫骨頭
    change_hat(Hats.Normal_Hat)
    bones = num_items(Items.Bone)
    print("4. 獲得骨頭數量:", bones)
    
    return apple_count, bones

# 主測試程式
def main():
    print("🦕 恐龍帽子功能測試程式")
    print("=" * 50)
    
    # 重置位置
    reset_position()
    
    # 根據測試模式執行不同測試
    if test_mode == "basic":
        apple_count, bones = basic_dinosaur_test()
    elif test_mode == "advanced":
        advanced_dinosaur_test()
    elif test_mode == "full":
        apple_count, bones = full_dinosaur_test()
    
    print("\n=== 測試結果 ===")
    print("測試模式:", test_mode)
    print("農場大小:", test_farm_size, "x", test_farm_size)
    if 'apple_count' in locals():
        print("吃到的蘋果數:", apple_count)
        print("獲得骨頭數:", bones)
        print("骨頭效率:", bones / apple_count if apple_count > 0 else 0)
    
    print("\n測試完成！")

# 執行測試
main()
