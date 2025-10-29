# test_dinosaur_simple.py - 簡化恐龍帽子測試程式
# 測試恐龍帽子的基本功能

# 設定農場大小為10x10
set_world_size(10)

# 回到起始位置
def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 基本恐龍測試
def test_dinosaur():
    print("🦕 開始恐龍帽子測試")
    
    # 1. 裝備恐龍帽子
    print("1. 裝備恐龍帽子...")
    change_hat(Hats.Dinosaur_Hat)
    
    # 2. 檢查初始狀態
    print("2. 當前位置:", get_pos_x(), get_pos_y())
    
    # 3. 簡單移動測試
    print("3. 開始移動測試...")
    apple_count = 0
    
    # 移動5步測試
    for i in range(5):
        print("   移動", i+1, "步")
        move(East)
        
        # 檢查是否吃到蘋果
        if get_entity_type() == Entities.Apple:
            print("   吃到蘋果！")
            apple_count += 1
    
    print("4. 移動完成，吃到蘋果數:", apple_count)
    
    # 5. 脫下帽子收穫骨頭
    print("5. 脫下帽子收穫骨頭...")
    change_hat(Hats.Normal_Hat)
    
    # 檢查骨頭數量
    bones = num_items(Items.Bone)
    print("   獲得骨頭數量:", bones)
    
    return apple_count, bones

# 執行測試
reset_position()
apple_count, bones = test_dinosaur()

print("\n=== 測試結果 ===")
print("吃到的蘋果數:", apple_count)
print("獲得骨頭數:", bones)
print("測試完成！")
