import sys
import re

file = sys.argv[1]
sequencias = {}  #Dicionário com o nome do gene e o seu conteúdo
contagem = {}
with open(file) as fasta:
    geneID = ""
    for linha in fasta:
        linha = linha.rstrip()
        if linha.startswith(">"): #Linha de descrição
            linhas_juntas = ""
            geneID = re.search(r"^>([\w]{8,10})", linha).group(1)
        else: #Linha de bases
            linhas_juntas += linha.strip()
            codons = re.findall(r".{3}", linhas_juntas.replace("\n", ""))
            sequencias[geneID] = "".join(codons)

    for geneID in sequencias.keys():
        bases = set(sequencias[geneID])
        nt_comp = {}
        for base in bases:
            nt_comp[base] = str(sequencias[geneID]).count(base)
        contagem[geneID] = nt_comp
    #print(contagem['c0_g1_i1']['T']) exemplo de uso
        print(f"{geneID}\\{contagem[geneID]['A']}\\{contagem[geneID]['T']}\\{contagem[geneID]['G']}\\{contagem[geneID]['C']}")
