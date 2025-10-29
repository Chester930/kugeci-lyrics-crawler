# 🔄 F6 智能混合策略指南

## 🎯 策略目标

**自动在迷宫模式和生产模式之间切换，实现完全自动化的金币和 Weird_Substance 生产**

---

## 🔄 自动切换机制

### 模式切换逻辑（精确版）

```
开始 → 生产模式（FARM）
  ↓
积累 Weird_Substance
  ↓
达到 50,000？
  ↓ 是
切换到迷宫模式（MAZE）
  ↓
创建迷宫（需要 16 Weird_Substance）
  ↓
Weird_Substance 足够？
  ↓ 是
走迷宫 → 获得金币 → 继续创建下一个迷宫
  ↓
Weird_Substance 不足以创建新迷宫？
  ↓ 是
切换回生产模式（FARM）
  ↓
循环往复...
```

**关键切换点：**

1. **生产 → 迷宫**：当 `Weird_Substance >= 50,000` 时
2. **迷宫 → 生产**：当 `Weird_Substance < 创建迷宫所需数量` 时
   - 32×32 地图，迷宫等级 0：需要 32 Weird_Substance
   - 实际上，程序还会检查 `< 100` 作为保底阈值

**为什么这样设计？**
- ✅ 迷宫模式会持续运行，直到**无法创建新迷宫**为止
- ✅ 不会浪费任何 Weird_Substance
- ✅ 自动最大化迷宫数量和金币产出

---

## ⚙️ 核心参数

### 切换阈值

```python
weird_substance_maze_threshold = 50000  # 达到 50k 时切换到迷宫模式
weird_substance_farm_threshold = 100    # 低于 100 时切换到生产模式
```

**调整建议：**

#### 更频繁切换到迷宫
```python
weird_substance_maze_threshold = 10000  # 达到 10k 就开始走迷宫
```

#### 更少切换（积累更多）
```python
weird_substance_maze_threshold = 100000  # 积累 10 万再走迷宫
```

#### 更早切换回生产
```python
weird_substance_farm_threshold = 1000  # 剩余 1k 时就回到生产模式
```

---

## 📊 两种模式详解

### 模式 1：生产模式（FARM）

**来源：** f4.py 策略（已修改）

**区域配置（32×32 地图）：**
- **左下角 20×20**：仙人掌区（100%感染 + 排序 + 连锁收获）
- **右下角 12×12**：南瓜区（100%感染 + 巨型南瓜）
- **左上角 12×12**：南瓜区（100%感染 + 巨型南瓜）
- **右上角 12×12**：混合区（伴生种植：草/灌木/树/萝卜）
- **其余区域**：向日葵区（能量生产）

**功能：**
- 仙人掌区：100%感染 + 排序 + 连锁收获
- 南瓜区（2个）：100%感染 + 巨型南瓜（12×12）
- 混合区：伴生种植（放养模式）
- 向日葵区：能量生产

**产量：**
- 仙人掌：80,000 Weird_Substance/次
- 南瓜（2个）：1,296 × 2 = 2,592 Weird_Substance/次
- 混合区：伴生奖励
- 总计：~150,000 Weird_Substance/小时

**何时运行：**
- Weird_Substance < 50,000
- 自动积累资源

---

### 模式 2：迷宫模式（MAZE）

**来源：** f5.py 策略

**功能：**
- 创建迷宫（消耗 16 Weird_Substance）
- 自动走迷宫（智能求解）
- 获得金币（1,024 金币/次）

**产量：**
- 金币：64 金币/Weird_Substance
- 效率：~3,125 迷宫（50,000 / 16）
- 总金币：~3,200,000 金币

**何时运行：**
- Weird_Substance >= 50,000
- 持续走迷宫直到 < 100

---

## 📈 完整循环示例

### 第 1 阶段：生产模式（0 → 50,000）

```
轮次 1-100：
→ 模式：FARM
→ 采收南瓜、仙人掌、向日葵
→ Weird_Substance：0 → 5,000

轮次 101-200：
→ 模式：FARM
→ 仙人掌连锁收获（80,000 Weird）
→ Weird_Substance：5,000 → 85,000

达到 50,000！切换到迷宫模式
```

---

### 第 2 阶段：迷宫模式（85,000 → 剩余不足）

