#Test bench Generator for one-module, top-level combinational designs

import re
import os

#Function to search for the module's name on the Verilog design

def getModuleName(file):
    print("Obtaining module name...")
    file = open (file_name,'r')
    pattern = '^module'
    for line in file:
        line = line.strip()
        if re.search(pattern, line):
            moduleLine = re.search('module *([\w\d_].+) *[\(]', line) #Regular expression to obtain
                                                                      #the module's name
            moduleName = (moduleLine.group(1))
            moduleName = moduleName.split()
    file.close()
    return (moduleName[0])

#Function to save the input names and their bit sizes on a list

def getInputName(file):
    print("Obtaining input list...")
    file = open (file_name,'r')
    pattern = '^input'
    inputList = []
    for line in file:
        line = line.strip()
        if re.search(pattern, line):
            inputLine = re.search('input *(.\w+.*)([,);])', line)
            inputName = (inputLine.group(1))
            if inputName.split(sep=','):
                inputName = inputName.split(sep=',')
            else:
                inputName = inputName.split(sep=';')
            inputList = inputList+inputName
    for index, value in enumerate(inputList):
        inputList[index] = value.replace(")", "")
    for index, value in enumerate(inputList):
        inputList[index] = value.replace(" ", "")
    file.close()
    return (inputList)

#Function to save the output names and their bit sizes on a list

def getOutputName(file):
    print("Obtaining output list...")
    file = open (file_name,'r')
    pattern = '^output'
    outputList = []
    for line in file:
        line = line.strip()
        if re.search(pattern, line):
            outputLine = re.search('output *(.\w+.*)([,);])', line)
            outputName = (outputLine.group(1))
            if outputName.split(sep=','):
                outputName = outputName.split(sep=',')
            else:
                outputName = outputName.split(sep=';')
            outputList = outputList+outputName
    for index, value in enumerate(outputList):
        outputList[index] = value.replace(")","")
    for index, value in enumerate(outputList):
        outputList[index] = value.replace(" ", "")
    file.close()
    return (outputList)

#Generator function. Calls the previous functions to get the information needed to create the test bench file

def Generate_TB(getmodule, getinput, getoutput):
    print("Generating Test Bench SystemVerilog file...")
    route = getmodule+"_TB.sv"
    file = open (route,'w')
    file.write("`timescale 1ns/1ps\n\n")
    file.write("module "+getmodule+"_TB();\n\n")
    for str in getinput:
        file.write("\treg "+str+"_TB;\n")
    for str in getoutput:
        file.write("\twire "+str+"_TB;\n")

    file.write("\n\t\t"+getmodule+" UUT (")
    for item in getinput:
        if re.search("\[.*\]", item):
            inputline = re.search("(\[.*\])(.*)", item)
            file.write("."+inputline.group(2)+"("+inputline.group(2)+"_TB), ")
        else:
            file.write("."+item+"("+item+"_TB), ")
    for item in getoutput:
        if re.search("\[.*\]", item):
            outputline = re.search("(\[.*\])(.*)", item)
            file.write("."+outputline.group(2)+"("+outputline.group(2)+"_TB), ")
        else:
            file.write("."+item+"("+item+"_TB), ")

    file.seek(file.tell() - 2, os.SEEK_SET)
    file.write(");\n\n")
    file.write("\tinteger for_counter = 0;\n\n")

    #The following section is used to account for all possible combinations in the top-level

#############################################################################################

    buslist = []
    bitlist = []
    multibitcount = 0
    bittotal = 0

    #Method to concatenate all inputs into one vector, in which an integer is going to
    #be assigned

    for item in getinput:
        if re.search("\[.*\]", item):
            inputline = re.search("(\[.*\])(.*)", item)
            str = inputline.group(2)+"_TB "+inputline.group(1)
            buslist.append(str)
        else:
            str = item+"_TB"
            buslist.append(str)
    
    #Method to calculate the total amount of bits required to represent the number of all
    #possible combinations in the design

    for var in getinput:
        if re.search("\[(\d*):(\d*)\].*", var):
            inputline = re.search("\[(\d*):(\d*)\].*", var)
            if int(inputline.group(2)) > int(inputline.group(1)):
                bitnum = int(inputline.group(2))
            else:
                bitnum = int(inputline.group(1))
            bitlist.append(bitnum)
    for bits in bitlist:
        multibitcount += bits
    bittotal = multibitcount+len(getinput)

#############################################################################################

    file.write("\tinitial begin\n\n")
    file.write('\t\t$dumpfile("'+getmodule+'.vcd");\n')
    file.write('\t\t$dumpvars(1, '+getmodule+'_TB);\n\n')
    combinations = "% s" % (2**bittotal)
    file.write("\t\tfor (for_counter = 0; for_counter < "+combinations+"; for_counter++) begin\n")
    file.write("\t\t\t{")
    for item in buslist:
        file.write(item+", ")
    file.seek(file.tell() - 2, os.SEEK_SET)
    file.write("} = for_counter;\n\t\t\t#2;\n\t\tend")
      
    file.write("\n\n")
    file.write("\t\t$finish;\n\n")
    file.write("\tend\n\n")
    file.write("endmodule")

    file.close()


#Main program. Receives the file name via user's input and calls all functions to generate the
#test bench required for the design


file_name = input("Type the name of your project: ")
Generate_TB(getModuleName(file_name), getInputName(file_name), getOutputName(file_name))
print("File created successfully")