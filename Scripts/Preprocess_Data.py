import json
from collections import defaultdict
import nltk
nltk.download('averaged_perceptron_tagger')

def pos_replace(tokens):
    for i in range(len(tokens)):
        tokens[i] = list(tokens[i])
        if tokens[i][0] == ';':
            tokens[i][1] = ';'
        elif tokens[i][0] == '--':
            tokens[i][1] = '--'
        elif tokens[i][0] == '-':
            tokens[i][1] = '-'
        elif tokens[i][0] == '...':
            tokens[i][1] = '...'
        elif tokens[i][0] == "!!":
            tokens[i][1] = "!!"
        elif tokens[i][0] == "???":
            tokens[i][1] = "???"
        tokens[i] = tuple(tokens[i])
    return tokens

def preprocess_text(texta, textb):
    texta = texta.replace("??? ", "")
    texta = texta.replace(" th e ", " the ")
    texta = texta.replace("part - time", "part-time")
    texta = texta.replace(" : ", " ")
    texta = texta.replace(" - - ", " -- ")
    texta = texta.replace("free - time", "free-time")
    texta = texta.replace("second - hand", "second-hand")
    textc = texta.replace("[BOE]", "")
    textc = textc.replace("[EOE]", "")
    tokens = textc.split(" ")
    tokens = nltk.pos_tag(tokens)
    tokens = pos_replace(tokens)
    text = texta.split(" ")
    pos_list = []
    for i in range(len(text)):
        rtext = tokens[i][0]
        pos_token = tokens[i][1]
        if text[i][len(text[i])-5:len(text[i])] == '[EOE]':
            rtext = rtext + "[EOE]"
            pos_token = pos_token + "[EOE]"
        if text[i][0:5] == '[BOE]':
            rtext = "[BOE]" + rtext
            pos_token = "[BOE]"+pos_token
        text[i] = rtext
        pos_list.append(pos_token)
    texta = " ".join(text)
    textc = " ".join(pos_list)
    textb = textb.replace(">..", ">.")
    textb = textb.replace("into into", "into")
    textb = textb.replace("’", "'")
    textb = textb.replace("‘", "'")
    textb = textb.replace('"', "''")
    textb = textb.replace("*verb 'to be'>", "*verb> 'to be'")
    textb = textb.replace("*base form> of a *verb>", "*base form of the verb>")
    textb = textb.replace("*base form> of a verb>", "*base form of the verb>")
    textb = textb.replace("*base form of a verb>", "*base form of the verb>")
    textb = textb.replace("base form of a *verb>", "*base form of the verb>")
    textb = textb.replace("base form of a verb", "base form of the verb")
    texta = texta + " POS_information: " + textc
    return texta, textb

def preprocess_text_test(texta):
    texta = texta.replace("??? ", "")
    texta = texta.replace(" th e ", " the ")
    texta = texta.replace("part - time", "part-time")
    texta = texta.replace(" : ", " ")
    texta = texta.replace(" - - ", " -- ")
    texta = texta.replace("free - time", "free-time")
    texta = texta.replace("second - hand", "second-hand")
    textc = texta.replace("[BOE]", "")
    textc = textc.replace("[EOE]", "")
    tokens = textc.split(" ")
    tokens = nltk.pos_tag(tokens)
    tokens = pos_replace(tokens)
    text = texta.split(" ")
    pos_list = []
    for i in range(len(text)):
        rtext = tokens[i][0]
        pos_token = tokens[i][1]
        if text[i][len(text[i])-5:len(text[i])] == '[EOE]':
            rtext = rtext + "[EOE]"
            pos_token = pos_token + "[EOE]"
        if text[i][0:5] == '[BOE]':
            rtext = "[BOE]" + rtext
            pos_token = "[BOE]"+pos_token
        text[i] = rtext
        pos_list.append(pos_token)
    texta = " ".join(text)
    textc = " ".join(pos_list)
    texta = texta + " POS_information: " + textc
    return texta

with open('/Users/Naoya/Downloads/train_dev-2/TRAIN.prep_feedback_comment.public.tsv', encoding="utf-8") as train, open('/Users/Naoya/Downloads/train_dev-2/feedback_train_final_no.json', 'w', encoding="utf-8") as o_file:
    train_lines = train.readlines()
    lines = []
    for line in train_lines:
        line = line.strip()
        linelist = line.split("\t")
        '''
        if sentence[0] == '"' and sentence[-1] == '"':
            sentence = sentence.strip('"')
            linelist[0] = sentence
        '''
        text = linelist[1].split(":")
        text[0] = int(text[0])
        text[1] = int(text[1])
        linelist[0] = linelist[0][:text[0]]+ "[BOE]" + linelist[0][text[0]:text[1]] + "[EOE]" + linelist[0][text[1]:]
        text = linelist[0].split(" ")
        text = " ".join(text)
        linelist[0] = linelist[0].replace('*', '')
        linelist[2] = linelist[2].replace('*', '')
        linelist[2] = linelist[2].replace('<', '*')
        linelist[2] = linelist[2].replace("`", "'")
        texta, textb = preprocess_text(linelist[0], linelist[2])
        lines.append({"translation": {"input": "Generate a feedback comment: " + texta, "Feedbackcomment": textb}})
    for line in lines:
        print(json.dumps(line, ensure_ascii=False), file=o_file)

