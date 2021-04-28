from PIL import Image

# Transformar cadena a octetos
def transformStringToBytes(data):
    #data = f'str={data}=str'
    dataBytes = []

    for i in data:
        dataBytes.append(format(ord(i), '08b'))

    return dataBytes

#Transformar pdf a octetos
def transformFileToBytes(file):
    with open(f'temp/{file}', 'r') as f:
        fileData = f.read()
    fileData = f'txt={fileData}=txt'
    dataBytes = []

    for i in fileData:
        dataBytes.append(format(ord(i), '08b'))

    return dataBytes

#Codificar cadena en imagen
def encodeStringInImage(data, image, password='null'):
    password = f'pwd={password}=pwd'
    data = f'str={data}=str'
    message = password + data
    dataBytes = transformStringToBytes(message)
    dataLength = len(dataBytes)
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
            red += dataBytes[i][:3]
            green += dataBytes[i][3:6]
            blue += dataBytes[i][6:]
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

#Codificar archivo en imagen
def encodeFileInImage(file, image, password='null'):
    password = f'pwd={password}=pwd'

    dataBytes = transformFileToBytes(file)
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


#Decodificar imagen
def decodeImage(image, password='null'):
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
        if 'str=' in data and '=str' in data:
            startIndex = data.find('str=') + 4
            endIndex = data.find('=str')
            data = data[startIndex:endIndex]
        elif 'txt=' in data and '=txt' in data:
            startIndex = data.find('txt=') + 4
            endIndex = data.find('=txt')
            data = data[startIndex:endIndex]
            filepath = 'temp/decodedmessage.txt' 
            with open(f'{filepath}', 'w') as f:
                f.write(data)
            data = filepath
        else:
            data = '0'
    else:
        data = '0'

    return data
