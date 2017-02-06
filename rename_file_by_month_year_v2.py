import os
from time import gmtime
import time
from PIL import Image
import PIL.ExifTags
import re

top_folder = os.getcwd()
dest_top = top_folder +'\\001_ordered_files\\'
dest_other = top_folder + '\\002_needs attention\\'
pic_vid_files_to_move = {}
other_files_to_move = {}

# create serialized file to store with pictures
try:
    f=open("sys_ser_num.py", "r")
except:
    f = open("sys_ser_num.py", "w")
    f.write("0")
    f.close()


def change_names():
    start = time.time()
    count_files = 0
    ser_num_file = open("sys_ser_num.py", "r")
    count_start = int(ser_num_file.read())
    count_vid_pic_files = count_start
    count_dirs = 0
    other_files_count = 0

    # walk through all folders within top_folder and find folders and files
    for path, dirnames, filenames in os.walk(str(top_folder)):
        count_dirs += len(dirnames)
        # iterate over each file in the directories and select video and picture files
        for file in filenames:
            count_files += 1

            # check if file allready renamed, if so let it stay
            pat_renamed_files = re.compile(r'^[01][0-9]{4}\s[0-9]+[-][12][0-9]{3}')
            if pat_renamed_files.search(file) != None:
                continue
            i = file.split('.')[-1].lower()
            if i in pic_ext:             
                try:
                    count_vid_pic_files += 1
                    img = PIL.Image.open(str(path + '\\' + file))
                    exif = {PIL.ExifTags.TAGS[k]:v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS}

                    file_created_year = exif['DateTime'][:4]
                    file_created_month = exif['DateTime'][5:7]
                    print(exif['DateTime'][:10] + '-' + exif['DateTime'][11:], file_created_year, file_created_month)

                # """
                # There is no exif info on the file, therefore most possibly
                # a videofile or a altered picfile. Anyways is should be moved to a
                # folder for the user to select correct action. Do NOT change
                # name of file.
                # -- A test could be made to see if the file has it's creation
                # year and month in the filename, then it should be possible
                # to give a filename and put i correct folder. (another try except
                # within this exception :)
                # """
                except AttributeError as e:
                    print(e, path, file)
                    continue
                #     print("except", file)
                    # #get year and month the file was created
                    # file_stat = os.stat((path+'\\'+file))
                    # file_created_year = gmtime(file_stat.st_ctime).tm_year
                    # file_created_month = gmtime(file_stat.st_ctime).tm_mon
                # src file and path name
#==============================================================================
#                 src_file = "{}{}{}".format(path, '\\', file)
# 
#                 # dest file and path name
# 
#                 new_file_number = str(count_vid_pic_files).zfill(5)
#                 new_file_name = "{} {}-{}.{}".format(new_file_number, file_created_month, file_created_year, file.split('.')[-1])
#                 dest_file = "{}{}\{}\\{}".format(dest_top, file_created_year, file_created_month, new_file_name)
# 
#                 # src and dest into dictionary
#                 pic_vid_files_to_move[src_file] = dest_file
#==============================================================================
            elif i in vid_ext:
                coh = re.compile(r'[12][09][0-9]{2}[01][0-9][0-3][0-9]')
                year = re.compile(r'[12][09][0-9]{2}')
                print(file)
                match_coh = coh.search(file)
                match_year = year.search(file)
                if match_coh != None:
                    print(match_coh.group(), file)
                elif match_year != None:
                    print(match_year.group(), file)


            else:
                if i != "py" :
                    other_files_count += 1
                    src_other_file = "{}\\{}".format(path, file)
                    dst_other_file = "{}{}".format(dest_other, file)

                    other_files_to_move[src_other_file] = dst_other_file

    for key, value in pic_vid_files_to_move.items():
        src = key
        dst = value
        try:
            os.renames(str(src), str(dst))
        except:
            print("Unsuccessfull: {}".format(src))



    for key, value in other_files_to_move.items():
        src = key
        dst = value
        try:
            os.renames(str(src), str(dst))
            # print("Other success")
        except:
            print("Unsuccessfull: {}".format(src))

    end = time.time() - start
    print("\nIterated over {} files, within {} folders.\n"
          "Found {} video/picture files.\n"
          "Fount {} other files.\n"
          "in {} seconds".format(str(count_files), str(count_dirs), str(count_vid_pic_files), str(other_files_count), str(end)))

    # update file sys_ser_num.txt
    f = open("sys_ser_num.py", 'w')
    f.write(str(count_vid_pic_files))
    f.close()

vid_ext =  ['ogg', 'avi', 'webm', 'f4p ', 'f4a', 'flv', '3gp', 'ppm',
            'asf', 'f4b ', 'yuv', 'svi', 'm4v', 'ani', 'mac', 'f4a ',
            'mpeg', 'drc', 'roq', 'mp2', 'ras', 'mpe', 'pcx', 'vob',
            'mp4 ', 'pbm', 'mpg ', 'f4p', 'pcd', 'cal', 'jpe', 'wmf',
            'flv ', 'mkv', 'amv', 'mpe ', 'ogv ', 'wmv', 'tga', 'jbg',
            '3g2', 'mpeg ', 'mpv', 'mxf', 'qt', 'f4b', 'fax', 'gifv',
            'm4p ', 'mpg', 'ogv', 'psd', 'pgm', 'm2v', 'nsv', 'mp4',
            'rmvb', 'rm', 'mov, ', 'mov', 'f4v ']
            


pic_ext =  ['jpeg', 'jpg', 'webp', 'gif', 'png', 'napng', 'mng', 'tiff',
            'svg', 'pdf', 'xbm', 'bmp', 'ico', 'pct']

            
            
            
if __name__ == "__main__":
    change_names()
