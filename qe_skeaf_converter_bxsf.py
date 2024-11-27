#This is code for converitng bxsf file generated by Quantum Espresso to the format suitable for SKEAF(A code to simulate dHvA frequency)
#This program writes fermi energy and band energy in Rydberg unit in bxsf file. QE produce bxsf file in eV units.
#this code is written by Navneet Kumar Karn at CSIR-NPL
import numpy as np
import glob
# Function to load the bxsf file
def load_file():
    # Ask the user for the file name
    file_name = input("Please enter the file name (with extension): ")
    mylines = [] 						                                                            # Declare an empty list named mylines.
    try:
        # Open and read the file
        with open(file_name, 'r') as file:
            lines = len(file.readlines())
            print("File content loaded successfully!")
        with open(file_name, 'rt') as file:
            for myline in file:                		                                                # For each line, stored as myline
                mylines.append(myline)
            print("Fermi energy in eV:",mylines[7][23:30], "\nThe no. of bands:", mylines[12])      # Display the Fermi energy in eV and no of bands
            band_num=int(mylines[12][4])
            E_f=str(0.0734985857*float(mylines[7][23:30]))                                          #Convert the Fermi energy in Rydberg unit
            mylines[7]=mylines[7].replace(mylines[7][23:30], E_f, 1)                                #Replace E_f in Rydberg unit in mylines
            mylines[12]=mylines[12].replace(mylines[12][4], '1', 1)                                 #Replce no. of bands by one as each resulting file have one band only 
            f = open("Band"+mylines[18][7:9]+".bxsf", 'w')                                          #Creat new file to store band data in eV unit
            for i in range(19,lines-3):                                                             #Store the energy data in eV for each band in seperate bxsf file
                if mylines[i][0:4]=='BAND':                                                         #having file names Band+bandnumber.bxsf 
                    f.close()
                    f = open("Band"+mylines[i][7:9]+".bxsf", 'w')
                else:
                    f.write(mylines[i])
            f.close()                                                                               
            files=glob.glob("*.bxsf")                                                               #sort and store banddata filenames
            files.sort()
            for i in range(band_num):   
                f.close()                                                                           #load each band data file as numpyarray
                a=np.loadtxt(files[i])*0.0734985857                                                 #convert to Rydberg unit in one go and store the data in numpy array
                open(files[i], 'w').close()                                                         #erase all band data in eV from the file
                f=open(files[i],'w')                                                                #open the same bxsf file and write intial format of a bsxf file
                for j in range(18):
                    f.write(mylines[j])
                f.write('BAND:  '+ files[i][4:6]+'\n')
                np.savetxt(f, a)                                                                    #Now write band data in Rydberg unit
                mylines[lines-3]=mylines[lines-3].replace(mylines[lines-3],str(0.073498585*float(mylines[lines-3][3:10])),1)
                f.write(mylines[lines-3])
                f.write('\n'+'END_BANDGRID_3D'+'\n'+'END_BLOCK_BANDGRID_3D')                        #End the bxsf file in it's format and close it
            f.close() 
        print('Programmed worked, do check number of bands in orignal bsxf file and number of output are same or not!')   
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to load the file and print the bxsf file for each band in Rydberg unit.
load_file()