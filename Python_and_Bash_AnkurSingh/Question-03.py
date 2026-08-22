file = open("content.txt", "w")
file.write("This is my Python 3rd  question solution and I am testing the file writing functionality.")
file.close()

file = open("content.txt", "r")
content = file.read()
file.close()

print(content)
