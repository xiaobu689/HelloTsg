import os

# 设置小程序源代码的目录
source_directory = r'E:\script_tool\UnpackMiniApp\wxpack'
output_directory = r'E:\script_tool\UnpackMiniApp\wxpack\tclx'

# 获取目录中所有.wxapkg文件
wxapkg_files = [f for f in os.listdir(source_directory) if f.endswith('.wxapkg')]
print(wxapkg_files)

# 处理子包
for wxapkg_file in wxapkg_files:
    wxapkg_path = os.path.join(source_directory, wxapkg_file)
    print(wxapkg_path)
    os.system(
        f'node E:\\script_tool\\wxappUnpacker\\wuWxapkg.js {wxapkg_path} -s=E:\\script_tool\\UnpackMiniApp\\wxpack\\tclx')


