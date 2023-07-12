from . import pyballcools
import pysam

class BAllCFile:
    def __init__(self, ballc_file, cmeta_file=None):
        self.bci = pyballcools.BAllCIndex(ballc_file)
        self.tbi = pysam.TabixFile(cmeta_file) if cmeta_file is not None else None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _fetch_with_cmeta(self, chrom, start, end):
        mciter = self.bci.QueryMcRecords_Iter(chrom, start, end)
        if mciter.HasNext():
            mciter.Next()
        while mciter.HasNext():
            rec = mciter.Next()
            try:
                cline = next(self.tbi.fetch(rec.chrom,rec.pos-1,rec.pos,))
            except:
                ##TODO
                pass

            *_, strand, context = cline.split()

            yield(rec.chrom,rec.pos,strand, context, rec.mc,rec.cov, )

    def _fetch(self, chrom, start, end):
        mciter = self.bci.QueryMcRecords_Iter(chrom, start, end)
        if mciter.HasNext():
            mciter.Next()
        while mciter.HasNext():
            rec = mciter.Next()
            yield(rec.chrom, rec.pos, rec.mc, rec.cov, )
        
    def fetch(self, chrom, start, end):
        if self.tbi is None:
            return self._fetch(chrom, start, end)
        else:
            return self._fetch_with_cmeta(chrom, start, end)
    def fetch_line(self, chrom, start, end):
        if self.tbi is None:
            mciter = self._fetch(chrom, start, end)
            for rec in mciter:
                yield('{}\t{}\t{}\t{}'.format(*rec))
        else:
            mciter = self._fetch_with_cmeta(chrom, start, end)
            for rec in mciter:
                yield('{}\t{}\t{}\t{}\t{}\t{}'.format(*rec))


