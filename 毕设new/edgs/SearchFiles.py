import math


class BM25(object):

    def __init__(self, docs):
        self.D = len(docs)
        self.avgdl = sum([len(doc)+0.0 for doc in docs]) / self.D
        self.docs = docs
        self.f = []  # 列表的每一个元素是一个dict，dict存储着一个文档中每个词的出现次数
        self.df = {} # 存储每个词及出现了该词的文档数量
        self.idf = {} # 存储每个词的idf值
        self.k1 = 1.5
        self.b = 0.75
        self.init()

    def init(self):
        for doc in self.docs:
            tmp = {}
            for word in doc:
                tmp[word] = tmp.get(word, 0) + 1  # 存储每个文档中每个词的出现次数
            self.f.append(tmp)
            for k in tmp.keys():
                self.df[k] = self.df.get(k, 0) + 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D-v+0.5)-math.log(v+0.5)

    def sim(self, doc, index):
        score = 0
        for word in doc:
            if word not in self.f[index]:
                continue
            d = len(self.docs[index])
            score += (self.idf[word]*self.f[index][word]*(self.k1+1)
                      / (self.f[index][word]+self.k1*(1-self.b+self.b*d
                                                      / self.avgdl)))
        return score

    def simall(self, doc):
        scores = []
        for index in range(self.D):
            score = self.sim(doc, index)
            scores.append(score)
        return scores
    
if __name__ == '__main__':

    from MyDataFrame import MyDataFrame
    mdf = MyDataFrame()
    df = mdf.new_DataFrame()
    df2 = mdf.m_cut(df)
    filelist=[]
    for i in range(len(df2)):
        filelist.append(df2['fenci'][i])
    
    
    s = BM25(filelist)
    #print(s.f)
    #print(s.idf)
    #print(s.simall(['医疗机构', '数据挖掘', '领域', '一带一路', '领域']))
    #print(type(s.simall(['医疗机构', '数据挖掘', '领域', '一带一路', '领域'])))
    scores = s.simall(['医疗机构'])
    #scores.sort()
    print(scores)
    simfile_list = []
    for i in range(len(scores)):
        simfile_list.append((i,scores[i]))
        
    import operator
    
    simfile_list.sort(key=operator.itemgetter(1),reverse=True)
    print(simfile_list)
    
    for i in range(len(simfile_list)):
        a,b = simfile_list[i]
        if b != 0:
            print(df.filename[a] +":"+str(b))