import os
import selenium
from selenium import webdriver
import base64
import time
import urllib.request

from selenium.webdriver.common.by import By

DRIVER_PATH = '/usr/local/bin/chromedriver'

SAVE_FOLDER = 'dataset/train'

# Pain:
# GOOGLE_IMAGES = 'https://www.google.com/search?q=horse+pain+face&tbm=isch&ved=2ahUKEwigwsqSjK77AhVkhHMKHXX4Dl8Q2-cCegQIABAA&oq=horse+pain+face&gs_lcp=CgNpbWcQAzIECCMQJzIECCMQJzIFCAAQgAQ6BggAEAgQHlDlzQRYmdAEYKfSBGgCcAB4AIAB5wKIAdQJkgEFMi00LjGYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=K21yY-CANeSIzgP18Lv4BQ&bih=731&biw=1536&rlz=1C1GCEU_enZA986ZA986'
# GOOGLE_IMAGES = 'https://www.google.com/search?q=unhappy+horse&tbm=isch&ved=2ahUKEwiI2--24rD7AhWbhM4BHf9vAyUQ2-cCegQIABAA&oq=unhappy+horse&gs_lcp=CgNpbWcQAzIFCAAQgAQyBwgAEIAEEBgyBwgAEIAEEBgyBwgAEIAEEBgyBwgAEIAEEBg6BAgjECc6CwgAEIAEELEDEIMBOggIABCABBCxAzoICAAQsQMQgwE6BQgAELEDOgQIABBDOgcIABCxAxBDOgoIABCxAxCDARBDUOcHWJYVYM8VaABwAHgAgAGaAogBzhaSAQQyLTEymAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=FNRzY4iBN5uJur4P_9-NqAI&bih=731&biw=1536&rlz=1C1GCEU_enZA986ZA986'
# GOOGLE_IMAGES = 'https://www.google.com/search?q=horse+nose+pain&tbm=isch&ved=2ahUKEwi_p63Syrr7AhUM8xoKHYb2DHEQ2-cCegQIABAA&oq=horse+nose+pain&gs_lcp=CgNpbWcQAzIFCAAQgAQ6BAgjECc6BAgAEEM6BggAEAgQHjoHCAAQgAQQGFDcBFjzL2CUMmgGcAB4AIABAIgBAJIBAJgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=Ufl4Y_-6HIzma4bts4gH&bih=731&biw=1536&rlz=1C1GCEU_enZA986ZA986'
# GOOGLE_IMAGES = 'https://www.google.com/search?q=horse+ears+pain&tbm=isch&ved=2ahUKEwi98t3n1Lr7AhUR9BoKHaPPBpYQ2-cCegQIABAA&oq=horse+ears+pain&gs_lcp=CgNpbWcQAzoECCMQJzoFCAAQgARQgwlYohBgwxVoAHAAeACAAZQCiAG-C5IBAzItNpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=-gN5Y72NKJHoa6Ofm7AJ&bih=731&biw=1536&rlz=1C1GCEU_enZA986ZA986'

# No Pain:
# GOOGLE_IMAGES = 'https://www.google.com/search?q=horse+head+photo&tbm=isch&ved=2ahUKEwivuO-moa77AhUBVhoKHeZaClMQ2-cCegQIABAA&oq=horse+head+photo&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBggAEAUQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB46BAgjECc6BggAEAgQHjoECAAQQzoGCAAQBxAeUIoJWOMdYOMgaABwAHgAgAHzAYgB0AqSAQMyLTaYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=W4NyY--eIoGsaea1qZgF&bih=947&biw=1903&rlz=1C1GCEU_enZA986ZA986&hl=en'
# GOOGLE_IMAGES = 'https://www.google.com/search?q=healthy+horse+head&tbm=isch&ved=2ahUKEwiPpNCG47D7AhUG7xoKHaYVCcYQ2-cCegQIABAA&oq=healthy+horse+head&gs_lcp=CgNpbWcQAzoECAAQQzoFCAAQgAQ6BggAEAUQHlAAWPUFYNAGaABwAHgAgAGLAogB_weSAQMyLTSYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=vNRzY4_WCYbea6arpLAM&bih=731&biw=1536&rlz=1C1GCEU_enZA986ZA986'
# GOOGLE_IMAGES = 'https://www.google.com/search?q=happy+horse+eyes&tbm=isch&ved=2ahUKEwiR2PuByrr7AhUrxIUKHR0hBX8Q2-cCegQIABAA&oq=happy+horse+eyes&gs_lcp=CgNpbWcQAzIFCAAQgAQ6BAgjECc6BggAEAgQHjoECAAQHlD_D1j9E2D7FGgAcAB4AIAB5gGIAawFkgEDMi0zmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=qPh4Y5HkNauIlwSdwpT4Bw&bih=731&biw=1536&rlz=1C1GCEU_enZA986ZA986'

# GOOGLE_IMAGES = 'https://www.google.com/search?q=horse+ears+forward&tbm=isch&ved=2ahUKEwjmiOK-yrr7AhVP4oUKHQbGD-kQ2-cCegQIABAA&oq=horse+ears&gs_lcp=CgNpbWcQARgJMgQIABBDMgQIABBDMgQIABBDMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABFClCFilCGDOKmgAcAB4AIABhQKIAfkDkgEDMi0ymAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=KPl4Y-bUF8_ElwSGjL_IDg&bih=731&biw=1536&rlz=1C1GCEU_enZA986ZA986'
GOOGLE_IMAGES = 'https://www.google.com/search?q=horse+nose&tbm=isch&ved=2ahUKEwiioNrPyrr7AhUihM4BHQwxDOMQ2-cCegQIABAA&oq=horse+nose&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BAgjECc6BAgAEENQvgtY_A1gwQ9oAHAAeACAAewBiAGdB5IBAzItNJgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=S_l4Y-LON6KIur4PjOKwmA4&bih=731&biw=1536&rlz=1C1GCEU_enZA986ZA986'


driver = webdriver.Chrome(DRIVER_PATH)
driver.get(GOOGLE_IMAGES)


# Scroll to the end of the page
def scroll_to_end():
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    print('scroll done')


counter = 0
for i in range(1, 10):
    scroll_to_end()
    image_elements = driver.find_elements(By.CLASS_NAME, 'rg_i')
    print(len(image_elements))
    for image in image_elements:
        if image.get_attribute('src') is not None:
            my_image = image.get_attribute('src').split('data:image/jpeg;base64,')
            # filename = 'pain' + str(counter) + '.jpeg'
            filename = 'no pain' + str(counter) + '.jpeg'
            if len(my_image) > 1:
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(my_image[1]))
            else:
                print(image.get_attribute('src'))
                # urllib.request.urlretrieve(image.get_attribute('src'), 'pain' + str(counter) + '.jpeg')
                urllib.request.urlretrieve(image.get_attribute('src'), 'no pain' + str(counter) + '.jpeg')
            counter += 1