```
迷宫 1：
→ 模式：MAZE
→ 检查 Weird_Substance：85,000（足够）
→ 创建迷宫（-32 Weird）
→ 走迷宫 → 获得金币（+1,024）

迷宫 2-2,656：
→ 持续创建迷宫
→ 每个迷宫：-32 Weird, +1,024 金币

迷宫 2,656 完成后：
→ Weird_Substance：85,000 → 16（剩余）
→ 总金币：+2,719,744
→ 检查创建新迷宫：需要 32，但只有 16

无法创建新迷宫！切换回生产模式
```

**说明：**
- 32×32 地图，迷宫等级 0：每个迷宫需要 32 Weird_Substance
- 85,000 ÷ 32 = 2,656 个迷宫（剩余 16）
- 当剩余 < 32 时，无法创建新迷宫，自动切换回生产模式

---

### 第 3 阶段：再次生产（16 → 50,000）

```
轮次 201-300：
→ 模式：FARM
→ 采收南瓜、仙人掌、向日葵、混合区
→ Weird_Substance：16 → 50,000

达到 50,000！再次切换到迷宫模式
```

**循环往复，永不停止！** 🔄

**重要说明：**
- ✅ 迷宫模式会**用尽所有可用的 Weird_Substance**
- ✅ 只有当**无法创建新迷宫**时才切换回生产模式
- ✅ 这确保了最大化金币产出，不浪费任何资源

---

## 💰 产量分析

### 单次完整循环

#### 生产阶段（~20 分钟）
```
Weird_Substance：0 → 50,000
金币：0
```

#### 迷宫阶段（~60-90 分钟）
```
Weird_Substance：50,000 → 0
金币：+3,200,000
```

#### 总计（~2 小时/循环）
```
Weird_Substance：净消耗 0（循环平衡）
金币：+3,200,000/循环
效率：~1,600,000 金币/小时
```

---

### 长期运行（24 小时）

```
循环次数：24 / 2 = 12 次
金币总计：3,200,000 × 12 = 38,400,000
Weird_Substance：持续循环（0 → 50k → 0）
```

**24 小时可获得 3,840 万金币！** 💰💰💰

---

## 🎯 使用流程

### 步骤 1：准备

```python
# 确保已解锁必要功能
# - Unlocks.Mazes（迷宫）
# - Unlocks.Fertilizer（肥料）
# - Unlocks.Cactus（仙人掌）
```

---

### 步骤 2：运行 f6.py

```python
# 直接运行，无需配置
# 程序会自动：
# 1. 检查 Weird_Substance 库存
# 2. 选择合适的模式
# 3. 自动切换
# 4. 持续运行
```

---

### 步骤 3：监控（可选）

```python
# 程序会自动记录：
current_mode          # 当前模式（"FARM" 或 "MAZE"）
total_mazes_solved    # 迷宫总数
total_gold_earned     # 金币总数
total_weird_used      # Weird_Substance 消耗
```

---

## 🔧 高级配置

### 1. 调整切换阈值

#### 快速切换（更频繁走迷宫）
```python
weird_substance_maze_threshold = 10000   # 10k 就走迷宫
weird_substance_farm_threshold = 500     # 剩余 500 就回生产
```

**效果：**
- ✅ 更频繁获得金币
- ✅ Weird_Substance 波动小
- ❌ 切换次数多

---

#### 慢速切换（积累更多再走）
```python
weird_substance_maze_threshold = 100000  # 10 万才走迷宫
weird_substance_farm_threshold = 100     # 剩余 100 就回生产
```

**效果：**
- ✅ 单次迷宫阶段更长
- ✅ 切换次数少
- ❌ 等待时间长

---

### 2. 调整生产模式参数

```python
# 肥料管理
fertilizer_min_stock = 20  # 最低肥料库存

# 南瓜策略
pumpkin_wait_for_merge = True  # 等待巨型南瓜
pumpkin_threshold = 17         # 12×12 南瓜阈值

# 仙人掌策略
cactus_sorting_cycles = 4  # 排序循环次数
```

---

### 3. 调整迷宫位置

```python
# 避免干扰生产区域
maze_position_x = 0  # 左下角
maze_position_y = 0
```

---

## 📊 模式对比

