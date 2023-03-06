def encrypt_message(message):
   nato_alphabet = {
   'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta',
   'E': 'Echo', 'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel',
   'I': 'India', 'J': 'Juliet', 'K': 'Kilo', 'L': 'Lima',
   'M': 'Mike', 'N': 'November', 'O': 'Oscar', 'P': 'Papa',
   'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
   'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'Xray',
   'Y': 'Yankee', 'Z': 'Zulu'
   }

   encrypted_message = ""
  
# Iterate through each letter in the message
   for letter in message:
   
  # If the letter is in the dictionary, add the corresponding codeword to the encrypted message
     if letter.upper() in nato_alphabet:
        encrypted_message += nato_alphabet[letter.upper()] + " "
   
  # If the letter is not in the dictionary, add the original letter to the encrypted message
     else:
        encrypted_message += letter

   return encrypted_message


message = "Hello World"
encrypted_message = encrypt_message(message)
print("Encrypted message: ", encrypted_message)