with open('/Users/Naoya/Downloads/train_dev-2/TRAIN.prep_feedback_comment.public.tsv', encoding="utf-8") as train, open('/Users/Naoya/Downloads/train_dev-2/feedback_train_final_no.json', 'w', encoding="utf-8") as o_file:
    train_lines = train.readlines()
    lines = []
    for line in train_lines:
        line = line.strip()
        linelist = line.split("\t")
        '''
        if sentence[0] == '"' and sentence[-1] == '"':
            sentence = sentence.strip('"')
            linelist[0] = sentence
        '''
        text = linelist[1].split(":")
        text[0] = int(text[0])
        text[1] = int(text[1])
        linelist[0] = linelist[0][:text[0]]+ "[BOE]" + linelist[0][text[0]:text[1]] + "[EOE]" + linelist[0][text[1]:]
        text = linelist[0].split(" ")
        text = " ".join(text)
        linelist[0] = linelist[0].replace('\*\*\*', '')
        linelist[0] = linelist[0].replace('\\', '')
        linelist[0] = linelist[0].replace('*', '')
        linelist[2] = linelist[2].replace('*', '')
        linelist[2] = linelist[2].replace('<', '*')
        linelist[2] = linelist[2].replace("`", "'")
        texta, textb = preprocess_text(linelist[0], linelist[2])
        lines.append({"translation": {"input": "Generate a feedback comment: " + texta, "Feedbackcomment": textb}})
    for line in lines:
        print(json.dumps(line, ensure_ascii=False), file=o_file)

with open('/Users/Naoya/Downloads/train_dev-2/DEV.prep_feedback_comment.public.tsv', encoding="utf-8") as train, open('/Users/Naoya/Downloads/train_dev-2/feedback_dev_final_no.json', 'w', encoding="utf-8") as o_file:
    train_lines = train.readlines()
    lines = []
    for line in train_lines:
        line = line.strip()
        linelist = line.split("\t")
        '''
        if sentence[0] == '"' and sentence[-1] == '"':
            sentence = sentence.strip('"')
            linelist[0] = sentence
        '''
        text = linelist[1].split(":")
        text[0] = int(text[0])
        text[1] = int(text[1])
        linelist[0] = linelist[0][:text[0]]+ "[BOE]" + linelist[0][text[0]:text[1]] + "[EOE]" + linelist[0][text[1]:]
        text = linelist[0].split(" ")
        text = " ".join(text)
        linelist[0] = linelist[0].replace('\*\*\*', '')
        linelist[0] = linelist[0].replace('\\', '')
        linelist[0] = linelist[0].replace('*', '')
        linelist[2] = linelist[2].replace('*', '')
        linelist[2] = linelist[2].replace('<', '*')
        linelist[2] = linelist[2].replace("`", "'")
        texta, textb = preprocess_text(linelist[0], linelist[2])
        lines.append({"translation": {"input": "Generate a feedback comment: " + texta, "Feedbackcomment": textb}})
    for line in lines:
        print(json.dumps(line, ensure_ascii=False), file=o_file)

with open('/Users/Naoya/Downloads/train_dev-2/TEST.prep_feedback_comment.public.tsv', encoding="utf-8") as train, open('/Users/Naoya/Downloads/train_dev-2/feedback_test_final.json', 'w', encoding="utf-8") as o_file:
    train_lines = train.readlines()
    lines = []
    for line in train_lines:
        line = line.strip()
        linelist = line.split("\t")
        '''
        if sentence[0] == '"' and sentence[-1] == '"':
            sentence = sentence.strip('"')
            linelist[0] = sentence
        '''
        text = linelist[1].split(":")
        text[0] = int(text[0])
        text[1] = int(text[1])
        linelist[0] = linelist[0][:text[0]]+ "[BOE]" + linelist[0][text[0]:text[1]] + "[EOE]" + linelist[0][text[1]:]
        text = linelist[0].split(" ")
        text = " ".join(text)
        linelist[0] = linelist[0].replace('\*\*\*', '')
        linelist[0] = linelist[0].replace('\\', '')
        linelist[0] = linelist[0].replace('*', '')
        #linelist[2] = linelist[2].replace('*', '')
        #linelist[2] = linelist[2].replace('<', '*')
        #linelist[2] = linelist[2].replace("`", "'")
        texta = preprocess_text_test(linelist[0])
        lines.append({"translation": {"input": "Generate a feedback comment: " + texta, "Feedbackcomment": "*NO_COMMENT>"}})
    for line in lines:
        print(json.dumps(line, ensure_ascii=False), file=o_file)