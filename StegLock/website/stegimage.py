from PIL import Image

# Transformar cadena a octetos
def transformStringToBytes(data):
    dataBytes = []

    for i in data:
        dataBytes.append(format(ord(i), '08b'))

    return dataBytes

#Transformar pdf a octetos
def transformPdfToBytes(file):
    pass

#Transformar octetos a cadena
def transformBytesToString(bytes):
    data = ''
    
    for octet in bytes:
        data += chr(int(octet[:8], 2))
        if (octet[-1] == 0):
            break

    return data

#Transformar octetos a pdf
def transformBytesToPdf(bytes):
    pass

#Codificar cadena en imagen
def encodeStringInImage(data, image, password='null'):
    password = f'pwd={password}=pwd'

    dataBytes = transformStringToBytes(data)
    passwordBytes = transformStringToBytes(password)
    fullData = passwordBytes + dataBytes
    dataLength = len(fullData)
    image = image.convert('RGB')

    # Coordenadas en imagen
    i = 0

    breakLoop = False
    for x in range(image.width):
        for y in range(image.height):
            (r, g, b) = image.getpixel((x, y))
            red = format(r, '08b')
            green = format(g, '08b')
            blue = format(b, '08b')
            red = str(red)
            green = str(green)
            blue = str(blue)
            red = red[:5]
            green = green[:5]
            blue = blue[:5]
            red += fullData[i][:3]
            green += fullData[i][3:6]
            blue += fullData[i][6:]
            if(i != dataLength - 1):
                blue += '1'
            else:
                blue += '0'
                breakLoop = True
            newRed = int(red, 2)
            newGreen = int(green, 2)
            newBlue = int(blue, 2)
            image.putpixel((x, y), (newRed, newGreen, newBlue))
            i += 1
            if breakLoop: break
        if breakLoop: break
    
    return image


#Codificar pdf en imagen
def encodePdfInImage(file, image):
    pass

#Decodificar cadena de imagen
def decodeStringFromImage(image, password='null'):
    message = ''
    data = ''

    breakLoop = False
    for x in range(image.width):
        for y in range(image.height):
            (r, g, b) = image.getpixel((x, y))
            red = format(r, '08b')
            green = format(g, '08b')
            blue = format(b, '08b')
            redStr = str(red)
            greenStr = str(green)
            blueStr = str(blue)
            binaryStr = f'{redStr[-3:]}{greenStr[-3:]}{blueStr[-3:-1]}'
            message += chr(int(binaryStr, 2))
            if (int(blue[-1]) == 0):
                breakLoop = True
                break
        if breakLoop: break
    
    startIndex = message.find('pwd=') + 4
    endIndex = message.find('=pwd')
    imagePassword = message[startIndex:endIndex]
    
    if (password == imagePassword):
        data = message[endIndex + 4:]
    else:
        data = '0'

    return data

#Decodificar pdf de imagen
def decodePdfFromImage(image):
    pass
