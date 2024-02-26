import argparse
import numpy as np
from PIL import Image

def string_to_key(key_string):
    # Convert the string key to a numerical value by summing ASCII values of characters
    return sum(ord(char) for char in key_string)

def shuffle_pixels(image, key):
    width, height = image.size
    pixels = list(image.getdata())

    # Use a deterministic shuffle algorithm based on the key
    rng = np.random.default_rng(string_to_key(key))
    shuffled_indices = np.arange(len(pixels))
    rng.shuffle(shuffled_indices)

    shuffled_pixels = [pixels[i] for i in shuffled_indices]

    shuffled_image = Image.new(image.mode, image.size)
    shuffled_image.putdata(shuffled_pixels)

    return shuffled_image

def inverse_shuffle_pixels(image, key):
    width, height = image.size
    pixels = list(image.getdata())

    # Use a deterministic shuffle algorithm based on the key
    rng = np.random.default_rng(string_to_key(key))
    shuffled_indices = np.arange(len(pixels))
    rng.shuffle(shuffled_indices)

    inverse_indices = np.argsort(shuffled_indices)
    original_pixels = [pixels[i] for i in inverse_indices]

    original_image = Image.new(image.mode, image.size)
    original_image.putdata(original_pixels)

    return original_image

def encrypt_image(image_path, key):
    img = Image.open(image_path)
    shuffled_img = shuffle_pixels(img, key)
    shuffled_img.save("encrypted_image.png")
    print("Image encrypted successfully!")

def decrypt_image(image_path, key):
    img = Image.open(image_path)
    original_img = inverse_shuffle_pixels(img, key)
    original_img.save("decrypted_image.png")
    print("Image decrypted successfully!")

def main():
    parser = argparse.ArgumentParser(description="Image Encryption/Decryption Tool")
    parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the image")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the image")
    parser.add_argument("key", help="Encryption/Decryption key")
    parser.add_argument("image_path", help="Path to the image file")
    args = parser.parse_args()

    if args.encrypt and not args.decrypt:
        encrypt_image(args.image_path, args.key)
    elif args.decrypt and not args.encrypt:
        decrypt_image(args.image_path, args.key)
    else:
        print("Specify either --encrypt (-e) or --decrypt (-d), not both.")

if __name__ == "__main__":
    main()
