#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/2/26 16:29
# @Author  : Arrow and Bullet
# @FileName: apriori.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/qq_41800366


def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    # return [{1, 3, 4}, {2, 3, 5}, {1, 2, 3, 5}, {2, 5}]


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))


def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


dataSet = loadDataSet()  # 加载的数据集
C1 = createC1(dataSet)  # C1 主要用于supportData中做字典的键
# print(C1)  # [frozenset({1}), frozenset({2}), frozenset({3}), frozenset({4}), frozenset({5})]
D = list(map(set, dataSet))  # 将数据集转化成集合模式
# print(D)  # [{1, 3, 4}, {2, 3, 5}, {1, 2, 3, 5}, {2, 5}]
L1, supportData0 = scanD(D, C1, 0.5)  #
# print(L1)  # [frozenset({5}), frozenset({2}), frozenset({3}), frozenset({1})]
# print(supportData0)  # 结果 {frozenset({1}): 0.5, frozenset({3}): 0.75, frozenset({4}): 0.25, frozenset({2}): 0.75, frozenset({5}): 0.75}


# 这函数的目的是为了下一次做准备，也就是现在是{1}{2}{3} 那么下一次就应该是{1， 2}{1，3}，{2，3}这个意思
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]  # 前k-2个数据
            L2 = list(Lk[j])[:k-2]  # 前k-2个数据
            L1.sort()  # 排序
            L2.sort()
            if L1 == L2:  # 只用合并前 k-2 个数据相同的点，这是非常聪明的一步，非常聪明，减少了很多的遍历量
              retList.append(Lk[i] | Lk[j])
    return retList


def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))
    L1, supportData = scanD(D, C1, minSupport)
    # 计算出第一次的还剩下的列表 以及 每个指对应的支持度
    L = [L1]  # 这里的L变成了列表 目的是为了之后能够保存属于频繁集的元素集
    k = 2
    while len(L[k-2]) > 0:  # 还有剩余元素
        Ck = aprioriGen(L[k-2], k)  # 合并
        Lk, supK = scanD(D, Ck, minSupport)  # 在Ck的基础上计算身下的
        supportData.update(supK)  # 把supK添加到supportData中
        L.append(Lk)
        k += 1
    return L, supportData
#        频繁项集列表 包含哪些频繁项集支持数据的字典


L, supportData = apriori(dataSet)
# print(L)
# print(supportData)


# 对规则进行评估
# 计算规则的可信度以及找到满足最小可信度要求的规则
def calcConf(freqSet, H, supportData, br1, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print(freqSet - conseq, "-->", conseq, "conf:", conf)
            br1.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH
#  返回一个满足最小可信度要求的规则列表


# 生成候选集规则
def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
    m = len(H[0])
    if len(freqSet) > (m + 1):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
        if len(Hmp1) > 1:
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)


#        频繁项集列表 包含哪些频繁项集支持数据的字典 最小可信度阀值
def generateRules(L, supportData, minConf=0.7):
    #  函数遍历L中每个频繁项集并对每个频繁项集创建只包含单个元素集合的列表H1
    bigRuleList = []
    # 因为无法从单元素项集中构建关联规则，所以要从包含两个或者更多元素的项集开始规则构建过程
    for i in range(1, len(L)):  #
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if i > 1:
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList
#   生成一个包含可信度的规则列表


L, supportData = apriori(dataSet, minSupport=0.5)
rules = generateRules(L, supportData, minConf=0.5)
print(rules)