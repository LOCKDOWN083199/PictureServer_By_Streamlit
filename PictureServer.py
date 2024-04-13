import streamlit as st
import os

# 设置列数
Cols_Size = 4
# 每页显示的图片数量
Image_Num = 30

# 获取/Src/目录下的所有文件
def get_all_files():
    files = os.listdir('./Src/')
    for i in range(len(files)):
        files[i] = './Src/' + files[i]
    return files


# 提供下载链接
def download_image(image_path: str, col: st.columns):
    with open(image_path, 'rb') as f:
        bytes = f.read()
        col.download_button(
            label=f"Download {image_path.split('/')[-1]}",
            data=bytes,
            file_name=image_path,
            mime='image/jpg'
        )

# 图片页面
def Picture_Page(files):
    st.write("## 图片浏览与下载")

    # 包含图片路径的列表
    image_paths = files

    # 创建并排的列
    Cols = st.columns(Cols_Size)

    # 在每个列中添加图片
    for i, image_path in enumerate(image_paths):
        t = i % Cols_Size
        # 显示图片预览
        Cols[t].image(image_path, width=170)  # 通过调整width参数来改变图片预览的大小
        download_image(image_path, Cols[t])

# 上传图片页面
def Upload_Page():
    st.write("## 上传图片")
    UpFile=st.file_uploader("选择文件")
    if UpFile is not None:
        st.image(UpFile, caption="Uploaded Image.")
        st.write("上传成功")

        File_Byts = UpFile.read()
        with open(f"./Src/{UpFile.name}", "wb") as f:
            f.write(File_Byts)
        st.write("保存成功")


# 页面选择切换
def Page_Select():
    files = get_all_files() # 获取所有文件名的列表
    files_len = len(files) # 获取文件数量
    pages_len = files_len // Image_Num # 获取页数
    PageList = [] # 页码列表

    if files_len % Image_Num != 0:
        pages_len += 1
    for i in range(pages_len):
        PageList.append(f"第{i+1}页({i*Image_Num+1}-{(i+1)*Image_Num})")
    PageList.append("上传")
    page = st.sidebar.selectbox(f"切换页面(共{files_len}项)", PageList)
    for i in PageList:
        if page == "上传":
            Upload_Page()
            break
        if i == page:
            Picture_Page(files[PageList.index(i)*Image_Num:(PageList.index(i)+1)*Image_Num])
            break
# 主函数
def main():
    Page_Select()

if __name__ == "__main__":
    main()

