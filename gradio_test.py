import gradio as gr
from yiyan import yiyan_api, get_access_token
import gradio as gr
import os
import time
import random
import structure_article
import shutil
from mdtree import tree2ppt
from PIL import Image
# def image_mod():
#     return Image.open("pptx_static/static/img.png")
def save_knowledge_func(task_name,knowledge_content,mode,sub_num):
    time1= time.time()
    sub_num = int(sub_num)
    rand_seed = str(random.randint(0,10000000000000000000000000000000000000000000000000000))
    character_a = "你是一个精通各方面知识的人"
    struct_article = structure_article.StructureArticle(api_type="yiyan",main_idea_knowledge=knowledge_content,max_sub_idea_num=sub_num,min_sub_idea_num=sub_num)
    content = struct_article.generate_final_summary(task_name,character_a)
    # md_content = read_md_file("./"+task_name+".md")
    if len(os.listdir("./myppt"))>100:
        shutil.rmtree("./myppt")
        os.makedirs("./myppt")

    save_path = "./myppt/test" + rand_seed + ".pptx"
    tree2ppt.Tree2PPT(content,"./my_ppt_mode/"+str(int(mode)),save_path=save_path)

    # download_url = update_file(save_path,update_path)
    print("一共消耗时长：",time.time()-time1)
    return save_path

def gen_requirement(task_name):
    Requirement_prompt = (f"""你是一个专业的需求分析师，很擅长引导人将一个想法从多角度细化。我会给你一个任务或者一个主题，请你通过反问的形式提出针对该任务或主题细化后的几个角度，帮我更加明白我自己的想法。"
                          任务名称:{task_name}
                          输出格式：
                          1.
                          2.
                          3. 
                          """)
    result = yiyan_api(Requirement_prompt, get_access_token())
    return result
# save_knowledge_func("睡前故事",5,1)


with gr.Blocks(title="一键PPT生成") as demo:
    gr.HTML("""<h1 align="center">一键PPT生成</h1>""")
    gr.HTML("""<h2 align="center">基于文心一言 （欧朋智能）</h2>""")
    task_name = gr.Textbox(label="输入你的PPT主题",show_label=True)
    requirement_button1 = gr.Button("分析需求")
    AI_gen_requirement_text = gr.Text(label="AI给出的细化建议",show_label=True)
    requirement_button1.click(fn=gen_requirement,inputs=[task_name],outputs=[AI_gen_requirement_text])
    knowledge_content = gr.Textbox(label="请输入关于PPT主题更细化的一些信息",show_label=True)
    sub_num = gr.Slider(1, 5,value=2,step=1,label="子主题个数",show_label=True)
    mode = gr.Slider(1, 2,value=1,step=1,label="模板选择",show_label=True)
    gen_ppt_button = gr.Button("PPT生成")
    c = gr.File(label="PPT下载",show_label=True)
    gen_ppt_button.click(fn=save_knowledge_func,inputs=[task_name,knowledge_content,mode,sub_num],outputs=[c])



if __name__ == "__main__":
    demo.launch(server_name='127.0.0.1',
                server_port= 2021)

