import json
import logging
from copy import deepcopy
from typing import Type

import psycopg2
import pytest
from koodistot_loader.koodistot_loader import DatabaseHelper, KoodistotLoader, codes

lifecycle_status_response = {
    "meta": {"code": 200, "from": 0, "resultCount": 2, "totalResults": 2},
    "results": [
        {
            "id": "18d6ba57-ac81-4e51-9efe-f5edaa60d1cd",
            "codeValue": "01",
            "uri": "http://uri.suomi.fi/codelist/rytj/kaavaelinkaari/code/01",
            "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/kaavaelinkaari/codes/01",
            "status": "DRAFT",
            "order": 1,
            "hierarchyLevel": 1,
            "created": "2023-03-28T13:48:49.500Z",
            "modified": "2023-11-29T14:12:44.614Z",
            "statusModified": "2023-03-28T13:48:49.500Z",
            "prefLabel": {
                "en": "Planning initiative",
                "fi": "Kaavoitusaloite",
                "sv": "Planläggningsinitiativ",
            },
            "description": {
                "en": "A planning initiative newly pending in a municipality or region.",
                "fi": "Kuntaan tai maakuntaan saapunut kaavoitusaloite.",
                "sv": "Ett initiativ om planläggning som inkommit till kommunen eller landskapet.",
            },
            "codeScheme": {
                "uri": "http://uri.suomi.fi/codelist/rytj/kaavaelinkaari",
                "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/kaavaelinkaari",
            },
            "membersUrl": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/kaavaelinkaari/codes/01/members/",
        },
        {
            "id": "6fd4835d-f58f-425e-a262-c5d1af83c229",
            "codeValue": "13",
            "uri": "http://uri.suomi.fi/codelist/rytj/kaavaelinkaari/code/13",
            "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/kaavaelinkaari/codes/13",
            "status": "DRAFT",
            "order": 13,
            "hierarchyLevel": 1,
            "created": "2023-03-28T13:48:49.583Z",
            "modified": "2023-11-29T14:12:44.742Z",
            "statusModified": "2023-03-28T13:48:49.583Z",
            "prefLabel": {"en": "Valid", "fi": "Voimassa", "sv": "Giltig"},
            "description": {
                "en": "The plan has been announced as valid.",
                "fi": "Kaava on kuulutettu voimaan.",
                "sv": "Planen har börjat gälla genom kungörelse.",
            },
            "codeScheme": {
                "uri": "http://uri.suomi.fi/codelist/rytj/kaavaelinkaari",
                "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/kaavaelinkaari",
            },
            "membersUrl": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/kaavaelinkaari/codes/13/members/",
        },
    ],
}

additional_lifecycle_status = {
    "id": "476c165b-373d-46fb-b81d-e1d8fbd198bd",
    "codeValue": "02",
    "uri": "http://uri.suomi.fi/codelist/rytj/kaavaelinkaari/code/02",
    "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/kaavaelinkaari/codes/02",
    "status": "DRAFT",
    "order": 2,
    "hierarchyLevel": 1,
    "created": "2023-03-28T13:48:49.519Z",
    "modified": "2023-11-29T14:12:44.634Z",
    "statusModified": "2023-03-28T13:48:49.519Z",
    "prefLabel": {"en": "Pending", "fi": "Vireilletullut", "sv": "Blivit anhängigt"},
    "description": {
        "en": "The plan has become pending through public notice or its status as pending has been announced in connection with a planning review.",
        "fi": "Kaava on kuulutettu vireille tai vireille tulosta on ilmoitettu kaavoituskatsauksen yhteydessä.",
        "sv": "Planen har kungjorts anhängig eller anhängiggörandet har meddelats i samband med planläggningsöversikten.",
    },
    "codeScheme": {
        "uri": "http://uri.suomi.fi/codelist/rytj/kaavaelinkaari",
        "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/kaavaelinkaari",
    },
    "membersUrl": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/kaavaelinkaari/codes/02/members/",
}

