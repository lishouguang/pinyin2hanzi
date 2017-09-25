# coding: utf-8

"""
构建训练数据

米家的忠实粉丝，这是第五次买米家的手机了，希望这次也是棒棒哒。
=>
mijiadezhongshifensi	米_家__的_忠____实__粉__丝_
zheshidiwucimaimijiadeshoujile	这__是__第_五_次_买__米_家__的_手___机_了_
xiwangzheciyeshibangbangda	希_望___这__次_也_是__棒___棒___哒_

"""

from __future__ import print_function

import os
import re
import pickle
import codecs
import logging
from collections import Counter

from pypinyin import lazy_pinyin
from pypinyin.constants import RE_HANS
from pypinyin.utils import simple_seg

from p2h.parameters import Parameters

logger = logging.getLogger(__file__)


def build_corpus(corpus_file=Parameters.raw_corpus_file, data_file=Parameters.train_data_file):
    hzCounter = Counter()

    '''遍历语料，生成拼音/汉字序列，统计汉字字频'''
    with codecs.open(data_file, 'w', 'utf-8') as f:
        for i, line in enumerate(iter_file(corpus_file)):
            if i % 10000:
                logger.info('Have process {} lines.'.format(i))

            try:
                line = clean(line).lower()

                # 拆分短句
                for sent in re.split(r'[，。？！?,]', line):
                    if sent:
                        pnyns, hanzis, chars = build_data(sent)
                        f.write(u"{}\t{}\n".format(pnyns, hanzis))
                        hzCounter.update(chars)
            except Exception:
                logger.exception('align pinyin/hanzi error.')

    SYMBOL_EMPTY = 'E'
    SYMBOL_UNKNOW = 'U'
    SYMBOL_BLANK = 'B'

    '''
    build hanzi vocab
    '''
    # 删除低频字
    hanzis = [hanzi for hanzi, cnt in hzCounter.items() if cnt > Parameters.min_hanzi_count]
    if '_' in hanzis:
        hanzis.remove("_")

    # 0: empty, 1: unknown, 2: blank
    hanzis = [SYMBOL_EMPTY, SYMBOL_UNKNOW, SYMBOL_BLANK] + hanzis

    hanzi2idx = {hanzi: idx for idx, hanzi in enumerate(hanzis)}
    idx2hanzi = {idx: hanzi for idx, hanzi in enumerate(hanzis)}

    '''
    build pinyin vocab
    '''
    pnyns = SYMBOL_EMPTY + SYMBOL_UNKNOW + SYMBOL_BLANK + "abcdefghijklmnopqrstuvwxyz0123456789。，！？"
    pnyn2idx = {pnyn: idx for idx, pnyn in enumerate(pnyns)}
    idx2pnyn = {idx: pnyn for idx, pnyn in enumerate(pnyns)}

    with open(Parameters.vocab_data_file, 'wb') as f:
        pickle.dump((pnyn2idx, idx2pnyn, hanzi2idx, idx2hanzi), f)


def build_data(sent):
    """
    解析句子，获得它的拼音/字
    :param sent: 一个短句
    :return: pinyins, hanzis, chars
    """
    tps = tag_pinyin(sent)

    pys = []
    hzs = []
    chars = []
    for tp in tps:
        py = tp[1] if tp[1] is not None else tp[0]
        hz = tp[0] + '_' * (len(py) - len(tp[0]))

        pys.append(py)
        hzs.append(hz)
        chars.append(tp[0])

    py_seq = ''.join(pys)
    hz_seq = ''.join(hzs)

    assert len(py_seq) == len(hz_seq)

    return py_seq, hz_seq, chars


def tag_pinyin(txt):
    """
    标注拼音
    :param txt:
    :return:
    """
    newparts = []

    for part in simple_seg(txt):
        if RE_HANS.match(part):
            pys = lazy_pinyin(part)
            newparts += [_ for _ in zip(part, pys)]
        else:
            for p in re.split(r'([，。？！?,])', part):
                if p:
                    newparts.append((p, None))

    return newparts


def clean(text):
    return text

    # if regex.search("[A-Za-z0-9]", text) is not None: # For simplicity, roman alphanumeric characters are removed.
    #     return ""
    # text = regex.sub(u"[^ \p{Han}。，！？]", "", text)
    # return text


def iter_file(file_path):
    with codecs.open(file_path, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                yield line


if __name__ == "__main__":
    build_corpus()

    print("Done")
