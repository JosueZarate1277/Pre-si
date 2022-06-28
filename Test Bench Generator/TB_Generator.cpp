//Test bench Generator for one-module, top-level combinational designs

#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <cmath>

using namespace std;


//Function to search for the module's name on the Verilog design

int getModuleName(std::fstream& file, std::string& file_name, std::string& module_Name){
    std::regex pattern("^module *([\\w\\d_].+) *[\\(]");
    smatch m;
    file.open(file_name, ios::in);
    if (file.is_open()){
        string line;
        while (getline(file, line)){
            if (regex_search(line, m, pattern)){
                regex_search(line, m, pattern);
                module_Name = m[1].str();
            }
        }
        file.close();
    }
    return 0;
}


//Function to save the input names and their bit sizes on a list

int getInputList(std::fstream& file, std::string& file_name, vector<string>& inputList){
    string inputName;
    std::regex pattern("input *(.\\w+.*)([,);])");
    smatch m;
    file.open(file_name, ios::in);
    if (file.is_open()){
        string line;
        while (getline(file, line)){
            if (regex_search(line, m, pattern)){
                regex_search(line, m, pattern);
                stringstream inputLine (m[1].str());
                while (inputLine.good()){
                    string inputName;
                    getline(inputLine, inputName, ',');
                    inputList.push_back(inputName);
                    //cout << inputName << endl;
                }
            }
        }
        string cleaning;
        for (int i=0; i < inputList.size(); i++){
            cleaning = inputList[i];
            remove(cleaning.begin(), cleaning.end(),')');
            inputList[i] = cleaning;
        }
        file.close();
    }
    return 0;
}


//Function to save the output names and their bit sizes on a list

int getOutputList(std::fstream& file, std::string& file_name, vector<string>& outputList){
    string outputName;
    std::regex pattern("output *(.\\w+.*)([,);])");
    smatch m;
    file.open(file_name, ios::in);
    if (file.is_open()){
        string line;
        while (getline(file, line)){
            if (regex_search(line, m, pattern)){
                regex_search(line, m, pattern);
                stringstream outputLine (m[1].str());
                while (outputLine.good()){
                    string outputName;
                    getline(outputLine, outputName, ',');
                    outputList.push_back(outputName);
                    //cout << inputName << endl;
                }
            }
        }
        string cleaning;
        for (int i=0; i < outputList.size(); i++){
            cleaning = outputList[i];
            cleaning.erase(remove(cleaning.begin(), cleaning.end(),')'), cleaning.end());
            outputList[i] = cleaning;
        }
        file.close();
    }
    return 0;
}


//Generator function. Calls the previous functions to get the information needed to create the test bench file

