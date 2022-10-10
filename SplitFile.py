# Using readlines()
import os
import glob


def getSeqPositions(line):
    seqPositionsStrArray = line.strip().replace(
        '\n', '').replace('>', '').split('..')
    seqPositionsIntArray = [int(numeric_string)
                            for numeric_string in seqPositionsStrArray]
    return seqPositionsIntArray


# Read fasta file and prepare fasta sequence string
fastaFilePath = glob.glob("./data/*.fasta")
fastaFile = open(fastaFilePath[0], 'r')
print('fastaFile: ', fastaFile)
fastaFileStr = ''
i = -1
for line in fastaFile:
    i = i+1
    if(i != 0):
        fastaFileStr = fastaFileStr+line.replace('\n', '')

genpeptFilePath = "./data/*.genpept"

for filename in glob.glob(genpeptFilePath):
    with open(filename, 'r') as f:
        version = ''
        folderpath = ''
        filePath = ''
        positions = []
        regionNameStrTokens = []
        noteStrTokens = []
        for line in f:
            if line.startswith('VERSION'):
                version = line.split()[1]
                # Create folder with version name
                folderpath = "./data/"+version
                if not os.path.exists(folderpath):
                    os.makedirs(folderpath)

            if line.strip().upper().startswith('REGION'):
                positions = getSeqPositions(line.upper().split('REGION', 1)[1])

            if 'region_name' in line:
                regionNameStrTokens = line.upper().split('"')
                print('regionName: ', regionNameStrTokens)

            if '/note' in line:
                noteStrTokens = line.upper().split('"')
                print('regionName: ', regionNameStrTokens)

            print(line)
            print('############# version:', version, '  positions: ',
                  len(positions), '  regionName: ', len(regionNameStrTokens))

            if (len(positions) != 0 and len(regionNameStrTokens) != 0 and version != '' and len(noteStrTokens)):
                print('@@@@@@@@@@ condition: TRUE')
                filePath = "./data/"+version+"/"+version + \
                    "_"+str(positions[0])+"_" + \
                    str(positions[1])+"_"+regionNameStrTokens[1] + \
                    "_"+noteStrTokens[1].replace(';', '')
                f = open(filePath, 'a')
                f.write(fastaFileStr[positions[0]-1:positions[1]-1])
                f.close()
                folderpath = ''
                filePath = ''
                positions = []
                regionNameStrTokens = []
