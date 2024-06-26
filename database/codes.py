from models import CodeBase


class LifeCycleStatus(CodeBase):
    """
    Elinkaaren vaihe
    """

    __tablename__ = "lifecycle_status"
    code_list_uri = "http://uri.suomi.fi/codelist/rytj/kaavaelinkaari"


class PlanType(CodeBase):
    """
    Kaavalaji
    """

    __tablename__ = "plan_type"
    code_list_uri = "http://uri.suomi.fi/codelist/rytj/RY_Kaavalaji"


class TypeOfPlanRegulation(CodeBase):
    """
    Kaavamääräyslaji
    """

    __tablename__ = "type_of_plan_regulation"
    code_list_uri = "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayslaji"


class TypeOfAdditionalInformation(CodeBase):
    """
    Kaavamääräyksen lisätiedon laji

    HAME-Ryhti-tietomallissa tämän koodiston arvot jaetaan useaan monivalintakenttään,
    joista jokaisesta käyttäjä voi valita yhden koodin.

    Toteutetaan kentät niin, että jokaisessa on filtteri, joka tarkistaa sopivan
    koodistoarvon. Tietokantaan voi tallentaa vain arvon jolla on oikea parent. Ainakin
    osissa kentistä tämä toimii sellaisenaan, koska arvot on RYTJ:ssä ryhmitelty oikein.
    """

    # Let's use a shortish table name, since the long name creates indexes that have
    # names that are too long for PostgreSQL, hooray :D
    __tablename__ = "type_of_additional_information"
    code_list_uri = (
        "http://uri.suomi.fi/codelist/rytj/RY_Kaavamaarayksen_Lisatiedonlaji"
    )
    local_codes = [
        {
            "value": "kayttotarkoitus",
            "name": {"fin": "Käyttötarkoitus"},
            "child_values": [
                "paakayttotarkoitus",
                "osaAlue",
                "poisluettavaKayttotarkoitus",
                "yhteystarve",
            ],
        },
        {
            "value": "olemassaolo",
            "name": {"fin": "Olemassaolo"},
            "child_values": [
                "olemassaOleva",
                "sailytettava",
                "uusi",
                "olennaisestiMuuttuva",
            ],
        },
        {
            "value": "kehittaminen",
            "name": {"fin": "Kehittäminen"},
            "child_values": [
                "reservialue",
                "kehitettava",
                "merkittavastiParannettava",
                "eheytettavaTaiTiivistettava",
            ],
        },
    ]


class TypeOfVerbalPlanRegulation(CodeBase):
    """
    Sanallisen määräyksen laji

    Epäselvää milloin tätä käytetään.
    """

    __tablename__ = "type_of_verbal_plan_regulation"
    code_list_uri = (
        "http://uri.suomi.fi/codelist/rytj/RY_Sanallisen_Kaavamaarayksen_Laji"
    )


class TypeOfSourceData(CodeBase):
    """
    Lähtöaineiston laji
    """

    __tablename__ = "type_of_source_data"
    code_list_uri = "http://uri.suomi.fi/codelist/rytj/RY_LahtotietoaineistonLaji"


class TypeOfUnderground(CodeBase):
    """
    Maanalaisuuden laji
    """

    __tablename__ = "type_of_underground"
    code_list_uri = "http://uri.suomi.fi/codelist/rytj/RY_MaanalaisuudenLaji"


class TypeOfDocument(CodeBase):
    """
    Asiakirjatyyppi
    """

    __tablename__ = "type_of_document"
    code_list_uri = "http://uri.suomi.fi/codelist/rytj/RY_AsiakirjanLaji_YKAK"


class AdministrativeRegion(CodeBase):
    """
    Maakunta
    """

    __tablename__ = "administrative_region"
    code_list_uri = "http://uri.suomi.fi/codelist/jhs/maakunta_1_20240101"


class TypeOfPlanRegulationGroup(CodeBase):
    """
    Kaavamääräysryhmän tyyppi

    This is our own code list. It does not exist in koodistot.suomi.fi.
    """

    __tablename__ = "type_of_plan_regulation_group"
    code_list_uri = ""
    local_codes = [
        {"value": "generalRegulations", "name": {"fin": "Yleismääräykset"}},
        {"value": "landUseRegulations", "name": {"fin": "Aluevaraus"}},
        {"value": "otherAreaRegulations", "name": {"fin": "Osa-alue"}},
        {"value": "lineRegulations", "name": {"fin": "Viiva"}},
        {"value": "otherPointRegulations", "name": {"fin": "Muu piste"}},
    ]


class PlanTheme(CodeBase):
    """
    Kaavoitusteema
    """

    __tablename__ = "plan_theme"
    code_list_uri = "http://uri.suomi.fi/codelist/rytj/kaavoitusteema"


class CategoryOfPublicity(CodeBase):
    """
    Asiakirjan julkisuusluokka
    """

    __tablename__ = "category_of_publicity"
    code_list_uri = "http://uri.suomi.fi/codelist/rytj/julkisuus"


class TypeOfInteractionEvent(CodeBase):
    """
    Vuorovaikutustapahtuman laji (kaava)
    """

    __tablename__ = "type_of_interaction_event"
    code_list_uri = (
        "http://uri.suomi.fi/codelist/rytj/RY_KaavanVuorovaikutustapahtumanLaji"
    )


class NameOfPlanCaseDecision(CodeBase):
    """
    Kaava-asian päätöksen nimi
    """

    __tablename__ = "name_of_plan_case_decision"
    code_list_uri = "http://uri.suomi.fi/codelist/rytj/kaavpaatnimi"


class TypeOfProcessingEvent(CodeBase):
    """
    Käsittelytapahtuman laji
    """

    __tablename__ = "type_of_processing_event"
    code_list_uri = "http://uri.suomi.fi/codelist/rytj/kaavakastap"
