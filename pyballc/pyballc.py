# from . import pyballcools
import os.path
import pyballcools
#pip install pytabix
# import tabix #
import pysam

class BAllCFile:
    def __init__(self, ballc_file, cmeta_file=None):
        """
        Python warpper of BallCFile

        Parameters
        ----------
        ballc_file: str
            path for ballc file (should be indexed)
        cmeta_file: str
            path for cmeta file ((should be indexed))
        """
        self.bci = pyballcools.BAllCIndex(ballc_file)
        # self.tbi = tabix.open(cmeta_file)  if cmeta_file is not None else None
        self.tbi = pysam.TabixFile(cmeta_file) if cmeta_file is not None else None
        self.ballc=pyballcools.BAllC(ballc_file,"r")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def header(self):
        if hasattr(self,'header_dict'):
            return self.header_dict
        self.header_dict={}
        attrs = ['version_minor', 'sc', 'assembly_text', 'l_assembly', 'header_text', 'l_text', 'refs', 'n_refs']
        for attr in attrs:
            # print(attr, self.ballc.header.__getattribute__(attr))
            self.header_dict[attr]=self.ballc.header.__getattribute__(attr)
        return self.header_dict

    def _fetch_with_cmeta(self, chrom, start, end):
        if chrom=="*":
            mciter = self.bci.QueryMcRecords_Iter("*")
        else:
            mciter = self.bci.QueryMcRecords_Iter(chrom, start, end)
        if mciter.HasNext():
            mciter.Next()
        while mciter.HasNext():
            rec = mciter.Next()
            try:
                record = next(self.tbi.fetch(rec.chrom,rec.pos-1,rec.pos,)).split()
                # record = next(self.tbi.query(rec.chrom,rec.pos-1,rec.pos))
                *_, strand, context = record
                yield(rec.chrom,rec.pos,strand, context, rec.mc,rec.cov, )
            except:
                print(f"No meta data found for {rec.chrom}:{rec.pos-1}-{rec.pos}")

    def _fetch(self, chrom, start, end):
        if chrom=="*":
            mciter = self.bci.QueryMcRecords_Iter("*")
        else:
            mciter = self.bci.QueryMcRecords_Iter(chrom, start, end)
        if mciter.HasNext():
            mciter.Next()
        while mciter.HasNext():
            rec = mciter.Next()
            yield(rec.chrom, rec.pos, rec.mc, rec.cov, )

    def fetch(self, chrom, start, end):
        """
        Fetch region from ballc.
        Parameters
        ----------
        chrom: str
            chromsome name,  if chrom=="*", fetch all records.
        start: int
            start position, could be None if chrom=='*'
        end: int
            end position, could be None if chrom=='*'

        Returns
        -------
        a generator containing the records.
        """
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

    def to_allc(self,allc_path):
        allc_path=os.path.abspath(os.path.expanduser(allc_path))
        f=open(allc_path,'w')
        for line in self.fetch_line("*",None,None):
            f.write(line+"\n")
        f.close()
        return allc_path

def BAllCToAllC(ballc_path,cmeta_path,allc_path):
    """
    Convert ballc file into allc path.

    Parameters
    ----------
    ballc_path: str
        input ballc path, should be indexed
    cmeta_path:str
        path
    allc_path: str
        output allc file

    Returns
    -------

    """
    bf = BAllCFile(ballc_path, cmeta_path)
    allc_path=bf.to_allc(allc_path)
    return allc_path

def IndexBallc(ballc_path):
    pyballcools.IndexBallc(ballc_path)

def AllcToBallC(allc_path,ballc_path,chrom_size_path,
                assembly_text="",header_text="",sc=True):
    """
    Convert allc file into ballc file.

    Parameters
    ----------
    allc_path: str
        input allc file path.
    ballc_path: str
        output ballc path, will be indexed automatically.
    chrom_size_path: str
        path
    assembly_text: str
        text to be added
    header_text: str
        text to be added
    sc: bool
        whether single cell file?

    Returns
    -------

    """
    pyballcools.AllCToBallC(allc_path,ballc_path,chrom_size_path,
                assembly_text,header_text,sc)
    IndexBallc(ballc_path)
    return ballc_path

def test():
    ballc_file = '/anvil/scratch/x-wding2/Projects/pyballc/test.ballc'
    cmeta_file = '/anvil/scratch/x-wding2/Projects/pyballc/h1930001.cmeta.gz'

    # test ballc to allc
    bf = BAllCFile(ballc_file, cmeta_file)
    for x in bf.fetch('chr1', 0, 80000):
        print(x)
    bf.to_allc("test.allc.txt")

    # test allc to ballc
    allc_path = "/anvil/scratch/x-wding2/Projects/pyballc/Pool179_Plate1-1-I3-A14.allc.tsv.gz"
    ballc_path = "test.ballc"
    chrom_size_path = os.path.expanduser("~/Ref/mm10/mm10_ucsc_with_chrL.chrom.sizes")
    assembly_text = "test"
    header_text = "header_test"
    sc = True
    AllcToBallC(allc_path, ballc_path, chrom_size_path,
                assembly_text, header_text, sc)

    bf = BAllCFile("test.ballc", cmeta_file)
    # bf.to_allc("test.allc.txt")

    chrom, start, end = "chrX", 4885350, 4885424
    for x in bf.fetch(chrom, start, end):
        print(x)
        break

if __name__=="__main__":
    pass