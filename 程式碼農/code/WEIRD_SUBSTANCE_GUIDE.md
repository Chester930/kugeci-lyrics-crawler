# 🧪 怪异物质最大化生产指南

## 🎯 策略目标

**最大化生产 `Items.Weird_Substance`（怪异物质）**

---

## 📚 核心机制

### 肥料与感染系统

#### 肥料效果
```python
use_item(Items.Fertilizer)
→ 减少 2 秒生长时间
→ 植物被感染（Infected）
```

#### 感染效果
```
感染的植物收获时：
- 50% 产量 → 正常物品
- 50% 产量 → Items.Weird_Substance
```

#### 示例
```
收获感染的南瓜：
- 正常：1 南瓜
- 感染：0.5 南瓜 + 0.5 Weird_Substance

收获感染的仙人掌：
- 正常：1 仙人掌
- 感染：0.5 仙人掌 + 0.5 Weird_Substance
```

---

## 🗺️ 农场布局

### 32×32 地图配置

#### 仙人掌区（左下角 20×20）
```
坐标：X: 0-19, Y: 0-19
面积：400 格
策略：
1. 种植仙人掌
2. 立即使用肥料感染
3. 成熟后直接采收（不排序，不连锁）
4. 获得 50% 仙人掌 + 50% Weird_Substance
```

**预期产量：**
```
400 格 × 50% = 200 Weird_Substance/轮
```

---

#### 南瓜区（三个角落 12×12）
```
右下角：X: 20-31, Y: 0-11 (144 格)
左上角：X: 0-11, Y: 20-31 (144 格)
右上角：X: 20-31, Y: 20-31 (144 格)
总面积：432 格

策略：
1. 种植南瓜
2. 立即使用肥料感染
3. 成熟后直接采收（不追踪ID，不合并）
4. 获得 50% 南瓜 + 50% Weird_Substance
```

**预期产量：**
```
432 格 × 50% = 216 Weird_Substance/轮
```

---

#### 向日葵区（其余区域）
```
面积：192 格
策略：
- 不使用肥料（保持正常产出）
- 优先收获高花瓣向日葵（5x 能量）
- 提供能量加速无人机（2x 速度）
```

---

## 🔧 关键参数

### 肥料管理
```python
fertilizer_min_stock = 10  # 最低肥料库存
```

**说明：**
- 当肥料 > 10 时，才使用肥料
- 避免肥料耗尽
- 确保持续供应

**肥料补充：**
```
基础：1 个/10 秒
升级后：2, 4, 8 个/10 秒（翻倍）
```

---

### 区域开关
```python
use_fertilizer_on_cactus = True   # 对仙人掌使用肥料
use_fertilizer_on_pumpkin = True  # 对南瓜使用肥料
```

**可调整：**
- 如果肥料不足，可以关闭某个区域
- 优先级：南瓜区 > 仙人掌区（南瓜生长更快）

---

## 📊 产量分析

### 理论产量（每轮）

#### 仙人掌区
```
400 格 × 0.5 = 200 Weird_Substance
```

#### 南瓜区
```
432 格 × 0.5 = 216 Weird_Substance
```

#### 总计
```
200 + 216 = 416 Weird_Substance/轮
```

---

### 实际产量（考虑生长时间）

#### 假设条件
```
- 水分：0.95（生长速度 4.75x）
- 肥料：-2 秒生长时间
- 每轮时间：~5 分钟
```

#### 仙人掌
```
基础生长时间：~60 秒
加速后：60 / 4.75 - 2 ≈ 10.6 秒
每轮可采收：~28 次
产量：400 × 0.5 × 28 = 5,600 Weird_Substance/小时
```

#### 南瓜
```
基础生长时间：~30 秒
加速后：30 / 4.75 - 2 ≈ 4.3 秒
每轮可采收：~70 次
产量：432 × 0.5 × 70 = 15,120 Weird_Substance/小时
```

#### 总计
```
5,600 + 15,120 = 20,720 Weird_Substance/小时
```

---

## 🚀 优化策略

### 1. 极限浇水
```python
if status['water'] < 0.95:
    use_item(Items.Water)
```

**效果：**
- 水分 0.95 → 生长速度 4.75x
- 接近最大速度（5x）

---

### 2. 积极采收
```python
# 每次移动后立即处理
move(North)
smart_zone_processing(x, y, True)
```

**效果：**
- 采收频率：~1024 次/轮
- 不错过任何成熟植物

---

### 3. 肥料优先级
```python
# 种植后立即使用肥料
plant(Entities.Pumpkin)
if num_items(Items.Fertilizer) > fertilizer_min_stock:
    use_item(Items.Fertilizer)
```

**效果：**
- 立即感染
- 加速生长
- 确保收获时获得 Weird_Substance

---

### 4. 未成熟植物加速
```python
# 对未成熟植物使用肥料
elif status['entity'] == Entities.Pumpkin and not status['can_harvest']:
    if num_items(Items.Fertilizer) > fertilizer_min_stock:
        use_item(Items.Fertilizer)
```

**效果：**
- 持续加速生长
- 最大化肥料利用
- 缩短生长周期

---

## ⚠️ 注意事项

### 1. 不要使用 Weird_Substance 治疗
```python
# ❌ 错误：治疗感染
use_item(Items.Weird_Substance)  # 会移除感染状态

# ✅ 正确：保持感染
# 不使用 Weird_Substance
```

