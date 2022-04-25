import os

def run():
    print("--- react2gatsby_images ---")    
    filesToProcess = os.listdir("input/")
    for file in filesToProcess:
        processFile("input/" + file, "output/" + file, "")

def processFile(file_path, output_path, message):
    
    print("Reading " + file_path + " ...")
    fileTuple = readFile(file_path)
    print("Processing...")
    rowsList = fileTuple[0]
    targetVariables = fileTuple[1]

    newRowsList = []
    for row in rowsList:
        newRow = row
        if "<img" in row and "src=" in row:
            for key, value in targetVariables.items():
                posibleMatches = [
                    "{" + key + "}",
                    "{ " + key + "}",
                    "{" + key + " }",
                    "{ " + key + " }"
                ]
                for posibleMatch in posibleMatches:
                    if posibleMatch in row:
                        newRow = newRow.replace("<img", "<StaticImage")
                        #BAM!!! src={pathVar} -> src="../path"
                        newRow = newRow.replace(posibleMatch, value + message) 
                        
        newRowsList.append(newRow)                            
    
    printFile(output_path, newRowsList)
    print("Output generated successfully in " + output_path + " !")


def readFile(filePath):
    rowsList = []
    targetVariables = {}

    with open(filePath, "r", encoding="utf-8") as f:
        for row in f:
            rowsList.append(row)            
            if "../../images/" in row:
                try:
                    rowTokenized = row.split()
                    if len(rowTokenized) == 4:
                        targetVariables[rowTokenized[1]] = rowTokenized[3].replace(";", "")                    
                except: 
                    pass
                
    return (rowsList, targetVariables)
    
def printFile(fileName, rows):
    with open(fileName, "w" ,encoding="utf-8") as f:
        f.write("import { StaticImage } from \"gatsby-plugin-image\";")
        for row in rows:
            f.write(row)

if __name__ == '__main__':
    run()