changed_lifecycle_status_response = deepcopy(lifecycle_status_response)
changed_lifecycle_status_response["results"].append(  # type:ignore
    additional_lifecycle_status
)
changed_lifecycle_status_response["meta"]["resultCount"] += 1  # type:ignore
changed_lifecycle_status_response["meta"]["totalResults"] += 1  # type:ignore

type_of_plan_regulation_response = {
    "meta": {"code": 200, "from": 0, "resultCount": 4, "totalResults": 4},
    "results": [
        {
            "id": "15934bd8-419b-420b-9b1d-b12608bdf27a",
            "codeValue": "asumisenAlue",
            "uri": "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji/code/asumisenAlue",
            "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/asumisenAlue",
            "status": "DRAFT",
            "order": 298,
            "hierarchyLevel": 1,
            "created": "2023-04-12T07:41:52.721Z",
            "modified": "2023-12-18T10:16:39.309Z",
            "statusModified": "2023-04-12T07:41:52.721Z",
            "prefLabel": {
                "en": "Housing area",
                "fi": "Asumisen alue",
                "sv": "Område för boende",
            },
            "description": {
                "fi": "Ilmaisee, että kaavakohde kuvaa asumisen rakennuksille tai asunnoille tarkoitetun alueen. Käytetään asemakaavoissa ilmaisemaan asuinrakennusten alueita, joille voidaan rakentaa eri tyyppisiä asuinrakennuksia. Maakunta- ja yleiskaavoissa käytetään ilmaisemaan asuntoalueita, jolla kerrosalasta pääosa on tarkoitettu asumiseen. Koodi liittyy lähtökohtaisesti kaavakohteeseen, joka on geometrialtaan alue."
            },
            "codeScheme": {
                "uri": "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji",
                "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji",
            },
            "shortName": "A",
            "membersUrl": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/asumisenAlue/members/",
        },
        {
            "id": "e6f03e18-f292-4068-b6a6-b9e52206accc",
            "codeValue": "asuinpientaloalue",
            "uri": "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji/code/asuinpientaloalue",
            "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/asuinpientaloalue",
            "status": "DRAFT",
            "order": 299,
            "hierarchyLevel": 2,
            "created": "2023-04-12T07:41:52.734Z",
            "modified": "2023-12-18T10:16:39.342Z",
            "statusModified": "2023-04-12T07:41:52.734Z",
            "prefLabel": {
                "en": "Area of residential houses",
                "fi": "Asuinpientaloalue",
                "sv": "Område för småhus",
            },
            "description": {
                "fi": "Ilmaisee, että kaavakohde kuvaa asuinpientaloille tarkoitetun alueen. Käytetään asemakaavoissa ilmaisemaan, että alueelle voidaan erilaisia pientaloja eli rivitaloja, kytkettyjä pientaloja ja erillisiä pientaloja asumistarkoituksiin. Käytetään yleiskaavoissa ilmaisemaan pientalovaltaista asuntoaluetta. Koodi liittyy lähtökohtaisesti kaavakohteeseen, joka on geometrialtaan alue."
            },
            "codeScheme": {
                "uri": "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji",
                "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji",
            },
            "shortName": "AP",
            "broaderCode": {
                "id": "15934bd8-419b-420b-9b1d-b12608bdf27a",
                "codeValue": "asumisenAlue",
                "uri": "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji/code/asumisenAlue",
                "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/asumisenAlue",
                "status": "DRAFT",
                "order": 298,
                "hierarchyLevel": 1,
                "created": "2023-04-12T07:41:52.721Z",
                "modified": "2023-12-18T10:16:39.309Z",
                "statusModified": "2023-04-12T07:41:52.721Z",
                "prefLabel": {
                    "en": "Housing area",
                    "fi": "Asumisen alue",
                    "sv": "Område för boende",
                },
                "description": {
                    "fi": "Ilmaisee, että kaavakohde kuvaa asumisen rakennuksille tai asunnoille tarkoitetun alueen. Käytetään asemakaavoissa ilmaisemaan asuinrakennusten alueita, joille voidaan rakentaa eri tyyppisiä asuinrakennuksia. Maakunta- ja yleiskaavoissa käytetään ilmaisemaan asuntoalueita, jolla kerrosalasta pääosa on tarkoitettu asumiseen. Koodi liittyy lähtökohtaisesti kaavakohteeseen, joka on geometrialtaan alue."
                },
                "shortName": "A",
                "membersUrl": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/asumisenAlue/members/",
            },
            "membersUrl": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/asuinpientaloalue/members/",
        },
        {
            "id": "ba9a86d5-6944-4bc4-a86c-87a78c0cdc2a",
            "codeValue": "erillistenAsuinpientalojenAlue",
            "uri": "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji/code/erillistenAsuinpientalojenAlue",
            "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/erillistenAsuinpientalojenAlue",
            "status": "DRAFT",
            "order": 300,
            "hierarchyLevel": 3,
            "created": "2023-04-12T07:41:52.740Z",
            "modified": "2023-12-18T10:16:39.357Z",
            "statusModified": "2023-04-12T07:41:52.740Z",
            "prefLabel": {
                "en": "Area of detached houses",
                "fi": "Erillisten asuinpientalojen alue",
                "sv": "Område för fristående småhus",
            },
            "description": {
                "fi": "Ilmaisee, että kaavakohde kuvaa erillisille asuinpientaloille tarkoitetun alueen eli alueen, jolle on ja/tai sille voidaan rakentaa yksi- tai kaksiasuntoisia pientaloja (omakotitaloja Rakennusluokituksen 2018 mukainen koodiarvo 0110 tai paritaloja Rakennusluokituksen 2018 mukainen koodiarvo 0111) asumistarkoituksiin. Mikäli halutaan, että kullekin rakennuspaikalle saa rakentaa vain yhden asuinrakennuksen, tulee kaavakohteeseen liittää sanallinen määräys asiasta. Kaavamääräyslaji ei ota kantaa asuntojen omistusmuotoon eli siihen onko kyseessä yhtiömuotoinen erillistalo. Koodi liittyy lähtökohtaisesti kaavakohteeseen, joka on geometrialtaan alue."
            },
            "codeScheme": {
                "uri": "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji",
                "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji",
            },
            "shortName": "AO",
            "broaderCode": {
                "id": "e6f03e18-f292-4068-b6a6-b9e52206accc",
                "codeValue": "asuinpientaloalue",
                "uri": "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji/code/asuinpientaloalue",
                "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/asuinpientaloalue",
                "status": "DRAFT",
                "order": 299,
                "hierarchyLevel": 2,
                "created": "2023-04-12T07:41:52.734Z",
                "modified": "2023-12-18T10:16:39.342Z",
                "statusModified": "2023-04-12T07:41:52.734Z",
                "prefLabel": {
                    "en": "Area of residential houses",
                    "fi": "Asuinpientaloalue",
                    "sv": "Område för småhus",
                },
                "description": {
                    "fi": "Ilmaisee, että kaavakohde kuvaa asuinpientaloille tarkoitetun alueen. Käytetään asemakaavoissa ilmaisemaan, että alueelle voidaan erilaisia pientaloja eli rivitaloja, kytkettyjä pientaloja ja erillisiä pientaloja asumistarkoituksiin. Käytetään yleiskaavoissa ilmaisemaan pientalovaltaista asuntoaluetta. Koodi liittyy lähtökohtaisesti kaavakohteeseen, joka on geometrialtaan alue."
                },
                "shortName": "AP",
                "membersUrl": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/asuinpientaloalue/members/",
            },
            "membersUrl": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/erillistenAsuinpientalojenAlue/members/",
        },
        {
            "id": "8ced8dae-5a62-410a-ad49-890f623a16bf",
            "codeValue": "rivitalojenJaMuidenKytkettyjenAsuinpientalojenAlue",
            "uri": "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji/code/rivitalojenJaMuidenKytkettyjenAsuinpientalojenAlue",
            "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/rivitalojenJaMuidenKytkettyjenAsuinpientalojenAlue",
            "status": "DRAFT",
            "order": 301,
            "hierarchyLevel": 3,
            "created": "2023-04-12T07:41:52.747Z",
            "modified": "2023-12-18T10:16:39.371Z",
            "statusModified": "2023-04-12T07:41:52.747Z",
            "prefLabel": {
                "en": "Area of semi-detached and terraced houses",
                "fi": "Rivitalojen ja muiden kytkettyjen asuinpientalojen alue",
                "sv": "Område för radhus och andra kopplade bostadshus",
            },
            "description": {
                "fi": "Ilmaisee, että kaavakohde kuvaa rivitaloille ja muille kytketyille asuinpientaloille tarkoitetun alueen. Kattaa rivitalot (Rakennusluokituksen 2018 mukainen koodiarvo  0112), joita ovat pientalot, joissa on vähintään kolme rinnakkaista asuinhuoneistoa ja joissa eri asuinhuoneistoihin kuuluvia tiloja ei ole päällekkäin. Rivitalot koostuvat kolmesta tai useammasta yhteen rakennetusta asuinhuoneistosta ja muusta asukkaiden käytössä olevasta huonetilasta. Muita kytkettyjä asuinpientaloja ovat esimerkiksi autokatoksin tai varastoin toisiinsa kytketyt asuinpientalot. Koodi liittyy lähtökohtaisesti kaavakohteeseen, joka on geometrialtaan alue."
            },
            "codeScheme": {
                "uri": "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji",
                "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji",
            },
            "shortName": "AR",
            "broaderCode": {
                "id": "e6f03e18-f292-4068-b6a6-b9e52206accc",
                "codeValue": "asuinpientaloalue",
                "uri": "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji/code/asuinpientaloalue",
                "url": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/asuinpientaloalue",
                "status": "DRAFT",
                "order": 299,
                "hierarchyLevel": 2,
                "created": "2023-04-12T07:41:52.734Z",
                "modified": "2023-12-18T10:16:39.342Z",
                "statusModified": "2023-04-12T07:41:52.734Z",
                "prefLabel": {
                    "en": "Area of residential houses",
                    "fi": "Asuinpientaloalue",
                    "sv": "Område för småhus",
                },
                "description": {
                    "fi": "Ilmaisee, että kaavakohde kuvaa asuinpientaloille tarkoitetun alueen. Käytetään asemakaavoissa ilmaisemaan, että alueelle voidaan erilaisia pientaloja eli rivitaloja, kytkettyjä pientaloja ja erillisiä pientaloja asumistarkoituksiin. Käytetään yleiskaavoissa ilmaisemaan pientalovaltaista asuntoaluetta. Koodi liittyy lähtökohtaisesti kaavakohteeseen, joka on geometrialtaan alue."
                },
                "shortName": "AP",
                "membersUrl": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/asuinpientaloalue/members/",
            },
            "membersUrl": "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries/rytj/codeschemes/RY_Kaavamaarayslaji/codes/rivitalojenJaMuidenKytkettyjenAsuinpientalojenAlue/members/",
        },
    ],
}


