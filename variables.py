from os import listdir
from os.path import isfile, join
from os import walk



def get_files(mypath, suffix):

    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):

        filtered_filenames = []
        for fname in filenames:

            # remove dot files
            if fname[0] == '.':
                continue

            #match only given suffix
            if not(fname.lower().endswith(suffix)):
                continue

            #make it into full path
            fname = dirpath + '/' + fname

            filtered_filenames.append(fname)

        f.extend(filtered_filenames)
        #break
    return f


def write_files(fs):

    with open('files.txt', 'a') as ffile:
        ffile.write('[py]\n')
        for m in fs:
            if m.lower().endswith('.py'):
                ffile.write(m + '\n')

        ffile.write('\n')
        ffile.write('[cpp]\n')
        for m in fs:
            if m.lower().endswith( ('.c++', '.cpp', '.h') ):
                ffile.write(m + '\n')


if __name__ == '__main__':
    rdir = '../plasmabox/corgi'

    fs = get_files(rdir, ('.py', '.c++', '.h'))
    write_files(fs)




