# 使用 pysimplegui 开发的批量解压和压缩工具

功能： 将本子之类的 rar,7zip 压缩包批量解压成文件夹,或者将批量的文件夹打包成 zip,方便导入 calibre 或其他阅读软件查看。解压运行 gui.exe

1. 批量解压 rar,7zip,zip
2. 批量压缩文件夹成 zip

screenshot
![运行截图](https://raw.githubusercontent.com/liangcai/benzi_multiple_unzip/master/screenshot.png)

Use for：unzip multiple files to folder, or make multiple archiver files from folders.extract the file and exec gui.exe

## for dev

### windows

#### dependencies

rarfile dependencies unrar.exe for windows. see https://rarfile.readthedocs.io/en/latest/faq.html#how-can-i-get-it-work-on-windows

#### package

`pyinstaller -w gui.py --add-binary="unrar.exe;."`