def get_url(cls: Type[codes.CodeBase]) -> str:
    return f"http://mock.url/{cls.code_list_uri.rsplit('/', 1)[-1]}/codes"


@pytest.fixture()
def mock_koodistot(requests_mock) -> None:
    requests_mock.get(
        get_url(codes.LifeCycleStatus), text=json.dumps(lifecycle_status_response)
    )
    requests_mock.get(
        get_url(codes.TypeOfPlanRegulation),
        text=json.dumps(type_of_plan_regulation_response),
    )
    requests_mock.get(get_url(codes.PlanType), text="")
    requests_mock.get(
        get_url(codes.TypeOfAdditionalInformationForPlanRegulation), text=""
    )
    requests_mock.get(get_url(codes.TypeOfVerbalPlanRegulation), text="")
    requests_mock.get(get_url(codes.TypeOfSourceData), text="")
    requests_mock.get(get_url(codes.TypeOfUnderground), text="")


@pytest.fixture()
def changed_mock_koodistot(requests_mock, mock_koodistot) -> None:
    # override one response
    requests_mock.get(
        get_url(codes.LifeCycleStatus),
        text=json.dumps(changed_lifecycle_status_response),
    )


@pytest.fixture(scope="module")
def connection_string(hame_database_created) -> str:
    return DatabaseHelper().get_connection_string()


