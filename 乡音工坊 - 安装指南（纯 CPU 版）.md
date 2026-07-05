

---

# 乡音工坊 - 安装指南（纯 CPU 版）

## 重要提示

请严格按照以下步骤操作，**不要跳过任何一步**！本指南专为**纯 CPU 电脑**编写，确保普通用户也能一步步完成安装。


## 第一步：安装 Python 3.10（必须是这个版本！）

1. **下载 Python 3.10**：
   - 点击这个链接直接下载：[Python 3.10.11 Windows 64位安装包](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)
   - 如果链接打不开，手动访问 https://www.python.org/downloads/release/python-31011/ ，拉到页面最底部，找到 **"Windows installer (64-bit)"** 点击下载。

2. **安装 Python**：
   - 双击下载好的 `python-3.10.11-amd64.exe`
   - ⚠️ **关键步骤**：在安装界面的最下方，**必须勾选 "Add Python 3.10 to PATH"**（如果不勾选，后面会报错）
   - 点击 **"Install Now"**，等待安装完成，点击 **"Close"**

3. **验证安装是否成功**：
   - 按 `Win + R` 键，输入 `cmd`，回车
   - 在黑框里输入：`python --version`
   - 如果显示 `Python 3.10.11`，说明安装成功！


## 第二步：配置国内下载源（解决下载慢/失败的问题）

1. 如果有 VPN，此步可以忽略。
2. 打开刚才的 cmd 黑框（或者重新按 `Win + R`，输入 `cmd`）
3. 复制下面这行命令，在黑框里右键点击粘贴，然后回车：

   `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`

4. 如果显示 `Writing to ...`，说明配置成功！


## 第三步：创建并激活虚拟环境（关键！）

为了避免依赖冲突，我们需要为"乡音工坊"创建一个独立的 Python 虚拟环境。

1. **找到程序文件夹**：
   - 将下载的 `乡音工坊.zip` 解压到一个**纯英文路径**下（例如 `D:\XiangYin\`，**路径中不能有中文和空格！**）
   - 打开解压后的文件夹，确保能看到 `LanguageTranslate.exe`、`requirements.txt` 等文件。

2. **打开 PowerShell**：
   - 在文件夹的空白处，**按住 Shift 键不放**，同时点击鼠标右键。
   - 在弹出的菜单里，点击 **"在此处打开 PowerShell 窗口"**（或"在终端中打开"）。

3. **创建虚拟环境**：
   - 在 PowerShell 中输入以下命令，然后回车：
     `python -m venv svc_env`
   - 这会在当前文件夹下创建一个名为 `svc_env` 的虚拟环境文件夹。
   - 说明：`svc_env` 是默认的虚拟环境名称，程序通常会自动识别。如果你想自定义名称或路径（例如 `my_venv`），也可以使用 `python -m venv 你的路径`，但后续安装和选择时需要手动对应。

4. **激活虚拟环境**：
   - 在 PowerShell 中输入以下命令激活环境：
     `.\svc_env\Scripts\Activate.ps1`
   - 如果使用命令提示符 (cmd)，激活命令为：
     `svc_env\Scripts\activate.bat`
   - 激活成功后，命令行提示符前会出现 `(svc_env)` 字样，表示当前已在虚拟环境中。


## 第四步：安装程序依赖库

请确保上一步虚拟环境已经激活（提示符前有 `(svc_env)`），再执行以下命令。

1. **安装 PyTorch（CPU 版）**：
   - 复制下面这行命令，在 PowerShell 里右键粘贴，然后回车：
     `pip install torch==2.1.0+cpu torchaudio==2.1.0+cpu -f https://download.pytorch.org/whl/torch_stable.html`
   - 注意：这是专门为纯 CPU 电脑准备的，下载可能需要 5-10 分钟，请耐心等待，不要关闭窗口！
   - 看到 `Successfully installed ...` 说明这步成功了。

2. **安装其他依赖**：
   - 继续复制下面这行命令，在 PowerShell 里粘贴并回车：
     `pip install -r requirements.txt`
   - 等待安装完成，没有报错即为成功！


## 第五步：下载并放置模型文件（重要！）

程序依赖两个预训练模型文件，由于体积较大（超过 900 MB），无法随安装包一起提供，**请务必手动下载并放置到指定位置**，否则声音转换功能将无法使用。

**需要下载的文件：**

- `G_28450.pth`（约 517 MB）→ 下载链接：https://language-translate.oss-cn-beijing.aliyuncs.com/model/G_28450.pth
- `hubert-soft-0d54a1f4.pt`（约 361 MB）→ 下载链接：https://language-translate.oss-cn-beijing.aliyuncs.com/pretrain/hubert-soft-0d54a1f4.pt

