from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_NAME = "facebook/nllb-200-distilled-600M"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def translate(text: str, src_lang: str, tgt_lang: str) -> str:
    """
    src_lang examples: "deu_Latn"
    tgt_lang examples: "eng_Latn", "rus_Cyrl"
    """
    tokenizer.src_lang = src_lang
    inputs = tokenizer(text, return_tensors="pt", truncation=True)

    forced_bos_token_id = tokenizer.convert_tokens_to_ids(tgt_lang)

    output_tokens = model.generate(
        **inputs,
        forced_bos_token_id=forced_bos_token_id,
        max_new_tokens=512,
    )

    return tokenizer.decode(output_tokens[0], skip_special_tokens=True)


if __name__ == "__main__":
    text_de = "Die Kiefer wächst in vielen Regionen Europas."

    print("German → English:")
    print(translate(text_de, "deu_Latn", "eng_Latn"))

    print("\nGerman → Russian:")
    print(translate(text_de, "deu_Latn", "rus_Cyrl"))
