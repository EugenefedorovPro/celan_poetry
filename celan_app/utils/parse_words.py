import spacy
nlp = spacy.load("de_core_news_sm")

doc = nlp("Umsonst malst du Herzen ans Fenster.")
for t in doc:
    print(t.text, t.pos_, t.lemma_, t.morph)

