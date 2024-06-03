import requests
import time
from random import randint

# Randomly attempts to get an image from gelbooru's CDN
# Checks randomly within the valid range of possible
# values for gelbooru image links.
# Loops forever until one is found.
def main():

    domain = "https://img3.gelbooru.com/images/"
    
    """
    url sub-directory xx/yy/zzz ... zzz 
    
    each character is hex (lowercase only)
    """
    chars = [char for char in '0123456789abcdef']

    # Possibly extendable. Can include GIF animated images.
    # Possibly other formats like .bmp, .tiff, .webp, .webm, etc.
    fileExt = ['.jpg', '.png']
    
    imageFound = False

    while not imageFound:
        url_sub1 = randint(0, 255)
        url_sub2 = randint(0, 255)
        url_sub3 = randint(0, 340282366920938463463374607431768211455)

        for ext in fileExt:

            # Formatting to hex will default to uppercase.
            # This is to ensure that we get properly formatted links
            sub1 = '{:02X}'.format(url_sub1).lower()
            sub2 = '{:02X}'.format(url_sub2).lower()
            sub3 = '{:032X}'.format(url_sub3).lower()

            url = domain + sub1 + '/' + sub2 + '/' + sub3 + ext
            
            # Get as a stream of data to not load it all into memory
            response = requests.get(url, stream = True)

            if not response.ok:
                print(f'No image at {url}: {response}')
                continue
                    
            print(f'image found at {url}... writing')
            
            with open('gelbooruImages/' + sub1 + '-' + sub2 + '-' + sub3 + ext, 'wb') as imageWriter:
                
                # Write the file as 1024 byte chunks
                for chunk in response.iter_content(1024):
                    if not chunk: break
                    imageWriter.write(chunk)
            
            imageFound = True
    
    print("Done.")

if __name__ == "__main__":
    main()
