import sys
import os
import glob
from xml.sax.saxutils import escape
import mojimoji

"""
Convert IME dictionary file to plist

Parameters
----------
EXPECT_SYS_ARGV_LENGTH : int
    Length of command line arguments to expect
"""

if __name__ == "__main__":
    EXPECT_SYS_ARGV_LENGTH = 3

    try:
        source_path = str(sys.argv[1])
        target_path = "./dist/"
    except IndexError:
        print("Fatal: You should be specify source file path.")
        print("Ex.) ptyhon index.py ./source.txt")
        sys.exit()
    except:
        print("Fatal: Unexpected error...")
        sys.exit()

    # If user specified target dir path, set one to target_path
    if len(sys.argv) >= EXPECT_SYS_ARGV_LENGTH and os.path.exists(sys.argv[2]):
        arg_path = str(sys.argv[2])

        # If last cahr is not '/', add it
        if arg_path[len(arg_path) - 1] == "/":
            target_path = arg_path
        else:
            target_path = arg_path + "/"

    # If source_path is not exists, exit program
    if not os.path.exists(source_path):
        print("No such file or directory: " + source_path)
        sys.exit()

    file_num = len(glob.glob(target_path + "*.plist"))
    target_file_path = "{}pl{}.plist".format(target_path, int(file_num) + 1)

    # If target_path is not exists, make it
    if not os.path.exists(target_path):
        os.makedirs(target_path)

        new_file = open(target_file_path, "w")
        new_file.write("")
        new_file.close()

    src_f = open(source_path, "r")
    tgt_f = open(target_file_path, "a")

    # Write header
    tgt_f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    tgt_f.write('<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
    tgt_f.write('<plist version="1.0">\n')
    tgt_f.write('<array>\n')

    # Read source_path
    for line in src_f:
        line_strs = line.split("\t")

        # If line is not header
        if len(line_strs) >= 3:
            phrase = escape(line_strs[1])
            shortcut = mojimoji.zen_to_han(line_strs[0], kana=False, digit=False, ascii=True)

            # Write contents
            tgt_f.write("\t<dict>\n")
            tgt_f.write("\t\t<key>phrase</key>\n")
            tgt_f.write("\t\t<string>" + phrase + "</string>\n")
            tgt_f.write("\t\t<key>shortcut</key>\n")
            tgt_f.write("\t\t<string>" + shortcut + "</string>\n")
            tgt_f.write("\t</dict>\n")

    # Write footer
    tgt_f.write('</array>\n')
    tgt_f.write('</plist>\n')

    src_f.close()
    tgt_f.close()
