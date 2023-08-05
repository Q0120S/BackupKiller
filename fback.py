import json
import argparse
import os
import sys
from urllib.parse import urlparse, urlunparse, urljoin
import tldextract
import itertools

BANNER ='''                

     ____             _                _  _ _ _ _           
    | __ )  __ _  ___| | ___   _ _ __ | |/ (_) | | ___ _ __ 
    |  _ \ / _` |/ __| |/ / | | | '_ \| ' /| | | |/ _ \ '__|
    | |_) | (_| | (__|   <| |_| | |_) | . \| | | |  __/ |   
    |____/ \__,_|\___|_|\_\__,__| .__/|_|\_\_|_|_|\___|_|   
                                |_|   
                                                            NoobHunter
'''

script_dir = os.path.dirname(os.path.abspath(__file__))
patterns_path = os.path.join(script_dir, "patterns.json")
extensions_path = os.path.join(script_dir, "extensions.json")

def extract_url_parts(url):
    parsed_url = urlparse(url)
    full_domain = parsed_url.netloc
    subdomain = tldextract.extract(url).subdomain
    domain_name = tldextract.extract(url).domain
    tld = tldextract.extract(url).suffix
    path = parsed_url.path
    full_path = urlunparse(('', '', parsed_url.path, '', '', ''))
    file_name = path.split('/')[-1] if '.' in parsed_url.path.split('/')[-1] else ""

    return {
        "URL": url,
        "Full Domain": full_domain,
        "Subdomain": subdomain,
        "Domain Name": domain_name,
        "TLD": tld,
        "Path": path,
        "Full Path": full_path,
        "File Name": file_name,
    }

def format_patterns(url, patterns):
    url_parts = extract_url_parts(url)
    formatted_patterns = []
    for pattern in patterns:
        formatted_pattern = pattern.replace("$domain_name", str(url_parts["Domain Name"]))
        formatted_pattern = formatted_pattern.replace("$full_domain", str(url_parts["Full Domain"]))
        formatted_pattern = formatted_pattern.replace("$subdomain", str(url_parts["Subdomain"]))
        formatted_pattern = formatted_pattern.replace("$tld", str(url_parts["TLD"]))
        formatted_pattern = formatted_pattern.replace("$file_name", str(url_parts["File Name"]))
        formatted_pattern = formatted_pattern.replace("$full_path", str(url_parts["Full Path"]))
        formatted_pattern = formatted_pattern.replace("$path", str(url_parts["Path"]))

        formatted_pattern = formatted_pattern.replace("..", ".").replace("//", "/")
        formatted_patterns.append(formatted_pattern)
    return formatted_patterns

def generate_patterns_combinations(url, patterns, words, extensions, numbers):
    for u, p, w, e, n in itertools.product([url], patterns, words, extensions, numbers):
        new_pattern = p.replace("$word", w).replace("$ext", e).replace("$num", n).replace("$url", u)
        if not contains_special_chars(new_pattern):
            yield new_pattern

def contains_special_chars(line):
    return "$" in line or "%" in line

def remove_components_until_path(urls):
    nice_urls = []
    for url in urls:
        url = urljoin(url, urlparse(url).path)
        nice_urls.append(url)
    return list(set(nice_urls))  # Use set to remove duplicates and convert back to list

def generate_date_formats_combinations(url, date_formats, words, extensions, numbers, years, months, days):
    for u, dt, w, e, n, y, m, d in itertools.product([url], date_formats, words, extensions, numbers, years, months, days):
        new_date_format = dt.replace("$word", w).replace("$ext", e).replace("$num", n).replace("$url", u).replace("%y", y).replace("%m", m).replace("%d", d)
        if not contains_special_chars(new_date_format):
            yield new_date_format

def create_year_range(year_range):
    if '-' in year_range:
        start_year, end_year = map(int, year_range.split('-'))
        if len(str(start_year)) == 4 and len(str(end_year)) == 4:
            return [str(year) for year in range(start_year, end_year + 1)]
        else:
            raise ValueError("Invalid input format. Use 'YYYY-YYYY' or 'YYYY,YYYY'.")
    elif ',' in year_range:
        year_range = year_range.split(',')
        for year in year_range:
            if len(str(year)) != 4:
                raise ValueError("Invalid input format. Use 'YYYY-YYYY' or 'YYYY,YYYY'.")
        return [str(year) for year in year_range]
    elif year_range.isdigit() == True and len(year_range) == 4:
        return [year_range]
    else:
        raise ValueError("Invalid input format. Use 'YYYY-YYYY' or 'YYYY,YYYY'.")

