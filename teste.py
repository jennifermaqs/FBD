first_name = 'Maria Júlia'
last_name = 'Rodrigues'
full_name = first_name +" "+ last_name
print("Hello, "+full_name)

age = 21
age += 1
print (age)

name = input("nome?: ")
age = int(input("idade?: "))
altura = float(input("altura?: "))

print("Hello " + name)
print("Você tem " + str(age) + " anos de idade")
print("E mede "+ str(altura) + " cm de altura")

Write code below 💖

eu quando

Write code below 💖

eu quando

print('JJJJJJJJJJ')
print('    J')
print('    J')
print('    J')
print('    J')
print('    J   J')
print('    J   J')
print('    J   J')
print('    J   J')
print('    JJJJJ')

date = "15/07/2025"

print(date + " OMG so amazing python is top uhul! 🫶") 

Write code below 💖
fahrenheit = float(input("Fahrenheit: "))
celsius = (fahrenheit - 32)/1.8

print(celsius)

massa = 66
altura = 1.73

pesos = int(input("What do you have left in pesos? "))
soles = int(input("What do you have left in soles? "))
reais = int(input("What do you have left in reais? "))
dolarp = pesos * 0.00025
dolars = soles * 0.28
dolarr = reais * 0.21
dolar = (dolarp + dolars + dolarr)

print(dolar)




import random

question = input('Question:      ')

random_number = random.randint(1, 9)

if random_number == 1:
  answer = 'Yes - definitely'
elif random_number == 2:
  answer = 'It is decidedly so'
elif random_number == 3:
  answer = 'Without a doubt'
elif random_number == 4:
  answer = 'Reply hazy, try again'
elif random_number == 5:
  answer = 'Ask again later'
elif random_number == 6:
  answer = 'Better not tell you now'
elif random_number == 7:
  answer = 'My sources say no'
elif random_number == 8:
  answer = 'Outlook not so good'
elif random_number == 9:
  answer = 'Very doubtful'
else:
  answer = 'Error'
  
print('Magic 8 Ball:  ' + answer)

heigth = float(input("altura?: "))
credits = int(input("creditos?: "))

if heigth >= 137 and credits >= 10:
  print("Aproveite o passeio!")
elif heigth < 137 and credits >= 10:
  print("Você não é alto o suficiente para andar")
elif heigth >= 137 and credits < 10:
  print("Você não tem créditos suficientes")
else:
  print("Nenhum dos requisitos foram atendidos!")

Q1 = int(input("Do you like 1.Dawn or 2.Dusk?"))
Q2 = int(input("When I’m dead, I want people to remember me as: 1) The Good 2) The Great 3) The Wise 4) The Bold"))
Q3 = int(input("Which kind of instrument most pleases your ear? 1) The violin 2) The trumpet 3) The piano 4) The drum"))

print(Q1)
print(Q2)
print(Q3)

grif = 0
corv = 0
lufa = 0
sons = 0

Q1 = int(input("Do you like 1.Dawn or 2.Dusk? "))
if Q1 == 1:
    grif += 1
    corv += 1
elif Q1 == 2:
    lufa += 1
    sons += 1
else:
    print("Entrada errada")
Q2 = int(input("When I’m dead, I want people to remember me as: 1) The Good 2) The Great 3) The Wise 4) The Bold "))

if Q2 == 1:
    lufa += 2
elif Q2 == 2:
    sons += 2
elif Q2 == 3:
    corv += 2
elif Q2 == 4:
    grif += 2
else:
    print("Entrada errada")
Q3 = int(input("Which kind of instrument most pleases your ear? 1) The violin 2) The trumpet 3) The piano 4) The drum "))
if Q3 == 1:
    sons += 4
elif Q3 == 2:
    lufa  += 4
elif Q3 == 3:
    corv += 4
elif Q3 == 4:
    grif += 4
else:
    print("Entrada errada")
    
print("Grifinória: " + str(grif))
print("Sonserina: " + str(sons))
print("Lufa-lufa: " + str(lufa))
print("Corvinal: " + str(corv))


print('BANK OF CODÉDEX')

pin = int(input('Enter your PIN: '))

while pin != 1234:
  pin = int(input('Incorrect PIN. Enter your PIN again: '))

if pin == 1234:
  print('PIN accepted!')
  

guess = 0
tries = 0

while guess != 6:
  guess = int(input("Guess the number:  "))
  tries += 1

print("You got it in " + str(tries) + "!")

for i in range(100):
  i = "Não usarei o snapchat na aula"
  print(i)


for i in range(5):
  print('The square of ' + str(i) + ' is ' + str(i*i))

for i in range(99, 0, -1):
  print(f'{i} garrafas de cerveja na parede')
  print(f'{i} garrafas de cerveja')
  print('pegue uma, passe ao redor') 
  print(f'{i-1} garrafas de cerveja na parede')   

for i in range(1, 101):
    print (i)
for i in range(1, 101):
  if i % 3 == 0 and i % 5 == 0:
    i = "FizzBuzz"
    print(i)
  elif i % 3 == 0:
    i = "Fizz"
    print(i)
  elif i % 5 == 0:
    i = "Buzz"
    print(i)
  else:
    print(i)