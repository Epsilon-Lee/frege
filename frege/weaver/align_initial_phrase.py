import argparse
import ipdb


parser = argparse.ArgumentParser("Get preliminary aligned initial phrases.")
parser.add_argument("--corpus", type=str, required=True,
                    help="Bilingual aligned sentence pairs: e.g."\
                    " I have a cat ||| 我 有 一只 猫.")
parser.add_argument("--align-file", type=str, required=True,
                    help="Path to the alignment file produced by fast_align,"\
                    " with i-j alignment direction. Notice that, alignment"\
                    "should be produced by forward mode, that is many-to-one align.")
parser.add_argument("--save-to", type=str, required=True,
                    help="Path to save extracted pharse pairs.")


# A Hierarchical Phrase-Based Model for Statistical Machine Translation
# http://www.aclweb.org/anthology/P05-1033
def main(args):
    with open(args.save_to, 'w') as f_saveto:
        with open(args.corpus, 'r') as f_corpus:
            with open(args.align_file) as f_align:
                # f_corpus, f_align should have equal line number
                for line, align in zip(f_corpus, f_align):
                    e, f = line.strip().split("|||")
                    e, f = e.strip(), f.strip()
                    e = e.split()  # a list of source tokens
                    f = f.split()
                    e_len = len(e)
                    f_len = len(f)

                    alignments = align.split()  # ['0-2', '1-3', '2-0']
                    align_dict = {}  # j : i or target-source
                    for a in alignments:
                        i, j = a.split('-')
                        i, j = int(i), int(j)
                        if j in align_dict:
                            ipdb.set_trace()
                            raise ValueError("Alignment should be many-to-one,"\
                                    " that is, every target token should only"\
                                    " aligned to one source token.")
                        align_dict[j] = i
                    reverse_align_dict = {}
                    for k, v in align_dict.items():
                        if v in reverse_align_dict:
                            reverse_align_dict[v].append(k)
                        else:
                            reverse_align_dict[v] = [k]

                    indexed_e = ["%d-%s" % (i, e_i) for i, e_i in enumerate(e)]
                    indexed_f = ["%d-%s" % (j, f_j) for j, f_j in enumerate(f)]
                    #print("%s" % " ".join(indexed_e))
                    #print("%s" % " ".join(indexed_f))
                    init_phrases = {}  # m-n : p-q, e[m:n+1] is aligned to f[p:q+1]
                    init_phrases_list = []
                    for start_align_point in alignments:
                        start_i, start_j = start_align_point.split('-')
                        start_i, start_j = int(start_i), int(start_j)
                        m, n, p, q = get_init_phrase(
                                start_i, start_j,
                                align_dict, reverse_align_dict,
                                e_len, f_len)
                        m_n = "%d-%d" % (m, n)
                        p_q = "%d-%d" % (p, q)
                        # filter out repeated phrases
                        if m_n in init_phrases:
                            continue
                        else:
                            init_phrases_list.append("{}:{}".format(m_n, p_q))
                            #print("%d-%d, %d-%d" % (m, n, p, q))
                        init_phrases[m_n] = p_q
                    init_phrases_str = " ".join(init_phrases_list)
                    f_saveto.write(init_phrases_str + '\n')

                    # ipdb.set_trace()


def get_init_phrase(
        start_i, start_j,
        align_dict, reverse_align_dict,
        e_len, f_len):
    """
    Extend start points of source and target i-j, to get the initial phrases
    m-n : p-q, which means phrase e[m:n+1] is aligned to f[p:q+1].

    The principle is that extend j left/right to get the longest target-side
    phrase, and the corresponding source phrase. Both should be no longer than
    10 tokens.

    However, there can be many different phrase pairs in terms of the start_j
    target position.
    """
    m = n = start_i  # m <= n
    p = q = start_j  # p <= q

    def _extend_left(pos):
        j = pos - 1
        if j < 0:
            return -1, -1, -1
        if j in align_dict:
            # check phrase align condition
            return _check(j, j, q)
        else:
            return j, m, n

    def _extend_right(pos):
        j = pos + 1
        if j >= f_len:
            return -1, -1, -1
        if j in align_dict:
            # check phrase align condition
            return _check(j, p, j)
        else:
            return j, m, n

    def _check(new_pos, new_p, new_q):
        new_src_pos = align_dict[new_pos]
        if new_src_pos >= m and new_src_pos <= n:
            return new_pos, m, n
        elif new_src_pos > n:
            # check e[n+1:new_src_pos+1] are aligned between f[new_p:new_q+1]
            for i in range(n + 1, new_src_pos + 1):
                if i in reverse_align_dict:
                    for j in reverse_align_dict[i]:
                        if j > new_q or j < new_p:
                            return -1, -1, -1
            return new_pos, m, new_src_pos
        else:
            # check e[new_src_pos:m] are aligned between f[new_p:new_q+1]
            for i in range(new_src_pos, m):
                if i in reverse_align_dict:
                    for j in reverse_align_dict[i]:
                        if j > new_q or j < new_p:
                            return -1, -1, -1
            return new_pos, new_src_pos, n

    # extend left
    while True:
        new_p, new_m, new_n = _extend_left(p)
        if new_p == -1:
            break
        p = new_p
        m = new_m
        n = new_n
        if (n - m + 1) > (e_len / 2):
            break

    # extend right
    while True:
        new_q, new_m, new_n = _extend_right(q)
        if new_q == -1:
            break
        q = new_q
        m = new_m
        n = new_n
        if (n - m + 1) > (e_len / 2):
            break

    return m, n, p, q


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