def create_month_range(month_range):
    if '-' in month_range:
        start_month, end_month = map(int, month_range.split('-'))
        if 1 <= start_month <= 12 and 1 <= end_month <= 12:
            return [f"{month:02d}" for month in range(start_month, end_month + 1)]
        else:
            raise ValueError("Invalid input format. Use 'mm-mm' or 'mm,mm'.")
    elif ',' in month_range:
        month_range = month_range.split(',')
        for month in month_range:
            if 1 < int(month) > 12:
                raise ValueError("Invalid input format. Use 'mm-mm' or 'mm,mm'.")
        return [f"{int(month):02d}" for month in month_range]
    elif month_range.isdigit() == True and 1 <= int(month_range) <= 12:
        return [f"{int(month_range):02d}"]
    else:
        raise ValueError("Invalid input format. Use 'mm-mm' or 'mm,mm'.")

def create_day_range(day_range):
    if '-' in day_range:
        start_day, end_day = map(int, day_range.split('-'))
        if 1 <= int(start_day) <= 31 and 1 <= int(end_day) <= 31:
            return [f"{day:02d}" for day in range(start_day, end_day + 1)]
        else:
            raise ValueError("Invalid input format. Use 'dd-dd' or 'dd,dd'.")
    elif ',' in day_range:
        day_range = day_range.split(',')
        for day in day_range:
            if 1 < int(day) > 31:
                raise ValueError("Invalid input format. Use 'dd-dd' or 'dd,dd'.")
        return [f"{int(day):02d}" for day in day_range]
    elif day_range.isdigit() == True and 1 <= int(day_range) <= 31:
        return [f"{int(day_range):02d}"]
    else:
        raise ValueError("Invalid input format. Use 'dd-dd' or 'dd,dd'.")

