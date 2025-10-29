# 南瓜尺寸檢查測試程式
# 指定位置檢查南瓜尺寸

# ===== 請在這裡填寫要檢查的位置 =====
test_x = 0  # 請填入X座標
test_y = 0  # 請填入Y座標
# ======================================

# 初始化變數
farm_size = get_world_size()

# 移動到指定位置
def move_to_position(x, y):
    # 重置到原點
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)
    
    # 移動到指定X位置
    for i in range(x):
        move(East)
    
    # 移動到指定Y位置
    for i in range(y):
        move(North)

# 檢查指定位置的南瓜尺寸
def check_pumpkin_at_position(x, y):
    move_to_position(x, y)
    
    # 檢查當前位置是否有南瓜
    if get_entity_type() == Entities.Pumpkin:
        if can_harvest():
            # 使用 measure() 取得南瓜尺寸
            pumpkin_size = measure()
            print(str(pumpkin_size))
        else:
            print("南瓜未成熟")
    else:
        print("該位置沒有南瓜")

# 主測試循環 - 檢查指定位置
while True:
    # 檢查指定位置的南瓜尺寸
    check_pumpkin_at_position(test_x, test_y)
    
    # 等待一段時間
    for i in range(50):
        do_a_flip()
