import emoji
import re
def extract_emojis(text):
  """ Used to extract emojis in the text """
  text_de= emoji.demojize(text)
  emojis_list_de= re.findall(r'(:[!_\-\w]+:)', text_de)
  list_emoji= [emoji.emojize(x) for x in emojis_list_de]
  return list_emoji
