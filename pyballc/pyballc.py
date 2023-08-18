# from . import pyballcools
import os.path
from .pyballcools import (
    BAllCIndex,
    BAllC,
    IndexBallc,
    AllCToBallC,
    BAllCToAllC,
    ExtractCMeta,
    IndexCMeta
)
#pip install pytabix
# import tabix #
import pysam
import fire

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
        self.bci = BAllCIndex(ballc_file)
        # self.tbi = tabix.open(cmeta_file)  if cmeta_file is not None else None
        self.tbi = pysam.TabixFile(cmeta_file) if cmeta_file is not None else None
        self.ballc=BAllC(ballc_file,"r")

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
                print(f"No meta data found for {rec.chrom}:{rec.pos-1}-{rec.pos}",end="\r")

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

def Ballc2Allc(ballc_path=None,cmeta_path=None,
               allc_path=None,warn_mismatch=True,
               err_mismatch=True,skip_mismatch=True,
               c_context="*"):
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
    warn_mismatch: bool
        warn_mismatch
    err_mismatch: bool
        err_mismatch
    skip_mismatch: bool
        skip_mismatch
    c_context: str
        c_context

    Returns
    -------

    """
    # bf = BAllCFile(ballc_path, cmeta_path)
    # allc_path=bf.to_allc(allc_path)
    BAllCToAllC(ballc_path, cmeta_path, allc_path,
                 warn_mismatch, err_mismatch, skip_mismatch,
                 c_context)
    return allc_path

def index_ballc(ballc_path):
    IndexBallc(ballc_path)

def Allc2Ballc(allc_path=None,ballc_path=None,chrom_size_path=None,
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
    AllCToBallC(allc_path,ballc_path,chrom_size_path,
                assembly_text,header_text,sc)
    index_ballc(ballc_path)
    return ballc_path

def extractC(fasta_path=None,cmeta_path=None):
    """
    Extract all C position from fasta file.

    Parameters
    ----------
    fasta_path: str
        path for fasta file
    cmeta_path: str
        path for the output cmeta file.

    Returns
    -------

    """
    ExtractCMeta(fasta_path, cmeta_path)
    IndexCMeta(cmeta_path)
    return cmeta_path

def header(ballc_path=None,cmeta_path=None):
    bf = BAllCFile(ballc_path, cmeta_path)
    header_dict=bf.header()
    for key in header_dict:
        value=header_dict[key]
        print(f"{key}: {value}")

def main():
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire({
        "cmeta":extractC,
        "b2a":Ballc2Allc,
        "a2b":Allc2Ballc,
        "header":header
    })

if __name__=="__main__""" :
    main()