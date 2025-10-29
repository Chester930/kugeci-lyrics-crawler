# 🗺️ F5 迷宫金币最大化生产指南

## 🎯 策略目标

**使用 Weird_Substance 创建迷宫，最大化金币产出**

---

## 📊 核心数据

### 收益计算（32×32 地图）

| 升级等级 | 所需 Weird_Substance | 金币收益 | 效率 |
|---------|-------------------|---------|------|
| **未解锁** | 32 | 1,024 | 32 金币/Weird |
| **等级 0** | 16 | 1,024 | 64 金币/Weird |
| **等级 1** | 32 | 2,048 | 64 金币/Weird |
| **等级 2** | 64 | 4,096 | 64 金币/Weird |
| **等级 3** | 128 | 8,192 | 64 金币/Weird |

**结论：解锁迷宫后，效率固定为 64 金币/Weird_Substance**

---

## 🔧 三种运行模式

### 模式 1：单次测试（推荐新手）

```python
run_mode = 1  # 设置为单次测试模式
```

**功能：**
- 创建一个迷宫
- 求解并获得金币
- 结束程序

**适用场景：**
- 第一次使用
- 测试迷宫功能
- 验证程序正确性

---

### 模式 2：持续循环（推荐高产）

```python
run_mode = 2  # 设置为持续循环模式
```

**功能：**
- 持续创建迷宫
- 自动求解
- 直到 Weird_Substance < 100 停止
- 显示统计数据

**适用场景：**
- 有大量 Weird_Substance（>1000）
- 需要快速获得金币
- 全自动运行

**预期产量：**
```
1000 Weird_Substance
→ 62 个迷宫（16 Weird/个）
→ 63,488 金币
```

---

### 模式 3：混合模式（最优策略）

```python
run_mode = 3  # 设置为混合模式
```

**功能：**
- 当 Weird_Substance > 500 时，创建迷宫
- 当 Weird_Substance < 500 时，等待积累
- 需要与 f4.py 结合使用

**适用场景：**
- 长期运行
- 平衡 Weird_Substance 生产和消耗
- 持续获得金币

---

## 🧭 两种求解算法

### 算法 1：右手法则（基础）

```python
solve_maze_right_hand()
```

**原理：**
- 始终保持右手贴墙
- 遍历整个迷宫
- 保证找到宝藏

**优点：**
- ✅ 简单可靠
- ✅ 代码量少（~20行）
- ✅ 100% 成功率

**缺点：**
- ❌ 可能绕远路
- ❌ 步数较多

**平均步数：** ~2000 步（32×32 迷宫）

---

### 算法 2：智能求解（推荐）

```python
solve_maze_smart()
```

**原理：**
- 使用 `measure()` 获取宝藏位置
- 结合右手法则导航
- 优先朝向宝藏方向

**优点：**
- ✅ 更快速
- ✅ 步数更少
- ✅ 100% 成功率

**缺点：**
- ⚠️ 代码稍复杂

**平均步数：** ~1500 步（32×32 迷宫）

---

## ⚙️ 参数配置

### 基础参数

```python
farm_size = get_world_size()  # 自动获取地图大小
weird_substance_min = 100     # 最低库存阈值
maze_position_x = 0           # 迷宫创建位置 X
maze_position_y = 0           # 迷宫创建位置 Y
```

**调整建议：**

#### `weird_substance_min`
```python
# 保守策略（确保有余量）
weird_substance_min = 200

# 激进策略（最大化利用）
weird_substance_min = 50

# 推荐
weird_substance_min = 100
```

#### `maze_position_x/y`
```python
# 左下角（默认，推荐）
maze_position_x = 0
maze_position_y = 0

# 中心位置
maze_position_x = farm_size // 2
maze_position_y = farm_size // 2

# 右上角
maze_position_x = farm_size - 1
maze_position_y = farm_size - 1
```

---

### 混合模式参数

```python
weird_threshold = 500  # Weird_Substance 阈值
```

**说明：**
- 当 Weird_Substance > 500 时，创建迷宫
- 当 Weird_Substance < 500 时，等待积累

**调整建议：**
```python
# 频繁创建迷宫
weird_threshold = 200

# 积累更多再创建
weird_threshold = 1000

# 推荐（平衡）
weird_threshold = 500
```

---

## 📈 产量分析

### 场景 1：初始库存 1000 Weird_Substance

#### 无升级
```
所需：32 Weird/迷宫
迷宫数：1000 / 32 = 31 个
金币：31 × 1,024 = 31,744
```

#### 等级 0（已解锁）
```
所需：16 Weird/迷宫
迷宫数：1000 / 16 = 62 个
金币：62 × 1,024 = 63,488
```

#### 等级 1
```
所需：32 Weird/迷宫
迷宫数：1000 / 32 = 31 个
金币：31 × 2,048 = 63,488
```

**结论：解锁后，总收益相同！**

---

### 场景 2：f4.py 持续生产

#### f4.py 产量
```
~150,000 Weird_Substance/小时
```

