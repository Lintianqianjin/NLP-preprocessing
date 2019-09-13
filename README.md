# NLP-preprocessing

## [PDF Extraction](https://github.com/Lintianqianjin/NLP-preprocessing/tree/master/pdfExtraction)   
Extract information such as abstracts, body texts, and annotations in the paper, and ensure the integrity of paragraphs, sentences, and grammar.  
###### example:  
This is [A paper](https://github.com/Lintianqianjin/NLP-preprocessing/blob/master/pdfExtraction/data/pdf1.pdf).  
when we run the code, we get following outputs.  

```
INTRODUCTION  
The nutritional environment is a crucial determinant of important cellular decisions, such as growth, proliferation and development.
Recently, a series of outstanding studies have demonstrated that nutrient availability tightly regulates cell growth through an evolutionarily highly conserved signalling pathway, the target of rapamycin (TOR)/p70 S6 kinase (S6K) pathway (reviewed in Hay & Sonenberg, 2004). S6K was originally discovered as a kinase that phosphorylates 40S ribosomal protein S6 at many sites and its activity has been considered as a characteristic of cell growth (Kozma & Thomas, 1994). Studies on the action mechanism of immunosuppressant rapamycin led to a surprising discovery that TOR is the upstream activator of S6K in vivo (Chung et al, 1992; Brown et al, 1994; Sabatini et al, 1994). Recently, studies using mammalian cell lines (Fingar et al, 2002) and knockout mice (Shima et al, 1998) clearly showed that the TOR/S6K signalling pathway controls cell growth in vertebrates. Consistently, Drosophila S6K (dS6K) and Drosophila TOR (dTOR) mutants also showed reduced cell and body size compared with the wildtype (w1118) fly (Montagne et al, 1999; Oldham et al, 2000; Zhang et al, 2000).
TOR is also involved in the regulation of autophagy. Autophagy is a process conserved among all eukaryotic cells and is required for rapid degradation of large portions of the cytoplasm and organelles in the lysosomal lumen, occurring as a result of nutrient deprivation or normal developmental processes (Levine & Klionsky, 2004). Under nutrient-rich conditions, TOR blocks the initiation step of autophagy by facilitating dissociation of Autophagy-specific gene (Atg) 13 from Atg1, an essential factor required for the formation of an autophagic vesicle (autophago-some) in budding yeast (Kamada et al, 2000). Furthermore, the crucial roles of TOR and ATG1 in starvation- and development-dependent autophagy have been discovered in the fat body cells of Drosophila (Scott et al, 2004).
As cell growth and autophagy are opposite biological processes both regulated by TOR, we hypothesized that autophagy might be responsible for inhibiting cell growth under conditions of suppressed TOR signalling, such as starvation. To investigate the relationship between autophagy and cell growth regulation, we examined the interactions between the representative components of the two pathways, TOR/S6K and ATG1. Using biochemical and genetic approaches, we demonstrated that ATG1 negatively regulates S6K and, consequently, inhibits cell growth in both mammals and Drosophila.
RESULTS AND DISCUSSION

...The latter part is omitted here...  

-----------------------------------------正文结束-----------------------------------------  
-----------------------------------------图解等附文开始-----------------------------------------  
Fig 1 | Involvement of Drosophila Autophagy-specific gene 1 in Drosophila Target of rapamycin-dependent cell growth and development. (A) Genomic structure of CG10967. The P-element insertion site of EP3348 (DmATG11) is denoted. (B) The transcriptional levels of DmATG1 in the third instar larvae were analysed by qRT–PCR. Ribosomal protein 49 (rp49) was used as an internal control; n¼3. Bars indicate mean7s.d. (C) Images of the larvae of denoted genotypes at 3 days (top) and 6 days (middle) after egg-laying (AEL), and quantification of the larvae that developed into the mid–late third instar stage of each genotype (bottom); n¼3. Bars indicate mean7s.d. Fifteen larvae of each genotype were examined in each experiment. (D) Suppression of lipid vesicle aggregation in the fat body of dTOR mutants by reduced gene dosage of DmATG1. The fat body images of the second/early third instar larvae of denoted genotypes under fully fed conditions. (E) Images of the larval salivary glands of denoted genotypes.
Hoechst33342 (pseudo-coloured green) and phalloidin-TRITC (red) were used to visualize the nuclei and cell boundary of larval salivary gland cells, respectively. (F) Quantitative analysis of cell and nuclear sizes in Fig 1E; n¼5. Bars indicate mean7s.d. DmATG1, Drosophila Autophagy-specific gene 1; dTOR, Drosophila TOR; qRT–PCR, quantitative real-time reverse transcriptase–PCR.  

...The latter part is omitted here...  

-----------------------------------------图解等附文结束-----------------------------------------  
-----------------------------------------摘要开始-----------------------------------------  
It has been proposed that cell growth and autophagy are coordinated in response to cellular nutrient status, but the relationship between them is not fully understood. Here, we have characterized the fly mutants of Autophagy-specific gene 1 (ATG1), an autophagy-regulating kinase, and found that ATG1 is a negative regulator of the target of rapamycin (TOR)/S6 kinase (S6K) pathway. Our Drosophila studies have shown that ATG1 inhibits TOR/S6K-dependent cell growth and development by interfering with S6K activation. Consistently, overexpression of ATG1 in mammalian cells also markedly inhibits S6K in a kinase activity-dependent manner, and short interfering RNA-mediated knockdown of ATG1 induces ectopic activation of S6K and S6 phosphorylation. Moreover, we demonstrated that ATG1 specifically inhibits S6K activity by blocking phosphorylation of S6K at Thr 389. Taken together, our genetic and biochemical results strongly indicate crosstalk between autophagy and cell growth regulation.

-----------------------------------------摘要结束-----------------------------------------  
```