def main():
    parser = argparse.ArgumentParser(description="Fback is a fast and dynamic tool to generate wordlist to find backup files.",
                                     formatter_class=argparse.RawTextHelpFormatter)

    # Input options
    INPUT = parser.add_argument_group('Flags:\n INPUT')
    INPUT.add_argument('-p', '-pattern', dest='pattern_file', default=patterns_path, help='Pattern File Name (default "patterns.json")')
    INPUT.add_argument('-e', '-extensions', dest='extensions_file', default=extensions_path, help='Input file containing list of extensions with levels (default "extensions.json")')
    INPUT.add_argument('-o', '-output', dest='output_file', default=None, help='Name of the output file')
    
    # Output options
    OUTPUT = parser.add_argument_group(' OUTPUT')
    OUTPUT.add_argument('-wo', '-wordlistonly', action='store_true', dest='wordlist_only', help='Wordlist only')
    OUTPUT.add_argument('-jo', '-json-output', action='store_true', dest='json_output', help='Wordlist only in JSON format')
    
    # Levels Management
    LEVELS = parser.add_argument_group(' LEVELS MANAGEMENT')
    LEVELS.add_argument('-l', '-levels', dest='levels', default='1,2' ,help='Backup & Compress extensions level(s) [min:1 max:10] (default "1,2")')
    LEVELS.add_argument('-bl', '-backup-levels', dest='backup_levels', default=None, help='Backup extensions level(s) [min:1 max:10]')
    LEVELS.add_argument('-cl', '-compress-levels', dest='compress_levels', default=None, help='Compress extensions level(s) [min:1 max:10]')
    
    # Main methods
    MAIN_METHODS = parser.add_argument_group(' MAIN METHODS')
    MAIN_METHODS.add_argument('-w', '-wordlist', dest='wordlist', default=None, help='Wordlist method, to generate by words')
    
    # Date methods
    DATE_METHODS = parser.add_argument_group(' DATE METHODS')
    DATE_METHODS.add_argument('-dm', '-date-method', action='store_true', dest='date_method', help='Enable Date Method')
    DATE_METHODS.add_argument('-dc', '-date-custom', dest='date_custom', default=None, help='Custom Date format, e.g. \'$full_domain.%%y-%%m-%%d.$ext\' [separated by comma]')
    DATE_METHODS.add_argument('-dd', '-date-default', action='store_true', dest='date_default', help='Use default formats for date method in patterns.json')
    DATE_METHODS.add_argument('-yr', '-year-range', dest='year_range', default='2019-2022', help='Range of years (default "2019-2022")')
    DATE_METHODS.add_argument('-mr', '-month-range', dest='month_range', default='2,3', help='Range of months [min:1 max:12] (default "2,3")')
    DATE_METHODS.add_argument('-dr', '-day-range', dest='day_range', default='1-3', help='Range of days [min:1 max:31] (default "1-3")')
    
    # Other options
    OTHER = parser.add_argument_group(' OTHER OPTIONS')
    OTHER.add_argument('-nr', '-number-range', dest='number_range', default='1,2', help='Range of $num var in patterns (default "1,2")')
    OTHER.add_argument('-s', '-silent', action='store_true', dest='silent', help='Silent mode')
    
    args = parser.parse_args()
    
    try:
        if not args.output_file and not args.silent:
            print(BANNER)

        if not sys.stdin.isatty():
            input_urls = [line.strip() for line in sys.stdin.readlines()]
            url_list = remove_components_until_path(input_urls)
            
        if args.pattern_file:
            with open(args.pattern_file, 'r') as file:
                pattern_file = json.load(file)
        else:
            print("Provide a patterns file")
            sys.exit(1)

        if args.extensions_file:
            with open(args.extensions_file, 'r') as file:
                extensions_file = json.load(file)
        else:
            print("Provide a extensions file")
            sys.exit(1)

        if args.wordlist:
            with open(args.wordlist, 'r') as file:
                words = [line.strip() for line in file]
        else:
            print("Provide a wordlist")
            sys.exit(1)

        if args.backup_levels:
            extensions = []
            backup_levels = args.backup_levels.split(',')
            for level in backup_levels:
                if level in extensions_file.get("backup_levels", {}):
                    extensions.extend(extensions_file["backup_levels"][level])
                else:
                    raise ValueError("Invalid backup level")
        elif args.compress_levels:
            extensions = []
            levels = args.compress_levels.split(',')
            for level in levels:
                if level in extensions_file.get("compress_levels", {}):
                    extensions.extend(extensions_file["compress_levels"][level])
                else:
                    raise ValueError("Invalid compress level")
        else:
            extensions = []
            levels = args.levels.split(',')
            for level in levels:
                if level in extensions_file.get("level", {}):
                    extensions.extend(extensions_file["level"][level])
                else:
                    raise ValueError("Invalid level")

        # Date methods
        if args.date_method:
            if args.year_range:
                year_range = create_year_range(args.year_range)

            if args.month_range:
                month_range = create_month_range(args.month_range)

            if args.day_range:
                day_range = create_day_range(args.day_range)

        if args.number_range:
            if '-' in args.number_range:
                start_num, end_num = map(int, args.number_range.split('-'))
                number_range = [str(num) for num in range(start_num, end_num + 1)]
            else:
                number_range = args.number_range.split(',')

        final = {"patterns": set()}
        for u in url_list:
            formatted_patterns = format_patterns(u, pattern_file.get("patterns", []))
            final["patterns"].update(generate_patterns_combinations(u, formatted_patterns, words, extensions, number_range))

        if args.date_method:
            final["date-formats"] = set() 
            for u, w, e, n, y, m, d in itertools.product(url_list, words, extensions, number_range, year_range, month_range, day_range):
                out_pattern = {"date-formats": set()}  # Use a set to store unique date formats
                if args.date_default:
                    out_pattern["date-formats"].update(generate_date_formats_combinations(u, format_patterns(u, pattern_file.get("date-formats", [])), [w], [e], [n], [y], [m], [d]))
                elif args.date_custom:
                    date_custom = args.date_custom.split(",")
                    pattern_file["date-formats"] = []
                    for i in date_custom:
                        pattern_file["date-formats"].extend([i])
                        out_pattern["date-formats"].update(generate_date_formats_combinations(u, format_patterns(u, pattern_file.get("date-formats", [])), [w], [e], [n], [y], [m], [d]))
                final["date-formats"].update(out_pattern["date-formats"])
            # Convert sets back to lists before printing
            final["date-formats"] = list(final["date-formats"])
        # Convert sets back to lists before printing
        final["patterns"] = list(final["patterns"])
        unique_output = set()

        if args.json_output:
            unique_output = final
            if args.output_file:
                with open(args.output_file, 'w') as outfile:
                    outfile.write(json.dumps(unique_output, indent=4))
            else:
                print(json.dumps(unique_output, indent=4))
        elif args.wordlist_only:
            for url in url_list:
                for path in final["patterns"]:
                    unique_output.add(path)
                if args.date_method:
                    for path in final["date-formats"]:
                        unique_output.add(path)
            if args.output_file:
                with open(args.output_file, 'w') as outfile:
                    for url in unique_output:
                        if url[0] == '/':
                            url = url[1:]
                        outfile.write(url + '\n')
            else:
                for url in unique_output:
                    if url[0] == '/':
                        url = url[1:]
                    print(url)
        else:
            for url in url_list:
                for path in final["patterns"]:
                    unique_output.add(urljoin(url, path))
                if args.date_method:
                    for path in final["date-formats"]:
                        unique_output.add(urljoin(url, path))
            if args.output_file:
                with open(args.output_file, 'w') as outfile:
                    for url in unique_output:
                        outfile.write(url + '\n')
            else:
                for url in unique_output:
                    print(url)
    except Exception as e:
        print(e)

if __name__ == "__main__":  
    main()
