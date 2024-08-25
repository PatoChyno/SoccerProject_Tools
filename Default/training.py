import requests
from bs4 import BeautifulSoup

from player import Player

URL_BASE = "https://www.soccerproject.com/"
LOGIN_PATH = "login.php"
TRAINING_PATH = "spnewl_speler_training.php"
AJAX_PATH = "ajax_player.php"


def load_players(session, training_page):
    players = []
    player_rows = training_page.find_all("tr", attrs={"id": None})
    for player_row in player_rows:
        player_link = player_row.find(attrs={"class": "dummylink"})
        player_select = player_row.find("select")
        # player_selected_option = None
        # if player_select:
        #     player_selected_option = player_select.find("option", attrs={"selected": "selected"})
        player_selected_option = player_select.find("option", attrs={"selected": "selected"}) if player_select else None
        # player_links = training_page.find_all(attrs={"class": "dummylink"})[:-1]
        # for link in player_links:
        player_data = extract_player_data_from_link(player_link)
        player_id = player_data["id"]
        player_name = player_data["name"]
        player_detail = request_player_detail_rows(session, player_id)
        player = Player(player_detail_rows=player_detail, selected_option=player_selected_option, id=player_id,
                        name=player_name)
        players.append(player)
    return players


def training_payload(players):
    payload = {"step": 2}
    for player in players:
        property_to_train = None
        selected_property = player.selected_property()
        selected_property_is_maxed = False
        if selected_property:
            selected_property_is_maxed = selected_property["is_maxed"]
            if not selected_property_is_maxed:
                property_to_train = player.properties[selected_property["order"]]
        if not selected_property or selected_property_is_maxed:
            for i in range(len(player.properties)):
                property = player.properties[i + 1]
                if not property.is_maxed and property_to_train is None:
                    property_to_train = property
        stamina = player.properties[len(player.properties)]
        if stamina.value < 50 or property_to_train is None:
            property_to_train = stamina
        train_id = "train[" + player.id + "]"
        payload[train_id] = len(player.properties) - property_to_train.order + 1
    return payload


def submit_new_training(session, players):
    payload = training_payload(players)
    session.post(training_url(), data=payload)


def process_page(session, training_page):
    players = load_players(session, training_page)
    submit_new_training(session, players)


def run_app():
    session = requests.session()
    login(session)
    training_page = fetch_training_page(session)
    process_page(session, training_page)


def extract_player_data_from_link(link):
    link_text = link["onclick"]
    id_start = link_text.find("(")
    id_end = link_text.find(",")
    player_id = link_text[id_start + 1:id_end]
    player_name = link.text
    return {"id": player_id, "name": player_name}


def request_player_detail_rows(session, player_id):
    response = session.get(ajax_url(), params={"pID": player_id})
    return BeautifulSoup(response.content, "html.parser")("tr")


def fetch_training_page(session):
    response = session.get(training_url())
    return BeautifulSoup(response.content, "html.parser")


def login(session):
    payload = {
        "login": "PaToM",
        "password": "181113"
    }
    session.post(login_url(), data=payload)


def login_url():
    return URL_BASE + LOGIN_PATH


def training_url():
    return URL_BASE + TRAINING_PATH


def ajax_url():
    return URL_BASE + AJAX_PATH


if __name__ == "__main__":
    run_app()
