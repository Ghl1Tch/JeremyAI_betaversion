import ollama
response = ollama.chat(model="qwen2.5:3b", messages=[{"role": "user", "content": "Hello, how are you?"}])
print(response['message']['content'])
#This test for AI