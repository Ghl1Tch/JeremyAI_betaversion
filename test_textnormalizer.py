from core.text_normalizer import TextNormalizer


normalizer = TextNormalizer()

text = "Джеремия, открой Дис Корд"

result = normalizer.normalize(text)

print(result)