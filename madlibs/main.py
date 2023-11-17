with open("story.txt", "r") as f:
    story = f.read()

palavras = set()
start_of_word = -1
fim_palavra = ">"

for i, char in enumerate(story):
    if char == "<":
        start_of_word = i

    if char == fim_palavra and start_of_word != -1:
        palavra = story[start_of_word:i + 1]
        palavras.add(palavra)
        start_of_word = -1

respostas = {}

for palavra in palavras:
    resposta = input("Enter a word for " + palavra + ": ")
    respostas[palavra] = resposta

for palavra in palavras:
    story = story.replace(palavra, respostas[palavra])

print(story)

