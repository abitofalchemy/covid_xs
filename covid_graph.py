import os
import pandas as pd
import json
from pprint import pprint
from nltk.tag import pos_tag

# def pretty_json(data):
#     return json.dumps(json.loads(data), indent=2, sort_keys=False)
#
# print([x for x in os.listdir('./') if not ('.' in x)])
## Read json
# js = pd.read_json('./input/wolfram_svo.gv.json',encoding='utf8')

js = json.loads(open('./input/wolfram_svo.gv.json').read())
# print(
#     json.dumps(js, indent=2, sort_keys=False)
# )
# pprint(js)

df = pd.DataFrame(data=js, columns=['t_from','t_to','rel_label'])
# print(df.head())

s_nodes = set(df.t_from)
t_nodes = set(df.t_to)
# print('src nodes',len(s_nodes))
# print('trg nodes',len(t_nodes))

e_labels = list(set(df.rel_label))
# print('edge_label',len(e_labels))
gjson = {}

all_nodes = list(
    set(df.t_from.values.tolist()+
        df.t_to.values.tolist())
)
# print('all nodes:', len(all_nodes))
# print([x for x in all_nodes if 'language' in x])

node_ids={}
for j,node in enumerate(all_nodes):
    node_ids[node] = j

# print(node_ids)

edge_id = 0
for s,t,l in js:
    try:
        gjson.setdefault('edges',[]).append({'id': edge_id,
                                         'from_id': node_ids[s],
                                         'label': l,
                                         'trg_id': node_ids[t],
                                         'relxn': 'inferred'})
    except Exception as e:
        print(t,s,t)
        print(str(e))
    edge_id += 1


# print(
#     json.dumps(gjson, indent=2, sort_keys=False)
# )
# https://stackoverflow.com/questions/17966554/in-python-nltk-i-am-trying-to-get-parts-of-speech-of-a-word-by-using-pos-tag-bu
#https://becominghuman.ai/natural-language-processing-in-python-3-using-nltk-fd0ff4a0da9b

for t in all_nodes:
    gjson.setdefault('nodes', []).append({'id': node_ids[t],
                                          'term': t,
                                          'pos':  pos_tag([t])[0][1] })

print(
    json.dumps(gjson, indent=2, sort_keys=False)
)