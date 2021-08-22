import os
import first_model
import second_model
import webbrowser


def main():
    clear()
    if not os.path.isdir("data"):
        os.mkdir("data")
    print(mk_title(string="main menù", length=52))
    print("1. 1st Model")
    print("2. 2nd Model")
    print("3. Performance summary")
    print("4. Exit")
    print(52 * "-")
    try:
        done = False
        while not done:
            choice = handle_int(4)
            if choice == 1:
                clear()
                if os.path.isfile(f"result{os.sep}first_model.html"):
                    path = f"result{os.sep}first_model.html"
                else:
                    path = first_model.main()
                webbrowser.open_new(path)
                done = True
            elif choice == 2:
                clear()
                if os.path.isfile(f"result{os.sep}second_model.html"):
                    path = f"result{os.sep}second_model.html"
                else:
                    path = None
                webbrowser.open_new(path)
                done = True
            elif choice == 4:
                clear()
                second_model.main(distance_df="test.json", output_csv="shortest_path_time.csv")
                webbrowser.open_new_tab("https://github.com/MatteoFasulo/Algos/blob/b764d198c8dc9a45f74fee5eab9e220bb4c7ed80/algorithm.ipynb")
                done = True
            else:
                clear()
                print("###################################\n"
                      "# Exit command received, exiting! #\n"
                      "#        Bye, see you soon!       #\n"
                      "###################################")
                done = True
    except KeyboardInterrupt:
        raise KeyboardInterrupt


def mk_title(string: str, length: int):
    if (length - 2) < len(string):
        raise ValueError

    string = string.upper().strip()
    title = ' '
    for i in range(0, len(string)):
        title += string[i] + ' '

    f_length = length - len(title) - 2
    if f_length % 2 == 0:
        title = ((f_length // 2) * '-') + ' ' + title + ' ' + ((f_length // 2) * '-')
    else:
        title = str((f_length // 2) * '-') + ' ' + title + ' ' + (((f_length // 2) + 1) * '-')

    return str('\n' + title)


def handle_int(numberOfChoiches):
    done = False
    while not done:
        choice = input("Enter your choice [1-%d]: " % numberOfChoiches).strip()
        try:
            choice = int(choice)
            done = 1 <= choice <= numberOfChoiches
        except ValueError:
            pass
    return choice


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


if __name__ == "__main__":
    main()
