import re

text = "[Funusdt]  Рядом с горизонтальной поддержкой   (15m)  [[?]] (Https://www.100 eyes.com/education/support-and-sistance/#horizontal-soupport)\n\n[Возьмите бонус на депозит в Bybit!] (Https://partner.bybit.com/b/100eyes)"

# Приведение "Funusdt" к верхнему регистру
text = re.sub(r'\[Funusdt\]', '[FUNUSDT]', text)
text = re.sub(r'\[Возьмите бонус на депозит в Bybit!]', '', text)
text = re.sub(r'\[[?]]', '', text)
text = re.sub(r'\[]', '', text)
text = re.sub(r'Рядом с горизонтальной поддержкой', 'Уровень поддержки', text)

# Удаление только ссылок, оставляя текст в квадратных скобках
text = re.sub(r'\(https?://[^\)]*\)', '', text, flags=re.IGNORECASE)

# Удаление лишних пробелов и переносов строк
text = re.sub(r'\s+', ' ', text).strip()

print(text)
