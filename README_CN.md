# Claude X Post Skill

一个 Claude Code 技能插件，让你可以直接在 Claude Code 会话中发布推文到 X (Twitter)。只需用自然语言告诉 Claude 你想发什么即可。

## 功能特点

- **自然语言发推** - 只需说"发到X"或"发推文"
- **线程支持** - 创建和继续命名线程
- **媒体支持** - 附加图片、GIF、视频
- **截图功能** - 截取终端窗口并发推
- **历史记录** - Claude 会记住你的线程

## 使用示例

```
"发到X: 刚刚完成了一个新功能！"

"Tweet: 正在用 Claude Code 做一些很酷的东西"

"截图这个终端并发推"

"创建一个叫 'launch-day' 的线程: 我们今天发布了！"

"继续我的 launch-day 线程: 反响非常好..."
```

---

## 第一步：申请 X (Twitter) API Key

要使用此技能，你需要先申请 X 的开发者账号和 API 密钥。

### 1.1 注册 X 开发者账号

1. 访问 [X 开发者平台](https://developer.twitter.com/)
2. 点击右上角 **Sign up** 或 **Log in**（如已有 X 账号则登录）
3. 登录后，点击 **Developer Portal**

### 1.2 申请开发者访问权限

1. 在 Developer Portal 中，点击 **Sign up for Free Account** 或申请更高级别的访问权限
2. 填写申请表单：
   - **What's your use case?** - 描述你的使用目的，例如：
     ```
     I am building a personal tool to post tweets from my terminal using Claude Code.
     This is for personal use only - posting my own content to my own account.
     I will not use it for automated posting, spam, or any commercial purposes.
     ```
   - 勾选同意开发者协议
3. 提交申请并等待审核（通常几分钟到几小时）

### 1.3 创建项目和应用

审核通过后：

1. 进入 [Developer Portal Dashboard](https://developer.twitter.com/en/portal/dashboard)
2. 点击 **+ Create Project**
3. 填写项目信息：
   - **Project name**: `Claude X Post` (或任意名称)
   - **Use case**: 选择 `Making a bot` 或 `Exploring the API`
   - **Project description**: 简单描述项目用途
4. 创建完项目后，会提示创建 App：
   - **App name**: `claude-x-post` (或任意名称)

### 1.4 获取 API Keys 和 Tokens

1. 进入你的 App 设置页面
2. 点击 **Keys and tokens** 标签
3. 你需要获取以下 4 个值：

#### API Key 和 Secret
- 在 **Consumer Keys** 部分
- 点击 **Regenerate** 获取：
  - `API Key` → 对应 `X_API_KEY`
  - `API Key Secret` → 对应 `X_API_KEY_SECRET`

#### Access Token 和 Secret
- 在 **Authentication Tokens** 部分
- 点击 **Generate** 获取：
  - `Access Token` → 对应 `X_ACCESS_TOKEN`
  - `Access Token Secret` → 对应 `X_ACCESS_TOKEN_SECRET`

> **重要**: 生成后请立即保存这些值，Secret 只显示一次！

### 1.5 设置 App 权限

1. 在 App 设置页面，点击 **Settings** 标签
2. 找到 **User authentication settings**，点击 **Set up**
3. 配置权限：
   - **App permissions**: 选择 **Read and write**（读写权限）
   - **Type of App**: 选择 **Web App, Automated App or Bot**
   - **Callback URI**: 填写 `https://localhost` (仅用于满足必填要求)
   - **Website URL**: 填写你的任意网站或 `https://github.com`
4. 点击 **Save**

> **注意**: 修改权限后，需要重新生成 Access Token 和 Secret！

---

## 第二步：安装技能

### 2.1 创建技能目录

```bash
mkdir -p ~/.claude/skills
```

### 2.2 克隆仓库

```bash
cd ~/.claude/skills
git clone https://github.com/pravj/claude-x-post-skill.git x-post
```

或者手动下载并解压到 `~/.claude/skills/x-post/` 目录。

### 2.3 安装 Python 依赖

```bash
cd ~/.claude/skills/x-post
pip install -r requirements.txt
```

依赖包括：
- `tweepy` - X API Python 客户端
- `python-dotenv` - 环境变量管理

---

## 第三步：配置 API 密钥

### 3.1 创建配置文件

```bash
cd ~/.claude/skills/x-post
cp .env.example .env
```

### 3.2 编辑 .env 文件

用你喜欢的编辑器打开 `.env` 文件：

```bash
nano ~/.claude/skills/x-post/.env
# 或
vim ~/.claude/skills/x-post/.env
# 或
code ~/.claude/skills/x-post/.env
```

填入你在第一步获取的 API 密钥：

```env
X_API_KEY=你的_API_Key
X_API_KEY_SECRET=你的_API_Key_Secret
X_ACCESS_TOKEN=你的_Access_Token
X_ACCESS_TOKEN_SECRET=你的_Access_Token_Secret
```

保存文件。

---

## 第四步：验证安装

### 4.1 检查目录结构

确保你的目录结构如下：

```
~/.claude/
└── skills/
    └── x-post/
        ├── SKILL.md          # 技能定义文件（必需）
        ├── x-post.py         # 主脚本
        ├── requirements.txt  # Python 依赖
        ├── .env              # 你的 API 密钥（你创建的）
        └── .env.example      # 示例配置文件
```

### 4.2 测试 API 连接

运行以下命令测试（不会实际发推）：

```bash
cd ~/.claude/skills/x-post
python x-post.py history
```

如果配置正确，应该显示空的历史记录而不是错误信息。

### 4.3 重启 Claude Code

关闭并重新打开 Claude Code，技能会自动被检测到。

---

## 使用方法

### 在 Claude Code 中使用（推荐）

直接用自然语言告诉 Claude：

**发送简单推文：**
> 你: "发到X: 正在用 Claude Code 构建项目"
> Claude: 完成！https://x.com/i/status/123...

**创建线程：**
> 你: "创建一个叫 'product-launch' 的线程: 今天我们发布新产品！"
> Claude: 线程已创建！我会记住 'product-launch' 以便你之后继续。

**继续线程：**
> 你: "继续我的 product-launch 线程: 感谢大家的支持..."
> Claude: 已添加到线程！https://x.com/i/status/456...

**带截图发推：**
> 你: "截图这个窗口并发推: 看看 Claude 刚帮我写的代码"
> Claude: *截取窗口* 已发布！https://x.com/i/status/789...

### 命令行直接使用

也可以直接在终端使用：

```bash
cd ~/.claude/skills/x-post

# 发送推文
python x-post.py tweet "你的推文内容"

# 带图片发推
python x-post.py media /path/to/image.jpg "图片说明"

# 发送线程（从 JSON 文件）
python x-post.py thread /path/to/thread.json --name "线程名称"

# 继续命名线程
python x-post.py continue "线程名称" "下一条推文"
python x-post.py continue-media "线程名称" /path/to/image.jpg "下一条推文"

# 回复推文
python x-post.py reply <推文ID> "回复内容"
python x-post.py reply-media <推文ID> /path/to/image.jpg "回复内容"

# 截图并发推（仅 macOS）
python x-post.py snap "说明文字"

# 查看历史
python x-post.py history
python x-post.py threads
```

---

## CLI 命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `tweet` | 发送文字推文 | `python x-post.py tweet "Hello World"` |
| `media` | 发送带媒体的推文 | `python x-post.py media ./pic.jpg "图片"` |
| `thread` | 从 JSON 发送线程 | `python x-post.py thread ./thread.json --name "my-thread"` |
| `reply` | 回复推文 | `python x-post.py reply 123456 "回复内容"` |
| `reply-media` | 带媒体回复 | `python x-post.py reply-media 123456 ./pic.jpg "回复"` |
| `continue` | 继续命名线程 | `python x-post.py continue "my-thread" "继续内容"` |
| `continue-media` | 带媒体继续线程 | `python x-post.py continue-media "my-thread" ./pic.jpg "内容"` |
| `snap` | 截图并发推 | `python x-post.py snap "截图说明"` |
| `history` | 查看发推历史 | `python x-post.py history 20` |
| `threads` | 查看保存的线程 | `python x-post.py threads` |

### 线程 JSON 格式

```json
["第一条推文", "第二条推文", "第三条推文"]
```

### --name 参数

使用 `--name "名称"` 可以给线程命名，方便之后继续：

```bash
python x-post.py tweet "线程开始" --name "my-thread"
python x-post.py continue "my-thread" "继续这个线程"
```

---

## 常见问题

### Q: 提示 "401 Unauthorized" 错误

**原因**: API 密钥配置错误或权限不足

**解决方案**:
1. 检查 `.env` 文件中的密钥是否正确复制（没有多余空格）
2. 确认 App 权限已设置为 **Read and write**
3. 如果修改过权限，重新生成 Access Token 和 Secret

### Q: 提示 "403 Forbidden" 错误

**原因**: 免费 API 访问级别限制

**解决方案**:
1. 免费版 API 有发推限制，检查是否超出配额
2. 考虑升级到 Basic ($100/月) 或更高级别获取更多配额

### Q: 截图功能不工作

**原因**: `screencapture` 命令仅支持 macOS

**解决方案**:
- 在 macOS 上，确保终端有屏幕录制权限（系统偏好设置 > 安全性与隐私 > 隐私 > 屏幕录制）
- 在其他系统上，手动截图后使用 `media` 命令发送

### Q: 线程发送失败

**原因**: 可能是 API 速率限制

**解决方案**:
- 线程中的推文发送间隔可能过快
- 等待几分钟后重试
- 检查 X 开发者后台的 API 使用情况

---

## 注意事项

- **字符限制**: 每条推文最多 280 字符（Premium 用户可能有更高限制）
- **媒体格式**: 支持 JPG、PNG、GIF、MP4
- **推文 ID**: 从 `https://x.com/user/status/1234567890` 中，`1234567890` 就是推文 ID
- **历史记录**: 保存在 `post-history.json` 文件中，最多保留最近 100 条

---

## 许可证

MIT

## 作者

Pravendra Singh