@pytest.fixture(scope="module")
def loader(connection_string) -> KoodistotLoader:
    return KoodistotLoader(
        connection_string,
        api_url="http://mock.url",
    )


@pytest.fixture()
def koodistot_data(mock_koodistot, loader):
    data = loader.get_objects()
    assert len(data) == 7
    # data should contain the mock data and be empty for other tables
    assert len(data[codes.LifeCycleStatus]) == 2
    assert len(data[codes.TypeOfPlanRegulation]) == 4
    assert len(data[codes.PlanType]) == 0
    return data


@pytest.fixture()
def changed_koodistot_data(changed_mock_koodistot, loader):
    data = loader.get_objects()
    assert len(data) == 7
    # data should contain the mock data and be empty for other tables
    assert len(data[codes.LifeCycleStatus]) == 3
    assert len(data[codes.TypeOfPlanRegulation]) == 4
    assert len(data[codes.PlanType]) == 0
    return data


def test_get_aloite(loader, koodistot_data):
    code = loader.get_object(koodistot_data[codes.LifeCycleStatus][0])
    assert code["id"]
    assert code["value"] == "01"
    assert "short_name" not in code.keys()
    assert code["name"]["fin"] == "Kaavoitusaloite"
    assert (
        code["description"]["fin"] == "Kuntaan tai maakuntaan saapunut kaavoitusaloite."
    )
    assert code["status"] == "DRAFT"
    assert code["level"] == 1
    assert "parent_id" not in code.keys()


