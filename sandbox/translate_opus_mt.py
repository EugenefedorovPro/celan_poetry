from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL = "Helsinki-NLP/opus-mt-de-en"

tok = AutoTokenizer.from_pretrained(MODEL)
mdl = AutoModelForSeq2SeqLM.from_pretrained(MODEL)


def de_to_en(text: str) -> str:
    x = tok(text, return_tensors="pt", truncation=True)
    y = mdl.generate(**x, max_new_tokens=512)
    return tok.decode(y[0], skip_special_tokens=True)


print(de_to_en("Ein Kranz ward gewunden aus schwärzlichem Laub in der Gegend von Akra"))