> 如果点击链接后浏览器直接下载，请将文件保存到本地。部分浏览器可能会弹出"此文件类型可能有害"的提示，请放心选择"保留"或"仍要下载"。

**放置路径（务必准确！）：**

1. 找到程序根目录：就是你解压后存放 `LanguageTranslate.exe` 的那个文件夹（例如 `D:\XiangYin\`）。
2. 创建必要的子文件夹（如果不存在的话）：
   - 在根目录下创建一个名为 `model` 的文件夹。
   - 在根目录下进入 `so-vits-svc` 文件夹，再在里面创建一个名为 `pretrain` 的文件夹（如果 `so-vits-svc` 文件夹不存在，请先解压源码包，确保它有）。
3. 将文件复制到对应位置：
   - 将下载的 `G_28450.pth` **复制或移动**到：`你的程序根目录\model\G_28450.pth`
   - 将下载的 `hubert-soft-0d54a1f4.pt` **复制或移动**到：`你的程序根目录\so-vits-svc\pretrain\hubert-soft-0d54a1f4.pt`

**最终目录结构应如下所示**（以 `D:\XiangYin` 为例）：

```
D:\XiangYin\
├── LanguageTranslate.exe
├── model\
│   └── G_28450.pth          ← 必须在此位置
├── so-vits-svc\
│   └── pretrain\
│       └── hubert-soft-0d54a1f4.pt   ← 必须在此位置
├── svc_env\                 （虚拟环境文件夹）
├── config.json              （如有）
└── ...其他文件
```

> ✅ 验证是否成功：检查上述两个文件的大小是否与下载时一致（约 517 MB 和 361 MB），且文件路径完全匹配。


## 第六步：运行程序并配置 Python 路径

1. **启动程序**：
   - 双击文件夹里的 **`LanguageTranslate.exe`**，程序界面会打开。

2. **选择虚拟环境的 Python 解释器**：
   - 在程序界面上方，找到 **"导入 Python 环境"** 按钮（或路径输入框）。
   - 点击按钮，浏览到刚才创建的虚拟环境文件夹，找到 `python.exe`，路径类似于：
     `你的解压路径\svc_env\Scripts\python.exe`
   - 例如：`D:\XiangYin\svc_env\Scripts\python.exe`
   - 选中它，确认选择。

3. **开始使用**：
   - 现在您可以正常进行录音、TTS 合成、SVC 声音转换了！如果程序正常打开且没有报错，恭喜您，安装成功！🎉


## 常见问题解决

**Q1：提示 "找不到 python" 或 "pip 不是内部或外部命令"**

A：卸载当前的 Python（在控制面板里找），重新安装，务必勾选 "Add Python 3.10 to PATH"。

**Q2：下载 torch 时特别慢或报错**

A：确保已经执行了第二步配置清华源，或者开启 VPN 后重试。

**Q3：提示 "ModuleNotFoundError: No module named 'xxx'"**

A：请确认在安装依赖时虚拟环境已激活（命令行提示符前有 `(svc_env)`）。如果漏装了某个包，重新执行 `pip install -r requirements.txt`。

**Q4：程序打开后闪退**

A：检查程序文件夹路径是否有中文或空格（例如 `D:\乡音工坊\` 不行，要改成 `D:\XiangYin\`）。确保所有依赖都已正确安装，检查在程序中选择的 Python 路径是否正确指向了虚拟环境中的 `python.exe`。

**Q5：如何自定义虚拟环境的位置？**

A：在第三步创建虚拟环境时，使用完整路径，例如 `python -m venv D:\MyVenvs\svc_env`。后续安装依赖时需要先激活该环境（`D:\MyVenvs\svc_env\Scripts\Activate.ps1`），在 Qt 程序中选择 Python 解释器的路径为 `D:\MyVenvs\svc_env\Scripts\python.exe`。

**Q6：下载模型文件后，程序仍然提示找不到模型？**

A：确认文件名称是否完全一致（注意大小写），确认文件是否放在了正确的子文件夹中（`model\` 和 `so-vits-svc\pretrain\`），不要将两个文件放反位置。如果文件已存在但程序报错，请尝试重启 `LanguageTranslate.exe`。


## 技术支持

如果按照以上步骤操作仍有问题，请联系开发者并提供以下信息：
1. 你的 Windows 版本（Win10/Win11）
2. 报错的截图（如果有）
3. PowerShell 里的错误信息（如果有）