int generate_TB(string& module_Name, vector<string>& inputList, vector<string>& outputList){
    ofstream TB_File;
    string TB_Name = module_Name+"_TB.sv";
    TB_File.open(TB_Name, ofstream::out | ofstream::trunc);
    if (TB_File.is_open()){
        TB_File << "`timescale 1ns/1ps \n\n";
        TB_File << "module "+module_Name+"_TB();\n\n";
        for(auto &itr : inputList){
			TB_File << "\treg "+ itr + "_TB" +";\n";
		}
		for(auto &itr : outputList){
			TB_File << "\twire "+ itr + "_TB" + ";\n";
		}
		TB_File << "\n";
		TB_File << "\t" +module_Name+ " UUT (";
		
        //Add .input(input) and .output(output)
		for(auto &itr : inputList){
			string str_format="";
			for(size_t p=0, q=0; p!=itr.npos; p=q)
               str_format =itr.substr(p+(p!=0),(q=itr.find(']', p+1))-p-(p!=0));
			
			TB_File << "." + str_format + "(" + str_format + "_TB" + "),";
		}
		for(auto &itr : outputList){
			string str_format="";
			for(size_t p=0, q=0; p!=itr.npos; p=q)
               str_format =itr.substr(p+(p!=0),(q=itr.find(']', p+1))-p-(p!=0));

			TB_File << "." + str_format + "(" + str_format + "_TB" + "),";
		}
        TB_File.seekp(-1, std::ios_base::cur);
		TB_File << ");\n\n";
        TB_File << "\tinteger for_counter = 0;\n";


        //The following section is used to account for all possible combinations in the top-level

        /////////////////////////////////////////////////////////////////////////////////////

        vector<string> busList;
        vector<int> bitList;
        int multibitcount = 0;
        int bittotal = 0;
        regex pattern ("(\\[.*\\])(.*)");
        regex brackets ("\\[.*\\]");
        regex multibit ("\\[(\\d*):(\\d*)\\].*");
        smatch m;

        //Method to concatenate all inputs into one vector, in which an integer is going to
        //be assigned

        for(auto &itr : inputList){
			if (regex_search(itr, m, brackets)){
                regex_search(itr, m, pattern);
                itr = m[2].str()+"_TB "+m[1].str();
                busList.push_back(itr);
            }
            else{
                itr = itr+"_TB";
                busList.push_back(itr);
            }
		}


        //Method to calculate the total amount of bits required to represent the number of all
        //possible combinations in the design

        for(auto &itr : inputList){
			if (regex_search(itr, m, multibit)){
                regex_search(itr, m, multibit);
                string num1_s = m[1].str();
                string num2_s = m[2].str();

                auto str1_n = std::strtol(num1_s.data(), nullptr, 0);
                int num1 = str1_n;
                auto str2_n = std::strtol(num2_s.data(), nullptr, 0);
                int num2 = str2_n;

                if (num2 > num1){
                        bitList.push_back(num2);
                    }
                else{
                        bitList.push_back(num1);
                }
            }
		}

        for(int i = 0; i < bitList.size(); i++){
			multibitcount += bitList[i];
		}
        bittotal = busList.size()+multibitcount;


        /////////////////////////////////////////////////////////////////////////////////////
        
        TB_File << "\treg [";
        int bus = bittotal - 1;
        string bussize = to_string(bus);
        TB_File << bussize+":0] inputbus_TB;\n\n";
        TB_File << "\tinitial begin\n\n";
        TB_File << "\t\t$dumpfile(\""+module_Name+".vcd\");\n";
        TB_File << "\t\t$dumpvars(1, "+module_Name+"_TB);\n\n";
        int combinations_i = pow(2,bittotal);
        string combinations = to_string(combinations_i);

        TB_File << "\t\tfor (for_counter = 0; for_counter < "+combinations+"; for_counter++) begin\n";
        TB_File << "\t\t\tinputbus_TB = for_counter;\n";
        TB_File << "\t\t\t{";
        for(auto &itr : busList){
            TB_File << itr+", ";
        }
        TB_File.seekp(-2, std::ios_base::cur);
        TB_File << "} = inputbus_TB;\n\t\t\t#2;\n\t\tend";
        TB_File << "\n\n";
        TB_File << "\t\t$finish;\n\n";
        TB_File << "\tend\n\n";
        TB_File << "endmodule";
    }
    TB_File.close();
    return 0;
}


//Main program. Receives the file name via user's input and calls all functions to generate the
//test bench required for the design

int main(){
    fstream file;
    string module_Name;
    vector<string> inputList;
    vector<string> outputList;
    string file_name;
    cout << "Type the name of your project: ";
    cin >> file_name;
    cout << "Obtaining module name...\n";    
    getModuleName(file, file_name, module_Name);
    cout << "Obtaining input list...\n";  
    getInputList(file, file_name, inputList);
    cout << "Obtaining output list...\n"; 
    getOutputList(file, file_name, outputList);
    cout << "Generating Test Bench Verilog file...\n"; 
    generate_TB(module_Name, inputList, outputList);
    cout << "File created succesfully";
}