import re
import nltk
from word_forms.word_forms import get_word_forms
import gensim
model = gensim.models.KeyedVectors.load_word2vec_format('/Users/Naoya/Downloads/GoogleNews-vectors-negative300.bin', binary=True)

with open('/Users/Naoya/Downloads/t5_final_answer') as answer, open('/Users/Naoya/Downloads/train_dev-2/feedback_test_final.json') as texts, open('/Users/Naoya/Downloads/train_dev-2/TEST.prep_feedback_comment.public.tsv') as test, open('/Users/Naoya/Downloads/TEST.prep_feedback_comment.output.tsv', 'w') as o_file:
    ans = answer.readlines()
    txt = texts.readlines()
    test = test.readlines()
    id_num = ""
    text = ""
    pred = ""
    for i in range(len(ans)):
        line = ans[i].strip()
        line = line.replace('*', '<')
        if i%2 == 0:
            id_num = str(int(i/2))
            text = txt[int(i/2)].strip()
            words = test[int(i/2)].strip()
            words = words.split("\t")
            words_text = words[0].split(" ")
            text = re.findall(r'{"translation": {"input": "?(.*)", "Feedbackcomment": "?.*"}}', text)[0]
            pred = line
            pred_tok = re.findall(r'<<(.*?)>>', pred)
            for tok in pred_tok:
                tok_s = tok.split(" ")
                if tok in words[0]:
                    continue
                tok = tok.lower()
                if tok in words[0]:
                    print(line)
                    continue
                word_form = get_word_forms(tok)
                tok_bool = False
                for word in word_form['n']:
                    if word in words[0]:
                        tok_bool = True
                for word in word_form['a']:
                    if word in words[0]:
                        tok_bool = True
                for word in word_form['v']:
                    if word in words[0]:
                        tok_bool = True
                for word in word_form['r']:
                    if word in words[0]:
                        tok_bool = True
                if tok not in words[0]:
                    if tok.capitalize() in words[0]:
                        pred = pred.replace("<<"+tok+">>", "<<"+tok.capitalize()+">>")
                        print(line)
                        print(pred)
                        continue
                    if tok.lower() in words[0]:
                        continue
                    if len(tok_s) >= 2:
                        continue
                    for b in words_text:
                        calc = model.most_similar(positive=[tok], topn=10)
                    for c in calc:
                        if c[0] in words_text:
                            pred = pred.replace("<<"+tok+">>", "<<"+c[0]+">>")
                            tok_bool = True
                            break
                    if tok_bool:
                        continue
                    print(pred)
                    pred = "<NO_COMMENT>"
                    
        else:
            print(f"{words[0]}\t{words[1]}\t{pred}", file=o_file)



    