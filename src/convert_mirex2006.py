# File: convert_mirex2006.py
# Author: Amir Harati
# This script conver the beat label files to Jibo beat trcker format.
# Each line will indicate one beat. For each annotation we generate a
#  different file and number the files.
#  Also  wave file should be ocnverted 16000 Hz (elsewhere) and
#  tempo labels rename by adding a _temp to their name (elsewhere)

import sys
import getopt


def main(argv):
    input_list_file = ""
    out_dir = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ilist=", "odirectory="])
    except getopt.GetoptError:
        print ('convert_mirex2006.py -i <input_list> -o <output_directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('convert_mirex2006.py -i <input_list> -o <output_directory>')
            sys.exit()
        elif opt in ("-i", "--ilist"):
            input_list_file = arg
        elif opt in ("-o", "--odirectory"):
            out_dir = arg
            pass
        pass

    # read the input list
    input_list = [line.strip() for line in open(input_list_file)]

    # loop over all files in the list read them and extract beat labels
    # and output them in out directory
    for fi in input_list:
        file_lines = [line.strip() for line in open(fi)]
        # each line (beat labels space seperated) in outputed to a different
        # file.
        temp_file_path = fi.split("/")
        temp_file_base = temp_file_path[-1:][0].split(".")[0]
        count = 1
        for line in file_lines:
            beats = [word for word in line.split('\t')]
            # print(beats)
            ofile = open(out_dir + "/" + temp_file_base + "_" + str(count) + ".lab", "w")
            ofile.write("\n".join(beats))
            ofile.close()
            count += 1
            pass
        pass

if __name__ == "__main__":
    main(sys.argv[1:])