def test_get_asumisen_alue(loader, koodistot_data):
    code = loader.get_object(koodistot_data[codes.TypeOfPlanRegulation][0])
    assert code["id"] == "15934bd8-419b-420b-9b1d-b12608bdf27a"
    assert code["value"] == "asumisenAlue"
    assert code["short_name"] == "A"
    assert code["name"]["fin"] == "Asumisen alue"
    assert (
        code["description"]["fin"]
        == "Ilmaisee, että kaavakohde kuvaa asumisen rakennuksille tai asunnoille tarkoitetun alueen. Käytetään asemakaavoissa ilmaisemaan asuinrakennusten alueita, joille voidaan rakentaa eri tyyppisiä asuinrakennuksia. Maakunta- ja yleiskaavoissa käytetään ilmaisemaan asuntoalueita, jolla kerrosalasta pääosa on tarkoitettu asumiseen. Koodi liittyy lähtökohtaisesti kaavakohteeseen, joka on geometrialtaan alue."
    )
    assert code["status"] == "DRAFT"
    assert code["level"] == 1
    assert "parent_id" not in code.keys()


def test_get_asuinpientaloalue(loader, koodistot_data):
    code = loader.get_object(koodistot_data[codes.TypeOfPlanRegulation][1])
    assert code["id"] == "e6f03e18-f292-4068-b6a6-b9e52206accc"
    assert code["value"] == "asuinpientaloalue"
    assert code["short_name"] == "AP"
    assert code["name"]["fin"] == "Asuinpientaloalue"
    assert (
        code["description"]["fin"]
        == "Ilmaisee, että kaavakohde kuvaa asuinpientaloille tarkoitetun alueen. Käytetään asemakaavoissa ilmaisemaan, että alueelle voidaan erilaisia pientaloja eli rivitaloja, kytkettyjä pientaloja ja erillisiä pientaloja asumistarkoituksiin. Käytetään yleiskaavoissa ilmaisemaan pientalovaltaista asuntoaluetta. Koodi liittyy lähtökohtaisesti kaavakohteeseen, joka on geometrialtaan alue."
    )
    assert code["status"] == "DRAFT"
    assert code["level"] == 2
    assert code["parent_id"] == "15934bd8-419b-420b-9b1d-b12608bdf27a"


