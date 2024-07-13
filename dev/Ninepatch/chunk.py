import numpy as np
import pyperclip
from PIL import Image


# Dev Documents:
# ChatGPT
# https://github.com/completejavascript/nine-patch-js
# https://github.com/andrepl/pyninepatch
# https://pypi.org/project/ninepatch/
# https://github.com/Anatolii/NinePatchChunk


class Res_png_9patch:
    def __init__(self, data):
        global chunk_info
        ninepatch_bottom = (data[15], width - data[19], width - data[19] - data[15])
        ninepatch_right = (data[23], height - data[27], height - data[27] - data[23])
        ninepatch_top = (data[35], data[39], data[39] - data[35])
        ninepatch_left = (data[43], data[47], data[47] - data[43])
        # print(f'Bottom: {ninepatch_bottom}')
        # print(f'Right: {ninepatch_right}')
        # print(f'Top: {ninepatch_top}')
        # print(f'Left: {ninepatch_left}')

        chunk_info = {
            "Bottom": ninepatch_bottom,
            "Right": ninepatch_right,
            "Top": ninepatch_top,
            "Left": ninepatch_left
        }

        # Bottom Start Padding Left[15]
        # print(data[12],data[13],data[14],data[15])
        # Bottom Start Padding Right[19]
        # print(data[16],data[17],data[18],data[19])

        # Right Start Padding Top[23] 0 0 0 36
        # print(data[20],data[21],data[22],data[23])
        # Right End Padding Bottom[27] 0 0 0 17
        # print(data[24],data[25],data[26],data[27])

        # print(data[28],data[29],data[30],data[31])

        # Top Start[35]
        # print(data[32],data[33],data[34],data[35])
        # Top End[39]
        # print(data[36],data[37],data[38],data[39])

        # Left Start[43] 0 0 0 22
        # print(data[40],data[41],data[42],data[43])
        # Left End[47] 0 0 0 54
        # print(data[44],data[45],data[46],data[47])

        # print(data[48],data[49],data[50],data[51])
        # print(data[52],data[53])

        # not working
        self.paddingLeft = data[0]
        self.paddingRight = data[1]
        self.paddingTop = data[2]
        self.paddingBottom = data[3]
        self.numXDivs = (len(data) - 4) // 2
        self.numYDivs = self.numXDivs
        self.xDivs = data[4:4 + self.numXDivs]
        self.yDivs = data[4 + self.numYDivs:]

    def getXDivs(self):
        return self.xDivs

    def getYDivs(self):
        return self.yDivs

    def serializedSize(self):
        return 4 + 2 * self.numXDivs + 2 * self.numYDivs


class NinePatchPeeker:
    def __init__(self):
        self.mPatch = None
        self.mPatchSize = 0
        self.mHasInsets = False
        self.mOpticalInsets = np.zeros(4, dtype=np.uint8)
        self.mOutlineInsets = np.zeros(4, dtype=np.uint8)
        self.mOutlineRadius = 0.0
        self.mOutlineAlpha = 0

    def readChunk(self, tag, data, length):
        if tag == "npTc":
            # print(tag, length)
            patch = Res_png_9patch(data)
            # print(patch.numXDivs, patch.numYDivs, '\n上下', patch.paddingTop, patch.paddingBottom, '\n左右', patch.paddingLeft, patch.paddingRight)
            patchSize = patch.serializedSize()
            # print(patchSize)
            if length != patchSize:
                return False

            # patchNew = Res_png_9patch(data)
            #
            # patchNew.deserialize()
            # self.mPatch = patchNew
            # self.mPatchSize = patchSize
        elif tag == "npLb" and length == 16:
            self.mHasInsets = True
            self.mOpticalInsets = np.frombuffer(data, dtype=np.uint8)
        elif tag == "npOl" and length == 24:
            self.mHasInsets = True
            self.mOutlineInsets = np.frombuffer(data[:16], dtype=np.uint8)
            self.mOutlineRadius = np.frombuffer(data[16:20], dtype=np.uint8)[0]
            self.mOutlineAlpha = np.frombuffer(data[20:24], dtype=np.uint8)[0] & 0xff
        return True

    def scaleDivRange(self, divs, scale, maxValue):
        divs = (divs * scale + 0.5).astype(np.uint8)
        for i in range(1, len(divs)):
            if divs[i] == divs[i - 1]:
                divs[i] += 1
        if divs[-1] > maxValue:
            highestAvailable = maxValue
            for i in range(len(divs) - 1, -1, -1):
                divs[i] = highestAvailable
                if i > 0 and divs[i] <= divs[i - 1]:
                    highestAvailable = divs[i] - 1
                else:
                    break

    def scale(self, scaleX, scaleY, scaledWidth, scaledHeight):
        if self.mPatch is None:
            return
        if scaleX != 1.0:
            self.mPatch.paddingLeft = int(self.mPatch.paddingLeft * scaleX + 0.5)
            self.mPatch.paddingRight = int(self.mPatch.paddingRight * scaleX + 0.5)
            self.scaleDivRange(self.mPatch.getXDivs(), scaleX, scaledWidth - 1)
        if scaleY != 1.0:
            self.mPatch.paddingTop = int(self.mPatch.paddingTop * scaleY + 0.5)
            self.mPatch.paddingBottom = int(self.mPatch.paddingBottom * scaleY + 0.5)
            self.scaleDivRange(self.mPatch.getYDivs(), scaleY, scaledHeight - 1)


def read_nine_patch(image_path):
    with open(image_path, 'rb') as f:
        data = f.read()

    global width, height
    image = Image.open(image_path)
    width, height = image.size
    image.close()
    peeker = NinePatchPeeker()
    offset = 8  # Skip PNG signature
    while offset < len(data):
        length = int.from_bytes(data[offset:offset + 4], byteorder='big')
        tag = data[offset + 4:offset + 8].decode('utf-8')
        chunk_data = data[offset + 8:offset + 8 + length]
        peeker.readChunk(tag, chunk_data, length)
        # print(peeker.readChunk(tag, chunk_data, length))
        offset += length + 12

    return peeker


# 传入NinePatch图像路径
def main(image_path):
    global chunk_info
    chunk_info = {}
    peeker = read_nine_patch(image_path)
    return chunk_info


if __name__ == '__main__':
    image_path = './test/myninepatch2.9.png'
    image_path = pyperclip.paste()
    result = main(image_path)
    print(result)

# print(peeker)
# print(patch)
# if peeker.mPatch:
#     print("Padding:",
#         (peeker.mPatch.paddingLeft, peeker.mPatch.paddingRight, peeker.mPatch.paddingTop,
#          peeker.mPatch.paddingBottom))
#     print("X Divs:", peeker.mPatch.getXDivs())
#     print("Y Divs:", peeker.mPatch.getYDivs())

# # 对NinePatch图像进行缩放
# scaleX = 2.0
# scaleY = 2.0
# scaledWidth = 400  # 假设目标宽度为400
# scaledHeight = 400  # 假设目标高度为400
# peeker.scale(scaleX, scaleY, scaledWidth, scaledHeight)
