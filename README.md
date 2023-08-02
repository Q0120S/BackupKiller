<h1 align="center">BackupKiller</h1>
<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#tool-options">Tool options</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>

BackupKiller is a tool to generate wordlist based on the URLs to check for backup, installation, etc files.

## Installation
```bash
git clone https://github.com/Q0120S/BackupKiller.git
cd BackupKiller
pip install -r requirements.txt
python3 fback.py -h
```
You can add this tool to your bashrc for ease of use:
```bash
fback() {                  
python3 /path/to/your/tool/fback.py "$@"
}
```

### Tool Options
* `-pattern` : You can define your pattern to get your desired output
* `-extensions` : Add extensions
* `-wordlistonly` : Use this option to generate a wordlist to use in feature fuzzing
* `-levels` : Choose the level you want to use in generation from the extensions.json 
* `-backup-levels` : Choose the backup level you want to use in generation from the extensions.json
* `-compress-levels` : Choose the compress level you want to use in generation from the extensions.json
* `-date-custom` : Define your own date format for generation, e.g. '$full_domain.%y-%m-%d.$ext' [separated by comma]
* `-date-default`: Choose this option to use the default date format in patterns.json 
```bash
python3 fback.py -h
```
This will display help for the tool. Here are all the switches it supports.
```console
usage: fback.py [-h] [-p PATTERN_FILE] [-e EXTENSIONS_FILE] [-o OUTPUT_FILE] [-wo] [-jo] [-l LEVELS] [-bl BACKUP_LEVELS]
                [-cl COMPRESS_LEVELS] [-w WORDLIST] [-dm] [-dc DATE_CUSTOM] [-dd] [-yr YEAR_RANGE] [-mr MONTH_RANGE]
                [-dr DAY_RANGE] [-nr NUMBER_RANGE] [-s]

Fback is a fast and dynamic tool to generate wordlist to find backup files.

options:
  -h, --help            show this help message and exit

Flags:
 INPUT:
  -p PATTERN_FILE, -pattern PATTERN_FILE
                        Pattern File Name (default "pattern.json")
  -e EXTENSIONS_FILE, -extensions EXTENSIONS_FILE
                        Input file containing list of extensions with levels (default "extensions.json")
  -o OUTPUT_FILE, -output OUTPUT_FILE
                        Name of the output file

 OUTPUT:
  -wo, -wordlistonly    Wordlist only
  -jo, -json-output     Wordlist only in JSON format

 LEVELS MANAGEMENT:
  -l LEVELS, -levels LEVELS
                        Backup & Compress extensions level(s) [min:1 max:10] (default "1,2")
  -bl BACKUP_LEVELS, -backup-levels BACKUP_LEVELS
                        Backup extensions level(s) [min:1 max:10]
  -cl COMPRESS_LEVELS, -compress-levels COMPRESS_LEVELS
                        Compress extensions level(s) [min:1 max:10]

 MAIN METHODS:
  -w WORDLIST, -wordlist WORDLIST
                        Wordlist method, to generate by words

 DATE METHODS:
  -dm, -date-method     Enable Date Method
  -dc DATE_CUSTOM, -date-custom DATE_CUSTOM
                        Custom Date format, e.g. '$full_domain.%y-%m-%d.$ext' [separated by comma]
  -dd, -date-default    Use default formats for date method in patterns.json
  -yr YEAR_RANGE, -year-range YEAR_RANGE
                        Range of years (default "2019-2022")
  -mr MONTH_RANGE, -month-range MONTH_RANGE
                        Range of months [min:1 max:12] (default "2,3")
  -dr DAY_RANGE, -day-range DAY_RANGE
                        Range of days [min:1 max:31] (default "1-3")

 OTHER OPTIONS:
  -nr NUMBER_RANGE, -number-range NUMBER_RANGE
                        Range of $num var in patterns (default "1,2")
  -s, -silent           Silent mode
```

## Usage
Simple usage:
```bash
cat sample_urls.txt | python3 fback.py -w wordlist.txt -s
```
Output:
```console
https://example.com/example.com.tar.xz
https://example.com/.example.bk
https://subs.example.com/fullbackup.bundle
https://example.com/passwords.txt.tar.bzip2.1
https://subs.example.com/files/.bak2
https://subs.example.com/logs.spg
https://example.com/search/.pack
https://subs.example.com/files/passwords.txt.save.1
https://subs.example.com/files/passwords.txt/install.tar.bzip2
https://example.com/passwords.txt.tig
https://example.com/path/.passwords.txt.swp.2
https://example.com/path/backup.gz2
[more]
...
```
Advance usage:
```bash
cat sample_urls.txt | python3 fback.py -s -p patterns.json -e extensions.json -w wordlist.txt -dm -yr 2020-2022 -mr 1-
4 -dr 10-20 -dd -bl 1 -cl 1
```
Output
```console
https://example.com/example.com.20210215.bkup
https://example.com/path/example.2022-04-19.old
https://subs.example.com/files/example.com.20200110.save
https://subs.example.com/files/example.com.20200117.back
https://example.com/example.com.20220116.sav
https://example.com/example.com.2022-03-18.save
https://subs.example.com/files/example.com.20220114.back
https://example.com/path/example.com.2022-04-19.~
https://subs.example.com/search/.swp
https://example.com/example.2021-01-11.bckp
https://example.com/path/subs.example.com.2021-03-12.backup1
https://subs.example.com/files/subs.example.com.20210112.swp
https://example.com/search/2021-01-18.backup
https://example.com/path/subs.example.com.20200312.bckp
https://subs.example.com/files/subs.example.com.2021-03-17.old
[more]
...
```

## License
This project is licensed under the MIT license. See the LICENSE file for details.
