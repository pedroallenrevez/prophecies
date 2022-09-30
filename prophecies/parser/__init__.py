def parse(s):
    from .grammar import ROOT

    toks = ROOT.many().parse(s)
    return toks
