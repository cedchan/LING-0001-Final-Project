import benepar, spacy
benepar.download('benepar_en3')

nlp = spacy.load('en_core_web_md')
nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
doc = nlp("This is a test of the program.")

print("\nSetup complete.\n" + "-" * 50 + "\n")

sent = list(doc.sents)[0]
print(sent._.parse_string)
# (S (NP (DT This)) (VP (VBZ is) (NP (NP (DT a) (NN test)) (PP (IN of) (NP (DT the) (NN program))))))
# (S (NP (DT This)) (VP (VBZ is) (NP (NP (DT a) (NN test)) (PP (IN of) (NP (DT the) (NN program))))) (. .))