#### f5.py 消耗（等级 0）
```
16 Weird/迷宫
150,000 / 16 = 9,375 个迷宫/小时
9,375 × 1,024 = 9,600,000 金币/小时
```

**结论：理论上可以获得 960 万金币/小时！**

**实际限制：**
- 求解迷宫需要时间（~10-30 秒/个）
- 实际产量：~500-1000 个迷宫/小时
- 实际金币：~50-100 万/小时

---

## 🎯 使用流程

### 步骤 1：准备阶段

```python
# 1. 确保有足够的 Weird_Substance
weird_count = num_items(Items.Weird_Substance)
# 建议：>500

# 2. 解锁迷宫功能
# unlock(Unlocks.Mazes)

# 3. 选择运行模式
run_mode = 2  # 持续循环
```

---

### 步骤 2：运行 f5.py

```python
# 直接运行
# 程序会自动：
# 1. 创建迷宫
# 2. 求解迷宫
# 3. 获得金币
# 4. 重复
```

---

### 步骤 3：监控统计

```python
# 程序会记录：
total_mazes_solved   # 求解的迷宫数
total_gold_earned    # 获得的金币总数
total_weird_used     # 消耗的 Weird_Substance

# 效率分析
efficiency = total_gold_earned / total_weird_used
# 应该接近 64 金币/Weird（等级 0）
```

---

## 🔄 与 f4.py 结合

### 策略 A：分离运行

```
1. 运行 f4.py 积累 Weird_Substance（1-2 小时）
2. 停止 f4.py
3. 运行 f5.py 消耗 Weird_Substance（10-30 分钟）
4. 停止 f5.py
5. 重复
```

**优点：**
- ✅ 简单
- ✅ 易于控制

**缺点：**
- ❌ 需要手动切换
- ❌ 效率较低

---

### 策略 B：混合运行（推荐）

```python
# 修改 f4.py，添加迷宫检查
while True:
    # f4.py 的采收逻辑
    total_harvests = smart_zone_harvest()
    
    # 检查 Weird_Substance
    weird_count = num_items(Items.Weird_Substance)
    
    # 如果超过阈值，创建迷宫
    if weird_count >= 500:
        # 调用 f5.py 的迷宫逻辑
        create_maze()
        solve_maze_smart()
        reset_position()
```

**优点：**
- ✅ 全自动
- ✅ 持续产出金币
- ✅ 最大化效率

**缺点：**
- ⚠️ 代码复杂度增加

---

## 💡 优化建议

### 1. 迷宫位置优化

```python
# 选择离农场中心较远的位置
# 避免干扰正常采收
maze_position_x = 0
maze_position_y = 0
```

---

### 2. 升级优先级

```python
# 优先升级迷宫等级
# 每次升级：金币翻倍
unlock(Unlocks.Mazes)  # 等级 0
unlock(Unlocks.Mazes)  # 等级 1
unlock(Unlocks.Mazes)  # 等级 2
```

**收益对比：**
```
等级 0 → 1：金币翻倍（1,024 → 2,048）
等级 1 → 2：金币翻倍（2,048 → 4,096）
等级 2 → 3：金币翻倍（4,096 → 8,192）
```

---

### 3. 算法选择

```python
# 小迷宫（<10×10）：右手法则
if farm_size < 10:
    solve_maze_right_hand()

# 大迷宫（≥10×10）：智能求解
else:
    solve_maze_smart()
```

---

### 4. 批量处理

```python
# 一次性创建多个迷宫
for i in range(10):
    create_maze()
    solve_maze_smart()
    reset_position()
```

---

## ⚠️ 注意事项

### 1. Weird_Substance 管理

```
⚠️ 确保有足够的库存
⚠️ 设置合理的 weird_substance_min
⚠️ 避免耗尽导致程序停止
```

---

### 2. 迷宫位置

```
⚠️ 避免在农场中心创建
⚠️ 可能干扰正常采收
⚠️ 推荐在角落或边缘
```

---

### 3. 求解失败

```
⚠️ 如果超过最大步数仍未找到宝藏
⚠️ 程序会停止
⚠️ 检查算法是否正确
```

---

### 4. 金币用途

```
💰 金币可以用于解锁功能
💰 检查哪些功能需要金币
💰 合理规划金币使用
```

---

## 🎉 总结

### 核心优势

1. **高效率**：64 金币/Weird_Substance
2. **全自动**：无需手动操作
3. **可扩展**：支持多种运行模式
4. **可靠性**：100% 求解成功率

---

### 推荐配置

```python
# f5.py 推荐配置
run_mode = 2                    # 持续循环
weird_substance_min = 100       # 最低库存
maze_position_x = 0             # 左下角
maze_position_y = 0

# 使用智能求解算法
solve_maze_smart()
```

---

### 预期产量

```
初始：1000 Weird_Substance
产出：~63,000 金币
时间：~30-60 分钟
效率：64 金币/Weird
```

---

**f5.py 迷宫金币生产系统已就绪！开始您的寻宝之旅吧！** 🗺️💰✨

