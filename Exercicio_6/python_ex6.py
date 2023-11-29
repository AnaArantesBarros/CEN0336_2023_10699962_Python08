#import sys
import re

#file = sys.argv[1]
sequencias = {}  # Dictionary with gene names and their content
codons_frames = {}

translation_table = {
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R',
    'AAT': 'N', 'AAC': 'N',
    'GAT': 'D', 'GAC': 'D',
    'TGT': 'C', 'TGC': 'C',
    'CAA': 'Q', 'CAG': 'Q',
    'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    'CAT': 'H', 'CAC': 'H',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I',
    'TTA': 'L', 'TTG': 'L', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'AAA': 'K', 'AAG': 'K',
    'ATG': 'M',
    'TTT': 'F', 'TTC': 'F',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'AGT': 'S', 'AGC': 'S',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'TGG': 'W',
    'TAT': 'Y', 'TAC': 'Y',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TAA': '*', 'TGA': '*', 'TAG': '*'
}

with open("Python_08.fasta") as fasta:
    geneID = ""
    protein_frames = {}  # Fix: initialize protein_frames here
    for linha in fasta:
        linha = linha.rstrip()

        if linha.startswith(">"):  # Description line
            linhas_juntas = ""
            geneID = re.search(r"^>([\w]{8,10})", linha).group(1)
        else:  # Bases line
            linhas_juntas += linha.strip()
            codons = re.findall(r".{3}", linhas_juntas.replace("\n", ""))
            sequencias[geneID] = "".join(codons)

            if geneID not in codons_frames:
                codons_frames[geneID] = {}

            for frame in range(6):
                codons = re.findall(r".{3}", sequencias[geneID][frame:])
                frameID = "frame_+" + str(frame + 1)
                codons_frames[geneID][frameID] = codons
                protein = "".join([translation_table[codon] for codon in codons])
                frame_aa = f"{geneID}_{frameID}_translated"
                if geneID not in protein_frames:
                    protein_frames[geneID] = {}
                protein_frames[geneID][frame_aa] = protein

with open("Python_08.codons-6frames.nt", "w") as nt_output:
    for geneID, frames in codons_frames.items():
        for frame, codons in frames.items():
            headline = f">{geneID}_{frame}\n"
            codons_str = " ".join(codons) + "\n"
            nt_output.write(headline)
            nt_output.write(codons_str)

with open("Python_08.translated.aa", "w") as aa_output:
    for geneID, frames in codons_frames.items():
        for frame, codons in frames.items():
            protein = "".join([translation_table[codon] for codon in codons])
            headline = f">{geneID}_{frame}_translated\n"
            aa_output.write(headline)
            aa_output.write(protein + "\n")

with open("Python_08.translated-longest.txt", "w") as longest_aa_output:
    for geneID in protein_frames.keys():
        longestProtein = ""
        longestFrame = ""
        for frame in protein_frames[geneID]:
            proteinas = re.findall(r"(M[A-Z]+?)\*", protein_frames[geneID][frame])
            for i in proteinas:
                if len(i) > len(longestProtein):
                    longestProtein = i
                    longestFrame = frame
        longest_aa_output.write(f">{geneID}_{longestFrame}\n")
        longest_aa_output.write(longestProtein + "\n")

