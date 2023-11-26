import sys
import re

file = sys.argv[1]
sequencias = {}  #Dicionário com o nome do gene e o seu conteúdo
codons_frames = {}
with open(file) as fasta:
    geneID = ""
    for linha in fasta:
        linha = linha.rstrip()
        if linha.startswith(">"):  #Linha de descrição
            linhas_juntas = ""
            geneID = re.search(r"^>([\w]{8,10})", linha).group(1)
        else: #Linha de bases
            linhas_juntas += linha.strip()
            codons = re.findall(r".{3}", linhas_juntas.replace("\n", ""))
            sequencias[geneID] = "".join(codons)

            if geneID not in codons_frames:
                codons_frames[geneID] = {}

            for frame in range(3):
                codons = re.findall(r".{3}", sequencias[geneID][frame:])
                frameID = "frame_+" + str(frame + 1)
                codons_frames[geneID][frameID] = codons

with open("Python_08.codons-frame-1.nt", "w") as outputFile:
    for geneID, frames in codons_frames.items():
        for frame, codons in frames.items():
            if frame == "frame_+1":
                headline = f"{geneID}_{frame}\n"
                codons_str = " ".join(codons) + "\n"
                outputFile.write(headline)
                outputFile.write(codons_str)