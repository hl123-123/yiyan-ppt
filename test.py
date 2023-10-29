from mdtree.parser import parse_string
from mdtree.tree2ppt import Tree2PPT
from mdtree.utils import read_md_file
import structure_article
if __name__ == '__main__':
    character_a = "你是一个专业的技术学者"
    task_name = "自行车"
############################################
    # 从任务到PPT文字大纲，如果把这一部分代码注释掉，那么直接读取read_md_file的md文件作为文本大纲也行
    struct_article = structure_article.StructureArticle(api_type="yiyan")
    content = struct_article.generate_final_summary(task_name,character_a)
    struct_article.save_content(content,"./my_markdown/"+task_name+".md")
################################################
    #从PPT文字大纲到一份PPT
    md_content = read_md_file("./my_markdown/"+task_name+".md")
    out = parse_string(md_content)
    for i in range(1,3):#i代表不同的模板
        Tree2PPT(md_content,"./my_ppt_mode/"+str(i),save_path="./myppt/"+task_name+"_mode"+str(i)+".pptx")

