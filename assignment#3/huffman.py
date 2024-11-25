import pickle
class huffmannode:
    def __init__(self, char,freq,left,right):
        self.ch=char
        self.probability=freq
        self.left=left
        self.right=right
def sortNodes(list):
    list.sort(key = lambda node:node.probability)
def DFS_traverse_tree(string,currentnode,codes):
    if(currentnode == None):
        return
    DFS_traverse_tree(string+"0",currentnode.left,codes)
    DFS_traverse_tree(string+"1",currentnode.right,codes)
    if(currentnode.ch!=None):
        codes[currentnode.ch]=string
    

class Huffman:
    def __init__(self, inputfilename, outputfilename):
        self.inname = inputfilename
        self.outname = outputfilename
    def build_tree(self):
        with open(self.inname) as file:
            text = file.read()
        self.txt=text
        frequencies = {}
        nodes=[]
        for i in text:
            if i not in frequencies:
                frequencies[i]=0
            frequencies[i]+=1
        for symbol,freq in frequencies.items():
            nodes.append(huffmannode(symbol,freq/len(text),None,None))
        while len(nodes)>1:
            sortNodes(nodes)
            left = nodes.pop(0)
            right = nodes.pop(0)
            nodes.append(huffmannode(None,left.probability+right.probability,left,right))
        return nodes
    def compress(self):
        nodes=self.build_tree()
        root = nodes[0]
        finalcode={}
        DFS_traverse_tree("",root,finalcode)
        
        binary_string = ""
        for char in self.txt:
            binary_string+=finalcode[char]
        print("Binary representation: ",binary_string)
        added_string = (8 - len(binary_string) % 8) % 8  # to fill the rest of bits to make the number of bits divisible by 8
        binary_string += "0" * added_string
        packed_data = bytearray()
        for i in range(0, len(binary_string), 8):
            byte = binary_string[i:i + 8]
            packed_data.append(int(byte, 2))#to avoid overflow
        with open(self.outname, 'wb') as file:
            pickle.dump(finalcode, file)
            file.write(packed_data)
        print("text compressed successfully")
    def decompress(self):
        with open(self.outname, 'rb') as file:
            huffman_codes = pickle.load(file)
            packed_data = file.read()
            binary_string = ""
            for byte in packed_data:
                binary_string+=format(byte,"08b")
            inverted_codes = {}
            for key,value in huffman_codes.items():
                inverted_codes[value]=key
            decoded_text = ""
            temp = ""
            for bit in binary_string:
                temp += bit
                if temp in inverted_codes:
                    decoded_text += inverted_codes[temp]
                    temp = "" 
            with open(self.outname,'w')as file:
                file.write(decoded_text)
            print("data decompressed successfully")
def comparebetweenfiles(filename1,filename2):
    with open(filename1)as file:
        text1=file.read()
    
    with open(filename2)as file:
        text2=file.read()
    if text1 == text2:
        print("the data is compressed and decompressed successfully")
    else:
        print("there is an error in compressing or decompressing data")
    
obj = Huffman("input.txt", "output.txt")

obj.compress()
obj.decompress()
comparebetweenfiles("input.txt","output.txt")