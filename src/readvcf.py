#!/usr/bin/python

import sys
import os
import argparse
import getopt
import pybedtools
import array

#class Error(Exception):
#    """Base-class for exceptions in this module."""

#class UsageError(Error):
#    def __init__(self, msg):
#        self.msg = msg

def main(argv):
    inputfile = ''
    #outputfile = ''
    vcf = ''

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--vcf", type=str, dest="vcf", help="Input variant file (vcf)", required=True)
    parser.add_argument("-o", "--output", type=str, dest="out", help="Output file (tabular)", required=True)
    parser.add_argument("-v", "--verbosity", action="count", default=0)

    args = parser.parse_args()

    if args.verbosity >= 2:
        print "{} to the power {} equals {}".format(args.v, args.o, answer)
    elif args.verbosity >= 1:
        print "{}^{} == {}".format(args.x, args.y, answer)
    #else:
    #    print "Starting ..."

    avcf = pybedtools.BedTool(args.vcf)
    outputfile = open(args.out, "w")
    current_info = avcf[0][7]
    info = current_info.split("ANN=")
    ann = info[1].split("|")

    #current_chr, current_pos, current_annotation, current_feature_type, current_gene_name,\
    #        current_LOF, current_exon, current_aa_pos, current_vep_sift, current_vep_polyphen, current_vep_eur_maf = "."

    #print "chr\tpos\tannotation\tfeature_type\tgene_name\tlof\texon\taa_pos\tpoly/sift\teur_maf"
    outputfile.write("chr\tpos\tannotation\tfeature_type\tgene_name\tlof\texon\taa_pos\tpoly/sift\teur_maf")

    for x in xrange(0, len(avcf)):
        current_chr = avcf[x][0]
        current_pos = avcf[x][1]
        current_info = avcf[x][7]

        #checkInfoForVepAnnotaion(current_info)
        # VEP
        if "CSQ=" in current_info:
            info_vep = current_info.split("CSQ=")
            csq_temp = info_vep[1].split(";")
            csq_temp2 = csq_temp[0].split(",")
            csq = csq_temp2[0].split("|")
            #csq = [x or '.' for x in csq]
            current_vep_annotation = csq[4]
            current_vep_sift = csq[24].split("(")[0]
            current_vep_polyphen = csq[25].split("(")[0]
            current_LOF = csq[48]
            current_vep_eur_maf = csq[34]
        else:
            current_vep_annotation = ''
            current_vep_sift = ''
            current_vep_polyphen = ''
            current_vep_eur_maf = ''
            current_LOF = ''


        # SnpEff
        info_snpeff = current_info.split("ANN=")
        ann = info_snpeff[1].split("|")
        #ann = [x or '.' for x in ann]
        current_snpeff_annotation = ann[1]
        current_gene_name = ann[3]
        current_gene2 = ann[4]
        current_feature_type = ann[5]
        current_exon = ann[8]
        current_aa_pos = ann[13]

        # current annotation
        if current_vep_annotation == current_snpeff_annotation:
            current_annotation = current_vep_annotation
        else:
            #current_annotation = current_vep_annotation + "|" + current_snpeff_annotation
            # FOR THE MOMENT ONLY PRINT snpeff ANNOTATION
            current_annotation = current_snpeff_annotation
        #current_annotation = current_snpeff_annotation

        if "damaging" in current_vep_polyphen or "deleterious" in current_vep_sift:
            current_polysift = "del"
        else:
            current_polysift = ''

        out_str = ["chr"+current_chr, current_pos, current_annotation, current_feature_type, current_gene_name,
                current_LOF, current_exon, current_aa_pos, current_polysift, current_vep_eur_maf]
        out_str = [x or '.' for x in out_str]
        #print "\t".join(out_str)
        outputfile.write("\t".join(out_str))
        outputfile.write("\n")

    #print len(avcf)
    outputfile.close()


if __name__ == "__main__":
    main(sys.argv[1:])

