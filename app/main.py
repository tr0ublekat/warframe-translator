import requests


def get_rus_name(eng_text):
    """Get the Russian name of a Warframe item from its English name from the Warframe Market API."""

    eng_words_list = eng_text.split()
    url = "https://api.warframe.market/v2/item/"

    for i in range(len(eng_words_list)):
        word = eng_words_list[i]
        if i == 0:
            url += word
        else:
            url += "_" + word

    url += "/set"

    response = requests.get(
        url, headers={"language": "ru", "application/type": "json"}
    ).json()

    try:
        rus_name = response["data"]["items"][0]["i18n"]["ru"]["name"]
        return rus_name

    except Exception as e:
        if response["error"]["request"][0] == "app.item.notFound":
            return None
        else:
            raise e


def get_eng_name_from_query(eng_text):
    """Get the English name of a Warframe item from a search query from the Warframe Wiki API."""

    list_of_items = requests.get(
        f"https://wiki.warframe.com/rest.php/v1/search/title?q={'+'.join(eng_text.split())}&limit=10",
        headers={"application/type": "json"},
    ).json()

    if len(list_of_items["pages"]) == 0:
        print("error: no items found")
        return None

    print("choose one of the following items:")

    for i, item in enumerate(list_of_items["pages"]):
        print(f"{i}: " + item["title"])

    print("selected number: ", end="")
    selected_number = int(input())

    eng_name = list_of_items["pages"][selected_number]["title"].lower()

    return eng_name


if __name__ == "__main__":
    while True:
        # get name from user
        print("\ninput: ", end="")
        eng_text = input()

        # get rus name from eng text
        rus_name = get_rus_name(eng_text)

        # if rus name is not None, print it and continue
        if rus_name is not None:
            print("output: ", rus_name)
            continue

        # get eng name from query
        eng_name = get_eng_name_from_query(eng_text)

        # if eng name is None, continue
        if eng_name is None:
            continue

        # else get rus name from eng name
        rus_name = get_rus_name(eng_name)
        print("output: ", rus_name)
