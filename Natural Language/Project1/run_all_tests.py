import PyPDF2, os, time, sys
from create_test import create_test

def run(fc=None):
    with open("tests.md", "r") as fp:
        if fc == None:
            tests = [x.strip().split(" ") for x in fp.readlines()[2:]]
        else:
            tests = [x.strip().split(" ") for x in fp.readlines()[2:] if fc in x]

    print(f"{len(tests)} test(s) imported!\n")

    time.sleep(1)

    wrong_tests = []

    for idx, test in enumerate(tests):
        if idx%1 == 0: print(f"Running test {idx}")
        input_text = test[1]
        transducer = test[3]
        expected = test[5]

        filebase = f"{transducer}-{input_text.replace('/', 'bar')}"
        create_test(input_text, f"{filebase}.txt")

        os.system(f"fstcompile --isymbols=syms.txt -osymbols=syms.txt tests/{filebase}.txt | fstarcsort > compiled/{filebase}.fst")
        os.system(f"fstcompose compiled/{filebase}.fst compiled/{transducer}.fst > res.fst")
        os.system(f"fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt res.fst | dot -Tpdf > res.pdf")

        pdf = open("res.pdf", "rb")
        page_text = PyPDF2.PdfFileReader(pdf).getPage(0).extractText()

        lines = page_text.split("\n")
        res = ""
        for line in lines:
            if ":" in line:
                res += line.split(":")[1]
        res = res.replace("eps", "")

        if res != expected:
            wrong_tests.append([input_text, transducer, expected, res])

        os.system(f"rm compiled/{filebase}.fst")
    os.system(f"rm res.pdf")
    os.system(f"rm res.fst")

    print(f"We are passing {len(tests) - len(wrong_tests)}/{len(tests)} tests!")
    if len(wrong_tests) > 0:
        print()
        print("--- WRONG TESTS ---")
        for wt in wrong_tests:
            print(f"Test '{wt[0]}' with transducer {wt[1]}.fst wrong! Exp: '{wt[2]}' vs Obt: '{wt[3]}'")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run()