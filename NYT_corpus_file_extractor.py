from alive_progress import alive_bar
import os
import tarfile


def check_files():
    """ Checks if necessary folders and files exist. """

    print('Checking for folders and files ... \n')

    # checks if folder 'output' exists, if not creates it
    if not os.path.exists('NYT-all-87-96/NYT-all-87-96/1987/01.tgz'):
        print('ERROR:   There is no folder NYT-all-87-96/NYT-all-87-96.')
        exit()

    # checks for file with wanted articles
    if not os.path.isfile('files_not_included.csv'):
        print('ERROR:   There is no file files_not_included.csv.')
        exit()

    # checks if folder 'output' exists, if not creates it
    if not os.path.exists('output'):
        os.makedirs('output')


def create_file_list():
    """ Reads 'files_not_included.csv' and creates an ordered list of all file names. """

    print('Creating list of wanted articles ...\n')

    # creates path of file
    path = os.path.abspath('./')
    _temp_file_name = os.path.join(path, 'files_not_included.csv')

    # reads file and creates ordered list of article names
    with open(_temp_file_name, 'r', encoding="utf8") as _temp_file:
        _temp_text = _temp_file.read()
        _temp_list = _temp_text.split('\n')
        _temp_list.sort()

    return _temp_list


def find_files(file_list):
    """ Copies all files from file_list from NYT-Corpus into output. """

    print('Extracting wanted articles files ...\n')

    path = os.path.abspath('./')

    # initiate progress bar
    with alive_bar(len(file_list[1:]), force_tty=True) as bar:

        for article in file_list[1:]:  # empty entry
            _year = article[0:4]
            _month = article[5:7]
            _file_path = article[5:].replace('_', '/')

            # creates input path for tgz-file
            _input_path = os.path.join(path, 'NYT-all-87-96', 'NYT-all-87-96', _year,
                                       _month + '.tgz')
            # access file in tgz-file and write content into new file (output)
            with tarfile.open(_input_path, 'r:gz') as tar:
                file_obj = tar.extractfile(_file_path)
                file_data = file_obj.read()

                g = open(os.path.join(path, 'output', article), "wb")
                g.write(file_data)

            # execute progress bar
            bar()

    print('Wanted articles files can be found in folder output.')


if __name__ == '__main__':
    check_files()
    file_list = create_file_list()
    find_files(file_list)
