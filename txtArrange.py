# @Author  :  lijishi
# @Contact :  lijishi@emails.bjut.edu.cn
# @Software:  Pycharm
# @EditTime:  Jan 27,2020
# @describe:  Make the TXT suitable for JSON
# @LICENSE :  GNU GENERAL PUBLIC LICENSE Version 3

# References

#in_path = r'C:\文件\庆余年_temp_pdf2txt.txt';
#out_path = r'C:\文件\庆余年_temp_txtArrange.txt';

def Arrange(in_path, out_path):
    total_lines = 0
    for index, line in enumerate(open(in_path, 'r', encoding = 'utf-8')):
        total_lines += 1
    in_txt = open(in_path)
    string = ''
    line_num = 0

    while True:
        line = in_txt.readline()
        if line_num == total_lines:
            out_txt = open(out_path, 'a+')
            out_txt.read()
            out_txt.write(string)
            out_txt.close()
            break
        if line == '':
            break
        line_num += 1

        for index in range(len(line)):
            if line[index] == "\n":     #Judge whether it is the real end
                line_return = 0
                if len(line) == 1:
                    continue
                else:
                    if line[index-1] == '。' or line[index-1] == '！' or line[index-1] == '？' or line[index-1] == '……' or line[index-1] == '”' or line[index-1] == '}' or line[index-1] == '】' or line[index-1] == '）' or line[index-1] == '》' or line[index-1] == '；' :
                        line_return = 1
                    elif line[index-1] == '.' or line[index-1] == '!' or line[index-1] == '?' or line[index-1] == '......' or line[index-1] == '"' or line[index-1] == '}' or line[index-1] == ']' or line[index-1] == ')' or line[index-1] == '>' or line[index-1] == ';' :
                        line_return = 1

                if line_return == 1:
                    string += line[index]
                    out_txt = open(out_path, 'a+')
                    out_txt.read()
                    out_txt.write(string)
                    out_txt.close()
                    string = ''
                else:
                    continue
            else:
                string += str(line[index])
    in_txt.close()
    return
