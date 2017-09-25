from __future__ import print_function

import codecs

import distance
import numpy as np
import tensorflow as tf
from p2h.data_load import load_vocab, load_test_data, load_test_string
from p2h.parameters import Parameters as P
from p2h.train import Graph

# from p2h.prepro import *


# Evaluate on testing batches
def main_batches():
    g = Graph(is_training=False)

    # Load data
    nums, X, ys = load_test_data()
    pnyn2idx, idx2pnyn, hanzi2idx, idx2hanzi = load_vocab()

    with g.graph.as_default():
        sv = tf.train.Supervisor()
        with sv.managed_session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
            # Restore parameters
            sv.saver.restore(sess, tf.train.latest_checkpoint(P.logdir));
            print("Restored!")

            # Get model
            mname = open(P.logdir + '/checkpoint', 'r').read().split('"')[1]  # model name

            with codecs.open('eval/{}.csv'.format(mname), 'w', 'utf-8') as fout:
                fout.write("NUM,EXPECTED,{},# characters,edit distance\n".format(mname))

                total_edit_distance, num_chars = 0, 0
                for step in range(len(X) // P.batch_size):
                    num = nums[step * P.batch_size:(step + 1) * P.batch_size]  # number batch
                    x = X[step * P.batch_size:(step + 1) * P.batch_size]  # input batch
                    y = ys[step * P.batch_size:(step + 1) * P.batch_size]  # batch of ground truth strings

                    preds = sess.run(g.preds, {g.x: x})
                    for n, xx, pred, expected in zip(num, x, preds, y):  # sentence-wise
                        # got = "".join(idx2hanzi[str(idx)] for idx in pred)[:np.count_nonzero(xx)].replace("_", "")
                        got = "".join(idx2hanzi[idx] for idx in pred)[:np.count_nonzero(xx)].replace("_", "")
                        edit_distance = distance.levenshtein(expected, got)
                        total_edit_distance += edit_distance
                        num_chars += len(expected)

                        fout.write(u"{},{},{},{},{}\n".format(n, expected, got, len(expected), edit_distance))
                fout.write(u"Total CER: {}/{}={},,,,\n".format(total_edit_distance,
                                                               num_chars,
                                                               round(float(total_edit_distance) / num_chars, 2)))


# For user input test
def main():
    # Load vocab
    pnyn2idx, idx2pnyn, hanzi2idx, idx2hanzi = load_vocab()

    g = Graph(is_training=False)

    with g.graph.as_default():
        sv = tf.train.Supervisor()
        with sv.managed_session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
            # Restore parameters
            sv.saver.restore(sess, tf.train.latest_checkpoint(P.logdir))
            print("Restored!")

            # Get model
            mname = open(P.logdir + '/checkpoint', 'r').read().split('"')[1]
            while True:
                line = input("请输入测试拼音：")
                if len(line) > P.maxlen:
                    print('最长拼音不能超过50')
                    continue
                x = load_test_string(pnyn2idx, line)
                preds = sess.run(g.preds, {g.x: x})
                got = "".join(idx2hanzi[idx] for idx in preds[0])[:np.count_nonzero(x[0])].replace("_", "")
                print(got.replace('U', ''))


if __name__ == '__main__':
    main()
    print("Done")
