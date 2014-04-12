README
===============

JavaReflect 项目能帮助你简化你的 Java 反射相关代码。

目前本版本的 JavaReflect 只支持 Linux/Unix 平台，并且需要已经安装 Python 环境。

<h2>安装：</h2>

1.打开Shell（Terminal，Console），进入已经解压的 JavaReflect 文件夹。

2.运行 <code> python configure.py</code> 生成 makefile 文件。

3.运行 <code> make && sudo make install</code> 安装。

<h2>说明：</h2>

命令文件 javar 将安装在 /usr/local/bin ，所以请将 /usr/local/bin 加入 PATH 路径。而相关的 Python 文件会放置在 /etc/javareflect 文件夹下。

运行 <code> javar</code> 或 <code> javar -help</code> 即可看到使用说明。使用 javar 编译时会调用 javac 命令，并且支持 javac 的任何 option 选项。

与 javac 不同的是，javar 多出两个 option 选项，使用 <code> javar -r</code> 时将会识别 java 文件中代替反射的 # ，并替换为标准反射语句来编译。请放心，你的源代码不会被改变。如果你想把替换后的代码保存下来，请使用 <code> javar -rs</code> ，这将会把替换后的代码保存为一个后缀名为 .txt 的同名文件。

<h2>测试：</h2>

进入 example 文件夹，使用 <code> javar -r</code> 或 <code> javar -rs</code>。