def test_get_erillisten_asuinpientalojen_alue(loader, koodistot_data):
    code = loader.get_object(koodistot_data[codes.TypeOfPlanRegulation][2])
    assert code["id"] == "ba9a86d5-6944-4bc4-a86c-87a78c0cdc2a"
    assert code["value"] == "erillistenAsuinpientalojenAlue"
    assert code["short_name"] == "AO"
    assert code["name"]["fin"] == "Erillisten asuinpientalojen alue"
    assert (
        code["description"]["fin"]
        == "Ilmaisee, että kaavakohde kuvaa erillisille asuinpientaloille tarkoitetun alueen eli alueen, jolle on ja/tai sille voidaan rakentaa yksi- tai kaksiasuntoisia pientaloja (omakotitaloja Rakennusluokituksen 2018 mukainen koodiarvo 0110 tai paritaloja Rakennusluokituksen 2018 mukainen koodiarvo 0111) asumistarkoituksiin. Mikäli halutaan, että kullekin rakennuspaikalle saa rakentaa vain yhden asuinrakennuksen, tulee kaavakohteeseen liittää sanallinen määräys asiasta. Kaavamääräyslaji ei ota kantaa asuntojen omistusmuotoon eli siihen onko kyseessä yhtiömuotoinen erillistalo. Koodi liittyy lähtökohtaisesti kaavakohteeseen, joka on geometrialtaan alue."
    )
    assert code["status"] == "DRAFT"
    assert code["level"] == 3
    assert code["parent_id"] == "e6f03e18-f292-4068-b6a6-b9e52206accc"


def assert_data_is_imported(main_db_params):
    conn = psycopg2.connect(**main_db_params)
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT count(*) FROM codes.lifecycle_status")
            assert cur.fetchone()[0] == 2
            cur.execute(f"SELECT count(*) FROM codes.type_of_plan_regulation")
            assert cur.fetchone()[0] == 4
            cur.execute(f"SELECT count(*) FROM codes.plan_type")
            assert cur.fetchone()[0] == 0
    finally:
        conn.close()


def assert_changed_data_is_imported(main_db_params):
    conn = psycopg2.connect(**main_db_params)
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT count(*) FROM codes.lifecycle_status")
            assert cur.fetchone()[0] == 3
            cur.execute(f"SELECT count(*) FROM codes.type_of_plan_regulation")
            assert cur.fetchone()[0] == 4
            cur.execute(f"SELECT count(*) FROM codes.plan_type")
            assert cur.fetchone()[0] == 0
    finally:
        conn.close()


def test_save_objects(loader, koodistot_data, main_db_params):
    loader.save_objects(koodistot_data)
    assert_data_is_imported(main_db_params)


def test_save_changed_objects(
    changed_koodistot_data, connection_string, main_db_params
):
    # The database is already populated in the first test. Because
    # connection string (and therefore hame_database_created)
    # has module scope, the database persists between tests.
    assert_data_is_imported(main_db_params)
    # check that a new loader adds one object to the database
    loader = KoodistotLoader(
        connection_string,
        api_url="http://mock.url",
    )
    loader.save_objects(changed_koodistot_data)
    assert_changed_data_is_imported(main_db_params)
