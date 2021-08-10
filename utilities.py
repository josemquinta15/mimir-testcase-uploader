from os import getcwd, mkdir, listdir, path
from typing import List


def printf(parts: List[str]=[1, 2, 3, 4, 5, 6], filename: str="", data: list = [], sep: str = ",", new_testcase: bool = False) -> str:
    """Print array into specified file

    Args:
        part (List[str], optional): assignment parts where to print. Defaults to all parts.
        filename (str, optional): name of generated file. Defaults to "input.txt".
        data (list, optional): data nested arrays to be printed into the file. Defaults to [].
        sep (str, optional): Separator for each line. Defaults to ",".
        new (bool, optional): Should a new folder be created?. Defaults to False.

    Returns:
        str: path for testcase's folder
    """
    cwd = getcwd()
    resource_folder = path.join(cwd, "files")
    testcase_folder_path = ""
    for part in parts:
        part_path = path.join(resource_folder, f"part_{part}")
        if not path.isdir(part_path):
            mkdir(part_path)
        testcase_number = len(listdir(part_path)) - int(not new_testcase) + 1
        testcase_folder_path = path.join(part_path, str(testcase_number))
        if new_testcase:
            mkdir(testcase_folder_path)
        if filename:
            full_file_path = path.join(testcase_folder_path, filename)
            with open(full_file_path, mode='w') as file:
                for elem in data:
                    if type(elem) in (str, int, float):
                        file.write(f"{elem}\n")
                    else:
                        file.write(f"{sep.join(map(str, elem))}\n")
    return testcase_folder_path



if __name__ == "__main__":
    pass