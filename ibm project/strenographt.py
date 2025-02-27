import cv2
import numpy as np

# Function to encode data into an image
def encode_image(image_path, secret_data):
    # Load the image
    img = cv2.imread(image_path)
    
    # Convert the secret data into binary format
    data = ''.join(format(ord(i), '08b') for i in secret_data) + '1111111111111110'  # End marker
    data_index = 0
    data_length = len(data)

    # Iterate over each pixel to hide the data
    for row in img:
        for pixel in row:
            for i in range(3):  # RGB channels
                if data_index < data_length:
                    pixel[i] = (pixel[i] & 254) | int(data[data_index])  # Modify LSB
                    data_index += 1
                else:
                    break
    
    # Save the encoded image
    cv2.imwrite("encoded_image.png", img)
    print("[✔] Data encoded successfully! Saved as 'encoded_image.png'")

# Function to decode data from an image
def decode_image(image_path):
    img = cv2.imread(image_path)
    binary_data = ""

    # Extract LSB bits
    for row in img:
        for pixel in row:
            for i in range(3):  # RGB channels
                binary_data += str(pixel[i] & 1)

    # Convert binary to text
    data_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_text = "".join([chr(int(byte, 2)) for byte in data_bytes])
    
    # Retrieve message before the end marker
    message = decoded_text.split("1111111111111110")[0]
    print("[✔] Decoded Message:", message)

# Example Usage
if __name__ == "__main__":
    choice = input("Choose an option:\n1. Encode message\n2. Decode message\nEnter 1 or 2: ")
    
    if choice == '1':
        secret_message = input("Enter the secret message: ")
        encode_image("input.png", secret_message)
    elif choice == '2':
        decode_image("encoded_image.png")
    else:
        print("[✘] Invalid choice! Run the script again.")
