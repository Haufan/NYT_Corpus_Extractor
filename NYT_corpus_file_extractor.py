import os
import tarfile


def create_file_list():
    '''Reads 'files_not_included.csv' and creates an ordered list of all file names.'''

    #creates path of file
    path = os.path.abspath('./')
    _temp_file_name = os.path.join(path, 'files_not_included.csv')

    #reads file and creates ordered list of article names
    with open(_temp_file_name, 'r', encoding="utf8") as _temp_file:
        _temp_text = _temp_file.read()
        _temp_list = _temp_text.split('\n')
        _temp_list.sort()

    return _temp_list


def find_files(file_list):
    '''Copies all files from file_list from NYT-Corpus into output.'''

    path = os.path.abspath('./')

    for article in file_list[1:]:     #empty entry
        _year = article[0:4]
        _month = article[5:7]
        _file_path = article[5:].replace('_', '/')

        #creates input path for tgz-file
        _input_path = os.path.join(path, 'NYT-all-87-96', 'NYT-all-87-96', _year,
                                   _month + '.tgz')
        #access file in tgz-file and write content into new file (output)
        with tarfile.open(_input_path, 'r:gz') as tar:
            fileobj = tar.extractfile(_file_path)
            file_data = fileobj.read()

            g = open(os.path.join(path, 'output', article), "wb")
            g.write(file_data)


if __name__ == '__main__':
    file_list = create_file_list()
    find_files(file_list)
