import wave

# Transformar cadena a bits
def transformStringToBits(data):
    dataBytes = []

    for i, c in enumerate(data):
        charArray = list(format(ord(c), '08b'))
        if i == len(data) - 1:
            charArray.append('0')
        else:
            charArray.append('1')
        dataBytes.append(charArray)

    return dataBytes

#Transformar archivo a octetos
def transformFileToString(file):
    with open(f'temp/{file}', 'r') as f:
        fileData = f.read()
    fileData = f'txt={fileData}=txt'
    
    return fileData

#Codificar cadena en imagen
def encodeStringInAudio(data, audioPath, password='null'):
    password = f'pwd={password}=pwd'
    data = f'str={data}=str'
    message = password + data
    dataBytes = transformStringToBits(message)
    outputPath = 'temp/encoded.wav'
    audio = wave.open(audioPath, mode='rb')
    frameBytes = bytearray(audio.readframes(-1))
    
    helper = 0

    for i in dataBytes:
        for j in i:
            frameBytes[helper] = (frameBytes[helper] & 254) | int(j)
            if i == len(dataBytes) - 1:
                if j == len(i):
                    frameBytes[helper] = 0
            helper += 1

    encodedFrame = bytes(frameBytes)

    newAudio = wave.open(outputPath, mode='wb')
    newAudio.setparams(audio.getparams())
    newAudio.writeframes(encodedFrame)
    newAudio.close()
    audio.close()

    return outputPath

#Codificar archivo en imagen
def encodeFileInAudio(file, audioPath, password='null'):
    password = f'pwd={password}=pwd'
    data = transformFileToString(file)
    message = password + data
    dataBytes = transformStringToBits(message)
    outputPath = 'temp/encoded.wav'
    audio = wave.open(audioPath, mode='rb')
    frameBytes = bytearray(audio.readframes(-1))
    
    helper = 0

    for i in dataBytes:
        for j in i:
            frameBytes[helper] = (frameBytes[helper] & 254) | int(j)
            if i == len(dataBytes) - 1:
                if j == len(i):
                    frameBytes[helper] = 0
            helper += 1

    encodedFrame = bytes(frameBytes)

    newAudio = wave.open(outputPath, mode='wb')
    newAudio.setparams(audio.getparams())
    newAudio.writeframes(encodedFrame)
    newAudio.close()
    audio.close()

    return outputPath

#Decodificar imagen
def decodeAudio(audioPath, password='null'):
    message = ''
    data = ''
    extracted = ''

    audio = wave.open(audioPath, mode='rb')
    frameBytes = bytearray(audio.readframes(-1))
    breakLoop = False
    for i in range(len(frameBytes)):
        if (i + 1) % 9 == 0:
            if frameBytes[i] == 0:
                breakLoop = True
        else:
            extracted += str(frameBytes[i])
        if breakLoop: break
    audio.close()
    n = 8
    extractedBits = [extracted[i: i + n] for i in range(0, len(extracted), n)]

    for i in range(len(extractedBits)):
        message += chr(int(extractedBits[i], 2)) 

    startIndex = message.find('pwd=') + 4
    endIndex = message.find('=pwd')
    audioPassword = message[startIndex:endIndex]

    if password == audioPassword:
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
