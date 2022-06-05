import re
import json
from collections import defaultdict
import nltk

file_name = 't5_ex.json'
d = defaultdict(int)

def pos_replaces(tokens):
    for i in range(len(tokens)):
        tokens[i] = list(tokens[i])
        if tokens[i][1] == 'CC':
            tokens[i][1] = "*coordinating conjunction>"
        elif tokens[i][1] == 'CD':
            tokens[i][1] = "*number>"
        elif tokens[i][1] == 'DT':
            tokens[i][1] = "*determiner>"
        elif tokens[i][1] == 'EX':
            tokens[i][1] = "*existential>"
        elif tokens[i][1] == 'FW':
            tokens[i][1] = "*foreign>"
        elif tokens[i][1] == 'IN':
            tokens[i][1] = "*preposition>"
        elif tokens[i][1] == 'JJ':
            tokens[i][1] = "*adjective>"
        elif tokens[i][1] == 'JJR':
            tokens[i][1] = "*comparative adjective>"
        elif tokens[i][1] == 'JJS':
            tokens[i][1] = "*superlative adjective>"
        elif tokens[i][1] == 'LS':
            tokens[i][1] = "*list item>"
        elif tokens[i][1] == 'MD':
            tokens[i][1] = "*modal>"
        elif tokens[i][1] == 'NN' or tokens[i][1] == 'NNP':
            tokens[i][1] = "*singular noun>"
        elif tokens[i][1] == 'NNS' or tokens[i][1] == 'NNPS':
            tokens[i][1] = "*plural noun>"
        elif tokens[i][1] == 'PDT':
            tokens[i][1] = "*predeterminer>"
        elif tokens[i][1] == 'POS':
            tokens[i][1] = "*possesive ending>"
        elif tokens[i][1] == 'PRP':
            tokens[i][1] = "*pronoun>"
        elif tokens[i][1] == 'PRP$':
            tokens[i][1] = "*possessive pronoun>"
        elif tokens[i][1] == 'RB':
            tokens[i][1] = "*adverb>"
        elif tokens[i][1] == 'RBR':
            tokens[i][1] = "*comparative adverb>"
        elif tokens[i][1] == 'RBS':
            tokens[i][1] = "*superlative adverb>"
        elif tokens[i][1] == 'RP':
            tokens[i][1] = "*particle>"
        elif tokens[i][1] == 'SYM':
            tokens[i][1] = "*symbol>"
        elif tokens[i][1] == 'TO':
            tokens[i][1] = "*to>"
        elif tokens[i][1] == 'UH':
            tokens[i][1] = "*interjection>"
        elif tokens[i][1] == 'VB':
            tokens[i][1] = "*verb base form>"
        elif tokens[i][1] == 'VBD':
            tokens[i][1] = "*verb past tense>"
        elif tokens[i][1] == 'VBG':
            tokens[i][1] = "*verb present participle>"
        elif tokens[i][1] == 'VBN':
            tokens[i][1] = "*verb past participle>"
        elif tokens[i][1] == 'VBP' or tokens[i][1] == 'VBZ':
            tokens[i][1] = "*verb present tense>"
        elif tokens[i][1] == 'WDT':
            tokens[i][1] = "*WH determiner>"
        elif tokens[i][1] == 'WP' or tokens[i][1] == 'WP$':
            tokens[i][1] = "*WH pronoun>"
        elif tokens[i][1] == 'WRB':
            tokens[i][1] = "*WH adverb>"
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

nltk.download('averaged_perceptron_tagger')

def preprocess_text(text):
    texta = text[0][0]; textb = text[0][1]
    texta = texta.replace("??? ", "")
    texta = texta.replace(" th e ", " the ")
    texta = texta.replace("part - time", "part-time")
    texta = texta.replace(" : ", " ")
    texta = texta.replace(" - - ", " -- ")
    texta = texta.replace("free - time", "free-time")
    texta = texta.replace("second - hand", "second-hand")
    textc = texta.replace("*", "")
    tokens = textc.split(" ")
    tokens = nltk.pos_tag(tokens)
    tokens = pos_replace(tokens)
    text = texta.split(" ")
    pos_list = []
    for i in range(len(text)):
        '''
        if tokens[i][1] == '':
            rtext = tokens[i][0]
        else:
            rtext = "*"+tokens[i][1]+">"+tokens[i][0]
        '''
        rtext = tokens[i][0]
        pos_token = tokens[i][1]
        if text[i][-1] == '*':
            rtext = rtext + "[EOE]"
            pos_token = pos_token + "[EOE]"
        if text[i][0] == '*':
            rtext = "[BOE]" + rtext
            pos_token = "[BOE]"+pos_token
        text[i] = rtext
        pos_list.append(pos_token)
    texta = " ".join(text)
    textc = " ".join(pos_list)
    #texta = texta.replace("*", "[POE]")
    #textb = textb.replace('*', '<')
    textb = textb.replace(">..", ">.")
    textb = textb.replace("into into", "into")
    textb = textb.replace("’", "'")
    textb = textb.replace("‘", "'")
    textb = textb.replace("*verb 'to be'>", "*verb> 'to be'")
    textb = textb.replace("*base form> of a *verb>", "*base form of the verb>")
    textb = textb.replace("*base form> of a verb>", "*base form of the verb>")
    textb = textb.replace("*base form of a verb>", "*base form of the verb>")
    textb = textb.replace("base form of a *verb>", "*base form of the verb>")
    textb = textb.replace("base form of a verb", "base form of the verb")
    texta = texta + " POS information: " + textc
    return texta, textb

with open('/Users/Naoya/Downloads/train_dev/feedback_train_t5a.json') as trains, open('/Users/Naoya/Downloads/train_dev/feedback_train_'+file_name, 'w') as o_file:
    train = trains.readlines()
    lines = []
    for line in train:
        text = re.findall(r'{"translation": {"input": "Generate a feedback comment for language learners: ?(.*)", "Feedbackcomment": "?(.*)"}}', line)
        texta, textb = preprocess_text(text)
        lines.append({"translation": {"input": "Generate a feedback comment: "+texta, "Feedbackcomment": textb}})
    for line in lines:
        print(json.dumps(line, ensure_ascii=False), file=o_file)

with open('/Users/Naoya/Downloads/train_dev/feedback_dev_t5a.json') as trains, open('/Users/Naoya/Downloads/train_dev/feedback_dev_'+file_name, 'w') as o_file:
    train = trains.readlines()
    lines = []
    for line in train:
        text = re.findall(r'{"translation": {"input": "Generate a feedback comment for language learners: ?(.*)", "Feedbackcomment": "?(.*)"}}', line)
        texta, textb = preprocess_text(text)
        lines.append({"translation": {"input": "Generate a feedback comment: "+texta, "Feedbackcomment": textb}})
    for line in lines:
        print(json.dumps(line, ensure_ascii=False), file=o_file)

with open('/Users/Naoya/Downloads/train_dev/feedback_test_t5a.json') as trains, open('/Users/Naoya/Downloads/train_dev/feedback_test_'+file_name, 'w') as o_file:
    train = trains.readlines()
    lines = []
    for line in train:
        text = re.findall(r'{"translation": {"input": "Generate a feedback comment for language learners: ?(.*)", "Feedbackcomment": "?(.*)"}}', line)
        texta, textb = preprocess_text(text)
        lines.append({"translation": {"input": "Generate a feedback comment: "+texta, "Feedbackcomment": textb}})
    for line in lines:
        print(json.dumps(line, ensure_ascii=False), file=o_file)

