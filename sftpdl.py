import argparse
import paramiko
import os, sys
from stat import S_ISDIR, S_ISLNK, S_ISREG

parser = argparse.ArgumentParser(description="Interactive SFTP download")
parser.add_argument("--host", required=True,
                    help="HOSTNAME")
parser.add_argument("--user", required=True,
                    help="USERNAME")
parser.add_argument("--pw", required=False,
                    help="PASSWORD")
args = parser.parse_args()

if not args.pw:
    password = input('Password:')
else:
    password = args.pw

try:
    t = paramiko.Transport(( args.host ))
    t.connect(
        username = args.user,
        password = password,
    )
    sftp = paramiko.SFTPClient.from_transport(t)
except:
    print('Could not connect to remote server!')
    sys.exit(0)

select = -1
while not select == '0':
    path = '.'
    dirlist = sftp.listdir(path)
    attrlist = sftp.listdir_attr(path)

    types = dict()
    for i, file in enumerate(attrlist):
        if S_ISDIR(file.st_mode): types[i] = 'DIR'
        if S_ISLNK(file.st_mode): types[i] = 'LNK'
        if S_ISREG(file.st_mode): types[i] = 'REG'

    items = dict()
    types_item_id = dict()
    item_id = 0
    for i, el in enumerate(dirlist):
        if not el[0] == '.':
            item_id += 1
            
            items[item_id] = el
            types_item_id[item_id] = types[i]

            print(item_id,':' ,types[i], ':', el)

    select = input('Enter the file/folder, ".." to go one level up or 0 to quit: ')

    def progress(transferred, total):
        if transferred == total:
            print('100 % ...done!')
        sys.stdout.write("%d%%   \r" % (transferred / total * 100) )

    if select == '..':
        sftp.chdir(path='..')
    elif select.isdigit():
        if int(select):
            select = int(select)

            try: items[int(select)]
            except:
                print('An invalid item was selected!')
            else:
                if types_item_id[select] == 'DIR' or types_item_id[select] == 'LNK':
                    sftp.chdir(path='./' + items[int(select)])
                elif types_item_id[select] == 'REG':
                    print('Downloading ' + items[int(select)])
                    try:
                        sftp.get(remotepath='./' + items[int(select)], localpath = './' + items[int(select)], callback = progress)
                    except KeyboardInterrupt:
                        sftp.get_channel().shutdown(2)
                    except:
                        print('File could not be downloaded!')
