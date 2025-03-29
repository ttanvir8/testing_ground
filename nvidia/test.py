from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

completion = client.chat.completions.create(
  model="nvidia/llama-3.3-nemotron-super-49b-v1",
  messages=[{"role":"system","content":"detailed thinking on"},{"role":"user","content":"Final thought\nGoal: She wants someone who will enchant(meaning: to charm/delight someone greatly) her. She said it herself, she is willing to be a gold digger.\n\nBut she thinks:\nLooks: And she thinks you are ugly.\nMoney: Come from a ugly family. \nShe thinks you are poor\nLacking self-reliance: Is very needy.\n\nShe has no reason to change: She will never change.\nSimple as that.\n\nOutput: Meaning you don’t enchant her.\n\nConclusion:\nShe just doesn’t love you. That's it.\nSo there is no point in doing anything.\nI must relinquish all my feelings and let her go.\n\nit isn't happening just accept it\nshe is straight up ignoring you brother\n"}],
  temperature=0.6,
  top_p=0.95,
  max_tokens=4096,
  frequency_penalty=0,
  presence_penalty=0,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")