| 特性 | 生产模式（FARM） | 迷宫模式（MAZE） |
|------|----------------|----------------|
| **目标** | 积累 Weird_Substance | 消耗 Weird_Substance，获得金币 |
| **时间** | ~20 分钟（0 → 50k） | ~60-90 分钟（50k → 0） |
| **产出** | 50,000 Weird_Substance | 3,200,000 金币 |
| **策略** | f4.py（巨型南瓜+仙人掌连锁） | f5.py（智能走迷宫） |
| **复杂度** | 高 | 中 |

---

## 💡 优化建议

### 1. 优先升级迷宫等级

```python
# 每次升级：金币翻倍
unlock(Unlocks.Mazes)  # 等级 0
unlock(Unlocks.Mazes)  # 等级 1（金币 ×2）
unlock(Unlocks.Mazes)  # 等级 2（金币 ×4）
```

**收益提升：**
```
等级 0：3,200,000 金币/循环
等级 1：6,400,000 金币/循环
等级 2：12,800,000 金币/循环
```

---

### 2. 优先升级肥料

```python
# 确保肥料充足
unlock(Unlocks.Fertilizer)  # 等级 0
unlock(Unlocks.Fertilizer)  # 等级 1（产量 ×2）
unlock(Unlocks.Fertilizer)  # 等级 2（产量 ×4）
```

**效果：**
- 更快积累 Weird_Substance
- 缩短生产阶段时间
- 提高整体效率

---

### 3. 平衡切换阈值

```python
# 推荐配置（平衡）
weird_substance_maze_threshold = 50000  # 5 万
weird_substance_farm_threshold = 100    # 100
```

**原因：**
- 5 万足够走 3,125 个迷宫
- 100 确保不会完全耗尽
- 切换频率适中

---

## ⚠️ 注意事项

### 1. 初始库存

```
⚠️ 首次运行时，Weird_Substance = 0
⚠️ 会先进入生产模式
⚠️ 需要等待积累到 50,000
⚠️ 预计时间：~20-30 分钟
```

---

### 2. 模式切换机制详解

#### 切换到迷宫模式的条件：
```python
# 在生产模式中检查
if num_items(Items.Weird_Substance) >= 50000:
    current_mode = "MAZE"
```

#### 切换回生产模式的条件：
```python
# 在迷宫模式中检查（两个检查点）

# 检查点 1：每次循环开始时
if num_items(Items.Weird_Substance) < 100:
    current_mode = "FARM"
    return

# 检查点 2：尝试创建迷宫时
maze_level = num_unlocked(Unlocks.Mazes)
substance_needed = farm_size * 2**(maze_level - 1)  # 32×32 地图 = 32
if num_items(Items.Weird_Substance) < substance_needed:
    current_mode = "FARM"
    return  # 无法创建新迷宫，切换回生产模式
```

**实际行为：**
- ✅ 迷宫模式会持续运行，直到 Weird_Substance **不足以创建新迷宫**
- ✅ 切换是**瞬间完成**的，不会中断当前操作
- ✅ 切换时会**重置位置**到 (0,0)

---

### 3. 资源管理

```
⚠️ 确保肥料充足（生产模式需要）
⚠️ 确保水资源充足（两种模式都需要）
⚠️ 监控库存，及时升级
```

---

## 🎉 总结

### 核心优势

1. **完全自动化**
   - 无需手动切换
   - 无需监控库存
   - 持续运行

2. **高效率**
   - 生产模式：~150,000 Weird/小时
   - 迷宫模式：64 金币/Weird
   - 总效率：~1,600,000 金币/小时

3. **平衡发展**
   - Weird_Substance 持续循环
   - 金币持续增长
   - 资源永不枯竭

4. **灵活配置**
   - 可调整切换阈值
   - 可调整生产参数
   - 可调整迷宫位置

---

### 推荐配置

```python
# 平衡配置（推荐）
weird_substance_maze_threshold = 50000
weird_substance_farm_threshold = 100
fertilizer_min_stock = 20
pumpkin_wait_for_merge = True
cactus_sorting_cycles = 4
```

---

### 预期收益

```
单次循环（~2 小时）：
→ Weird_Substance：0 → 50k → 0（循环）
→ 金币：+3,200,000

24 小时：
→ 循环次数：12 次
→ 金币：+38,400,000
```

---

**f6.py 智能混合策略 - 完全自动化的金币生产系统！** 🔄💰✨🚀

