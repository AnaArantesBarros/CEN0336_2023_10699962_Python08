import re
import sys

sequencias = {}
codons_frames = {}
file = sys.argv[1]

with open(file) as fasta:
    geneID = ""
    for linha in fasta:
        linha = linha.rstrip().upper()
        if linha.startswith(">"):
            linhas_juntas = ""
            geneID = re.search(r"^>([\w]{8,10})", linha).group(1)
        else:
            linhas_juntas += linha.strip()
        sequencias[geneID] = "".join(linhas_juntas)

    for geneID in sequencias.keys():
        reverseSeq = sequencias[geneID][::-1]
        reverseSeq = reverseSeq.replace("A", "t").replace("T", "a").replace("C", "g").replace("G", "c")
        reverseSeq = reverseSeq.upper()
        codons_frames[geneID] = {}

        for frame in range(6):
            frameID = "frame_+" + str(frame + 1)
            codons = re.findall(r".{3}", sequencias[geneID][frame:])
            codons_frames[geneID][frameID] = codons

            frameID_reverse = "frame_-" + str(frame + 1)
            codons_reverse = re.findall(r".{3}", reverseSeq[frame:])
            codons_frames[geneID][frameID_reverse] = codons_reverse

with open("Python_08.codons-6frames.nt", "w") as outputFile:
    for geneID, frames in codons_frames.items():
        for frame, codons in frames.items():
            headline = f"{geneID}-{frame}-codons\n"
            codons_str = " ".join(codons) + "\n"
            outputFile.write(headline)
            outputFile.write(codons_str)

