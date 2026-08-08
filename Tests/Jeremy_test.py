import ollama
response = ollama.chat(model="qwen2.5:3b", messages=[{"role": "user", "content": "Привет, как дела?"}])
print(response['message']['content'])