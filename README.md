# SD 提示词去重

一键去除 Stable Diffusion 提示词中的重复 tag，支持正/负向提示词分别处理。

## 使用方式

### 浏览器界面（推荐）

打开 `index.html`，左右双栏分别粘贴正/负向提示词，点击「去重」即可。

- 支持自动去重（粘贴即去重）
- 显示去重统计（N tags → M tags，去重 X 个）
- 一键复制结果

### 命令行

```bash
# 直接输入
python prompt_dedup.py "masterpiece, 1girl, masterpiece, solo"
# 输出: masterpiece, 1girl, solo

# 剪贴板一键去重
python prompt_dedup.py -c

# 管道输入
echo "tag1, tag2, tag1" | python prompt_dedup.py
```

## 文件

- `index.html` — 双栏去重界面
- `prompt_dedup.py` — CLI 脚本，支持命令行/管道/剪贴板

