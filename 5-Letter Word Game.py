words=[]
game="play"
while game=="play":
    new=input("Enter a 5 letter word.:")
    if len(new)>5 or len(new)<5:
        print("That's not a five letter word")
    else:
        if new in words:
            game="over"
            print("you already said that word. Game Over.")
            print("You know ", len(words), " 3-letter words.")
else:
    print("Nice one!")
    words.append(new)
