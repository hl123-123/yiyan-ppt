import embedding
import yiyan
import re



#最简单的自定义异常
class API_Type_Error(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self) #初始化父类
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo

class StructureArticle():
    def __init__(self,api_type,min_sub_idea_num=2,max_sub_idea_num=10,use_knowledge=False,**kwargs):
        self.use_knowledge =use_knowledge
        self.min_sub_idea_num = min_sub_idea_num
        self.max_sub_idea_num = max_sub_idea_num
        if kwargs.get("main_idea_knowledge"):
            self.main_idea_knowledge = kwargs["main_idea_knowledge"]
            self.sentence_knowledge_list=[self.main_idea_knowledge]
        else:
            self.main_idea_knowledge = " "
        if kwargs.get("sentence_knowledge_list"):
            self.sentence_knowledge_list = kwargs.get("sentence_knowledge_list")
        self.all_api_type = ["yiyan"]
        if api_type in self.all_api_type:
            self.api_type = api_type
        else:
            raise API_Type_Error(f"{api_type}not in{' '.join(self.all_api_type)},请重新选择api调用的类型")

        pass

    def get_main_idea(self,task_name, character_a, knowledge_content="None", language="Chinese"):
        if self.api_type=="yiyan":
            messages = f"""你是一个”{character_a}“，你可以基于一个任务生成具体的中心主题。无论输入语言是什么，您都必须用{language}输出文本。
            这里有一个任务”{task_name}“,请你基于我给你的参考内容针对该任务生成该任务类型文章的中心主题,如果参考内容无信息参考，则生成主题符合任务即可。\n\n参考内容：\n{knowledge_content}\n\n请你生成的主题更具体。要有创造力和想象力。回复字数在50字以内。不要添加任何其他内容。
            """

            yiyan_access_token = yiyan.get_access_token()
            out_str = yiyan.yiyan_api(messages,yiyan_access_token)
        return out_str
    def get_title_name(self,main_idea,language="Chinese"):
        if self.api_type=="yiyan":
            messages = f"""你是一个”标题生成小助手“，你可以基于具体的中心主题提炼出对应的标题。无论输入语言是什么，您都必须用{language}输出文本。
            这里有一个中心主题”{main_idea}“,请你基于中心主题提炼出对应的标题,要求回复字数在15字以内。不要添加任何其他内容。
            """

            yiyan_access_token = yiyan.get_access_token()
            out_str = yiyan.yiyan_api(messages,yiyan_access_token)
        return out_str
    def get_first_sentence(self,task_name, main_idea, character_a, knowledge_content="None", language="Chinese"):
        if self.api_type=="yiyan":
            messages = f"""你是一个{character_a}。请你基于我给你的参考内容根据我给你布置的任务和中心主题，进行文章第一段的内容创作，如果参考内容无信息参考，则生成主题符合任务即可。\n\n参考内容：\n{knowledge_content}\n\n。无论输入语言是什么，您都必须用{language}输出文本。\n输出要求如下:\n
        1.  要求展示在该领域的专业知识。
        2.  要求内容丰富，引导全文。
        3.字数要求200字左右
        请基于任务”{task_name}“和中心主题”{main_idea}“进行文章第一段的创作.
            """

            yiyan_access_token = yiyan.get_access_token()
            output_str = yiyan.yiyan_api(messages,yiyan_access_token)
        return output_str

    def get_muti_sub_idea(self,task_name, main_idea, character_a, first_sentence, knowledge_content="None",
                          language="Chinese"):
        if self.api_type=="yiyan":
            messages = f"""你是一个{character_a}。请你基于我给你的参考内容根据我给你的任务名称，中心主题，第一段内容，将中心主题分解为多个子主题，要求按照逻辑顺序先后排列。\n\n参考内容：\n{knowledge_content}\n\n。无论输入语言是什么，您都必须用{language}输出文本。
            任务名称为“{task_name}”，中心主题为“{main_idea}”,文章的第一个段落内容为“{first_sentence}”。请你将中心主题分解为多个子主题，作为文章的观点。要求内容简洁.每个子主题字数少于15字。格式为:\n1. \n2. 
            """

            yiyan_access_token = yiyan.get_access_token()
            output_str = yiyan.yiyan_api(messages,yiyan_access_token)
        return output_str

    def get_sublist(self,text):
        pattern = r'(\d+\.\s.*?)(?=\d+\.|\Z)'
        matches = re.findall(pattern, text, re.DOTALL)
        matches = [i.strip() for i in matches]
        return matches

    def get_sub_content(self,task_name, main_idea, sub_idea, character_a, knowledge_content="None", language="Chinese"):
        if self.api_type == "yiyan":
            messages = f"""：你是一个{character_a}。请你根据我给你布置的任务,中心主题,基于该部分子主题生成一整个段落的具体内容，作为整篇文章的一部分。\n\n可参考内容：\n{knowledge_content}\n\n。无论输入语言是什么，您都必须用{language}输出文本。
                请基于任务“{task_name}”，中心主题“{main_idea}”这些背景信息，针对该部分“{sub_idea}”的子主题，请直接输出对应的具体段落内容，要求200字，意思表述完整，不要分条输出，不要其他任何内容。
                """

            yiyan_access_token = yiyan.get_access_token()
            output_str = yiyan.yiyan_api(messages, yiyan_access_token)
        return output_str

    def get_end_sentence(self,task_name, main_idea, first_sentence, sub_idea, character_a, language="Chinese"):
        if self.api_type == "yiyan":
            messages = f"""：你是一个{character_a}。请你基于我给你的参考内容根据任务名称，文章的中心主题，第一段落内容，文章主要内容，进行文章最后一段的内容创作，要求与首段进行呼应。无论输入语言是什么，您都必须用{language}输出文本。
                请根据“{task_name}”的任务名称，“{main_idea}”的中心主题，“{sub_idea}”的文章内容，“{first_sentence}”的首段内容，进行文章内容的收尾，要求生成的结尾与文章第一段内容进行首尾呼应，要求200字。
                """

            yiyan_access_token = yiyan.get_access_token()
            output_str = yiyan.yiyan_api(messages, yiyan_access_token)
        return output_str

    def generate_final_summary(self,task_name="写一篇总结",character_a = "你是一个专业的学者"):
        article_summary = self.main_idea_knowledge
        main_idea = self.get_main_idea(task_name, character_a, knowledge_content=article_summary)
        title_name = self.get_title_name(main_idea)
        all_content = ""
        all_content += "# "+title_name+"\n"
        print("中心主题:", main_idea)
        print("标题:",title_name)
        print("======================")
        first_sentence = self.get_first_sentence(task_name, main_idea, character_a, knowledge_content=article_summary)
        all_content += "\n## 引文\n\n" + first_sentence
        print("首段：", first_sentence)
        sub_ideas_list = []
        while True:
            sub_ideas = self.get_muti_sub_idea(task_name, main_idea,character_a,first_sentence, knowledge_content=article_summary)
            sub_ideas_list += self.get_sublist(sub_ideas)
            if len(sub_ideas_list) >= self.min_sub_idea_num:
                break
        sub_ideas_list_new = []
        for sub_idea in sub_ideas_list:#重新编号
            sub_idea_new = ".".join(sub_idea.split(".")[1:])
            sub_idea_new = str(len(sub_ideas_list_new)+1)+"."+sub_idea_new
            sub_ideas_list_new.append(sub_idea_new)
        sub_ideas_list = sub_ideas_list_new[:self.max_sub_idea_num]
        print("一共子主题个数：",len(sub_ideas_list))
        print("===============================")
        if self.use_knowledge:
            sub_paragraph_embedding_list = []
            for sub_paragraph in self.sentence_knowledge_list:
                sub_paragraph_embedding_list.append(embedding.get_embedding(sub_paragraph))
        for sub_idea_i in sub_ideas_list:
            print(sub_idea_i)
            print("------------------------------------------------------------------------------")
            all_content += "\n\n## " + sub_idea_i
            if self.use_knowledge:
                sub_knowledge_content = embedding.answer_question(sub_idea_i,self.sentence_knowledge_list,sub_paragraph_embedding_list)[0]
            else:
                sub_knowledge_content = " "
            sub_content = self.get_sub_content(task_name, main_idea, sub_idea_i, character_a, knowledge_content=sub_knowledge_content)
            all_content += "\n\n" +sub_content
            print(sub_content)
            print("----------------------------")
        end_sentence = self.get_end_sentence(task_name, main_idea, first_sentence, sub_ideas, character_a)
        print("===============================")
        all_content += "\n\n## 总结\n\n"+end_sentence
        print("结尾：", end_sentence)
        return all_content

    def save_content(self,content,save_path):
        with open(save_path, mode="w+", encoding="utf-8") as f:
            f.write(content)





if __name__ =="__main__":
    character_a = "你是一个资深的技术专家"
    task_name = "AI的未来"
    struct_article = StructureArticle(api_type="yiyan")
    content = struct_article.generate_final_summary(task_name,character_a)
    struct_article.save_content(content,task_name+".md")
