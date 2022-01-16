import sys

def create_test(input_text, name_file):
    node = 0
    with open("tests/" + name_file, "w") as f:
        next_idx = 0
        for idx, char in enumerate(input_text):
            if idx != next_idx: continue
            if not char.isalpha() or input_text[idx:idx+3] not in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
                f.write(str(node) + " " + str(node+1) + " " + char + " " + char + "\n")
                next_idx += 1
            else:
                f.write(str(node) + " " + str(node+1) + " " + input_text[idx:idx+3] + " " + input_text[idx:idx+3] + "\n")
                next_idx += 3
            node+=1
        f.write(str(node))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Wrong usage!\npython create_test.py <test string> <file.txt>")

    if ".txt" not in sys.argv[2]:
        raise Exception("The output file should contain the extension .txt")

    create_test(sys.argv[1], sys.argv[2])