**原因：**
- 治疗会移除感染状态
- 失去 50% Weird_Substance 产出
- 违背策略目标

---

### 2. 不要追求巨型南瓜
```python
# ❌ 错误：等待南瓜合并
if consecutive_count >= pumpkin_threshold:
    harvest()

# ✅ 正确：直接采收
if status['can_harvest']:
    harvest()
```

**原因：**
- 巨型南瓜需要等待合并
- 降低采收频率
- 减少 Weird_Substance 产量

---

### 3. 不要排序仙人掌
```python
# ❌ 错误：排序仙人掌
safe_cactus_sorting_horizontal()
safe_cactus_sorting_vertical()

# ✅ 正确：直接采收
if status['can_harvest']:
    harvest()
```

**原因：**
- 排序需要时间
- 连锁收获不产生 Weird_Substance
- 单个采收更高效

---

### 4. 确保肥料充足
```python
# 检查肥料库存
if num_items(Items.Fertilizer) > fertilizer_min_stock:
    use_item(Items.Fertilizer)
```

**建议：**
- 升级 `Unlocks.Fertilizer` 到最高等级
- 设置合理的 `fertilizer_min_stock`（10-20）
- 监控肥料消耗速度

---

## 📈 与正常模式对比

### 正常模式（main.py）
```
仙人掌：400² = 160,000 仙人掌/次（连锁收获）
南瓜：最大 144² = 20,736 南瓜/次（巨型南瓜）
采收频率：低（需要等待合并/排序）
```

### 怪异物质模式（f3.py）
```
仙人掌：400 × 0.5 = 200 Weird_Substance/轮
南瓜：432 × 0.5 = 216 Weird_Substance/轮
采收频率：高（直接采收）
总产量：~20,000 Weird_Substance/小时
```

**对比：**
- 牺牲了连锁收获和巨型南瓜
- 换取了持续的 Weird_Substance 产出
- 适合需要大量 Weird_Substance 的场景

---

## 🎯 使用场景

### 何时使用怪异物质模式

#### 场景 1：种植迷宫
```
use_item(Items.Weird_Substance) on bush
→ 生成迷宫
→ 需要大量 Weird_Substance
```

#### 场景 2：感染控制
```
use_item(Items.Weird_Substance) on plant
→ 切换感染状态（自己 + 相邻植物）
→ 用于精确控制感染
```

#### 场景 3：实验/测试
```
测试感染机制
测试肥料效果
测试 Weird_Substance 用途
```

---

### 何时使用正常模式

#### 场景 1：最大化仙人掌产量
```
需要大量仙人掌
使用 main.py（连锁收获 160,000/次）
```

#### 场景 2：最大化南瓜产量
```
需要大量南瓜
使用 main.py（巨型南瓜 20,736/次）
```

#### 场景 3：平衡发展
```
需要多种资源
使用 main.py（平衡配置）
```

---

## 🔄 切换模式

### 从 main.py 切换到 f3.py
```
1. 停止 main.py
2. 运行 f3.py
3. 等待植物被感染
4. 开始收获 Weird_Substance
```

### 从 f3.py 切换回 main.py
```
1. 停止 f3.py
2. 清理感染的植物（可选）
3. 运行 main.py
4. 恢复正常生产
```

---

## 📝 监控指标

### 关键指标

#### Weird_Substance 库存
```python
weird_count = num_items(Items.Weird_Substance)
```

#### 肥料库存
```python
fertilizer_count = num_items(Items.Fertilizer)
```

#### 采收次数
```python
harvest_count  # 每 10 轮重置
```

#### 水资源
```python
water_count = num_items(Items.Water)
```

---

### 性能评估

#### 良好状态
```
✅ Weird_Substance 持续增加
✅ 肥料库存 > 10
✅ 水资源充足
✅ 采收频率稳定
```

#### 需要调整
```
⚠️ Weird_Substance 增长缓慢
⚠️ 肥料库存 < 10
⚠️ 水资源不足
⚠️ 采收频率下降
```

#### 问题状态
```
❌ Weird_Substance 不增加
❌ 肥料耗尽
❌ 水资源耗尽
❌ 无采收
```

---

## 🛠️ 故障排除

### 问题 1：Weird_Substance 不增加
```
原因：植物未被感染
解决：
1. 检查肥料库存
2. 确认 use_fertilizer_on_* = True
3. 确认 fertilizer_min_stock 设置合理
```

### 问题 2：肥料消耗过快
```
原因：肥料使用过于频繁
解决：
1. 提高 fertilizer_min_stock（10 → 20）
2. 关闭某个区域（use_fertilizer_on_cactus = False）
3. 升级 Unlocks.Fertilizer
```

### 问题 3：产量低于预期
```
原因：生长速度慢 / 采收频率低
解决：
1. 确保水分 ≥ 0.95
2. 确保肥料充足
3. 检查采收逻辑
```

---

## 🎉 总结

### 核心策略
```
1. 使用肥料感染植物
2. 直接采收获得 Weird_Substance
3. 不追求巨型南瓜和连锁收获
4. 最大化采收频率
5. 极限浇水加速生长
```

### 预期产量
```
~416 Weird_Substance/轮
~20,000 Weird_Substance/小时
```

### 适用场景
```
需要大量 Weird_Substance
种植迷宫
感染控制实验
```

---

**怪异物质生产模式已就绪！开始收获吧！** 🧪✨🚀

