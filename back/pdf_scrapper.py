import PyPDF2


def integrate(pdf_path):
    pdf = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf)

    cleaned_content = []
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num).extractText()
        cleaned_content += clean(page)

    print(cleaned_content)
    cleaned_content = remove_junk_parts(cleaned_content)
    save_to_file(pdf_path, cleaned_content)


def clean(page):
    res = [line.strip() for line in page.split('\n') if len(line) > 3]
    total_line_size = sum([len(res[i]) for i in range(min(len(res), 10))])
    print(total_line_size)
    if total_line_size <= 10:
        page = special_case(page)
    return res


def special_case(page):
    print("\t\t\t SPECIAL !!!!!!!!!!!!!!!!!!!!")
    print(page.replace("\n", ""))
    return page


def remove_junk_parts(content):
    in_grid = False
    cleaned_content = []
    for line in content:
        if "RELEVÉ DES OPÉRATIONS" not in line and not in_grid:
            continue
        elif not in_grid:
            print("\tfound 1st tag")
            in_grid = True

        if "Les écritures précédées du signe" in line:
            print("\tfound 2nd tag")
            break
        cleaned_content += [line]
    return cleaned_content


def save_to_file(pdf_path, content):
    new_path = pdf_path.split("/")
    del new_path[-2]
    new_path = "/".join(new_path).replace(".pdf", ".txt")
    with open(new_path, 'w') as file:
        for c in content:
            file.write(c + "\n")


# --------------------------- Utils ---------------------------


def get_all_files_path(directory):
    import glob

    all_files_regex = "*"
    return glob.glob(directory + all_files_regex)


# --------------------------- Test ---------------------------


def test(directory):
    all_pdfs = get_all_files_path(directory)
    count = 0
    for pdf_path in sorted(all_pdfs):
        if ".pdf" not in pdf_path:
            continue

        count += 1

        if count not in [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]:
            continue

        integrate(pdf_path)
        print(count, pdf_path)

        if count > 21:
            break

if __name__ == "__main__":
    dir_path = "../data/releve_de_compte_sg/"

    test(dir_path)
