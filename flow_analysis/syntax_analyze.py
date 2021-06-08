from os import listdir
from os.path import isfile, join
import re


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class CsmlFlow:
    def __init__(self, file_path, file_name):
        self.file_vars = []
        self.file_path = file_path
        self.file_name = re.sub('.csml', '', file_name)

    def look_for(self, finder):
        with open(self.file_path, 'r') as reader:
            line_number = 0
            for line in reader.readlines():
                line_number += 1
                finder(self, line, line_number)

    def create_step_context(self):
        with open(self.file_path, 'r') as reader:
            line_number = 0
            for line in reader.readlines():
                line_number += 1
                analysis = self.find_step(line, line_number)
                if analysis[1]:
                    line = line + '\ndo global_user_position = {"step": "' + analysis[1].group(
                        0).replace(':', '') + '", "flow": "' + self.file_name + '"}\n'
                    print(line)
                self.file_lines.append(line_adjustment)

    def change_flows(self, file_path):
        self.file_path = file_path
        self.open_file(self.replace_text)
        self.write_file()

        self.open_file(self.replace_var)
        self.write_file()

    def search_text(self, text):
        with open(self.file_path, 'r') as reader:
            line_number = 0
            for line in reader.readlines():
                line_number += 1
                self.find_text(line, line_number, text)

    def open_file(self, finder):
        self.file_lines = []
        with open(self.file_path, 'r') as reader:
            line_number = 0
            for line in reader.readlines():
                line_number += 1
                line_adjustment = finder(line, line_number)
                self.file_lines.append(line_adjustment)

    def write_file(self):
        file = open(self.file_path, "w")
        file.writelines(self.file_lines)
        file.close()

    def replace_var(self, line, line_number):
        line_sub = None
        for var in self.file_vars:
            var = var.strip()
            text = re.search(rf"(?<!stoodi.)(?<!\.)\b({var})\b", line)
            if text:
                line_sub = re.sub(
                    rf"(?<!stoodi.)(?<!\.)\b({var})\b", f"stoodi.{var}", line)

        if line_sub:
            print(
                f"{bcolors.HEADER}{line_number}:{bcolors.ENDC}{self.clean_line(line)}")
            print(
                f"{bcolors.OKGREEN}{line_number}:{bcolors.ENDC}{self.clean_line(line_sub)}")
            return line_sub

        return line

    def replace_text(self, line, line_number):
        text = re.search(
            'remember', line)
        var = re.search('(?<=remember)\s+(\w+)', line)
        if var:
            self.file_vars.append(var.group(0))
        if text:
            # print(
            #    f"{bcolors.HEADER}{line_number}:{bcolors.ENDC}{self.clean_line(line)}")
            line = re.sub('(remember\s+)', 'do stoodi.', line)
            # print(
            #    f"{bcolors.OKGREEN}{line_number}:{bcolors.ENDC}{self.clean_line(line)}")

        return line

    def find_text(self, line, line_number, text):
        var = re.search(rf"\b({text})\b", line)
        if var:
            print(
                f"{bcolors.HEADER}{line_number}:{bcolors.ENDC}{self.clean_line(var.group(0))}")

    def find_goto(self, line):
        goto = re.search('goto\sflow', line)
        if goto:
            line = re.sub('\t*', '', line)
            line = re.sub('\s*', '', line)
            print('\t' + line + '\n', end='')

    def find_step(self, line, line_number):
        step = re.search('^(?<!\")(\w*)\:', line)
        if step:
            print(
                f"{bcolors.HEADER}{line_number}:{bcolors.ENDC}{self.clean_line(line)}")
        return (line, step)

    def find_say(self, line, line_number):
        say = re.search('\s*(say)\s+', line)
        if say:
            print(
                f"{bcolors.HEADER}{line_number}:{bcolors.ENDC}{self.clean_line(line)}")

    def clean_line(self, line):
        line = re.sub('\t*', '', line)
        line = re.sub('', '', line)
        return line


path = './flows'
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]


def filter_cmds(file_name):
    if ".cmds.csml" not in file_name and "stoodi" in file_name:
        return True
    else:
        return False


only_code_files = filter(filter_cmds, onlyfiles)

for file in only_code_files:
    print(f"\n{bcolors.OKBLUE}{file}{bcolors.ENDC}\n")
    CsmlFlow(path + '/' + file, file).create_step_context()
