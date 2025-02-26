import inspect
import json
import logging
from typing import Any, Dict, List, Optional, Type, TypedDict

import codes
import requests
from db_helper import DatabaseHelper, User
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

"""
Koodistot.suomi.fi client for populating all code tables, adapted from
Tarmo lambda functions
"""

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class Response(TypedDict):
    statusCode: int  # noqa N815
    body: str


class Event(TypedDict):
    """
    Supports creating codes both online and from local code classes.
    """

    suomifi_codes: Optional[bool]
    local_codes: Optional[bool]


def iso_639_two_to_three_letter(language_dict: Dict[str, str]) -> Dict[str, str]:
    """
    Koodistot.suomi.fi uses two letter iso codes, while we use three letter codes.
    """
    language_map = {"fi": "fin", "sv": "swe", "en": "eng"}
    return {language_map[key]: value for key, value in language_dict.items()}


def get_code_list_url(api_base: str, code_registry: str, code_list: str) -> str:
    return f"{api_base}/{code_registry}/codeschemes/{code_list}/codes"


class KoodistotLoader:
    HEADERS = {"User-Agent": "HAME - Ryhti compatible Maakuntakaava database"}
    api_base = "https://koodistot.suomi.fi/codelist-api/api/v1/coderegistries"

    def __init__(
        self,
        connection_string: str,
        api_url: Optional[str] = None,
        load_suomifi_codes: Optional[bool] = True,
        load_local_codes: Optional[bool] = True,
    ) -> None:
        if api_url:
            self.api_base = api_url
        engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=engine)

        # Only load koodistot that have data source defined
        self.koodistot: List[Type[codes.CodeBase]] = [
            code_class
            for name, code_class in inspect.getmembers(codes, inspect.isclass)
            if issubclass(code_class, codes.CodeBase)
            and (
                (load_suomifi_codes and code_class.code_list_uri)
                or (load_local_codes and code_class.local_codes)
            )
        ]
        if load_suomifi_codes:
            LOGGER.info("Loading codes from suomi.fi")
        if load_local_codes:
            LOGGER.info("Loading local codes")
        LOGGER.info("Loader initialized with code classes:")
        LOGGER.info(self.koodistot)

    def get_code_registry_data(self, koodisto: Type[codes.CodeBase]) -> Dict[str, Dict]:
        """
        Get code registry codes for given koodisto, or empty list if not present.
        Index returned codes by code value. Also, order returned codes by hierarchy
        level to ease dependent code creation.
        """
        if not koodisto.code_list_uri:
            return dict()
        code_registry, name = koodisto.code_list_uri.rsplit("/", 2)[-2:None]
        LOGGER.info(koodisto.code_list_uri)
        LOGGER.info(code_registry)
        LOGGER.info(name)
        url = get_code_list_url(self.api_base, code_registry, name)
        LOGGER.info(f"Loading codes from {url}")
        r = requests.get(url, headers=self.HEADERS)
        r.raise_for_status()
        try:
            result_list: List[Dict] = r.json()["results"]
            # Order external codes by hierarchyLevel
            result_dict = {
                item["codeValue"]: item
                for item in sorted(result_list, key=lambda item: item["hierarchyLevel"])
            }
            return result_dict
        except (KeyError, requests.exceptions.JSONDecodeError):
            LOGGER.warning(f"{koodisto} response did not contain data")
            return dict()

    def get_objects(self) -> Dict[Type[codes.CodeBase], Dict[str, Dict]]:
        """
        Gets all koodistot data, divided by table and code value, ordered by code level.
        """
        data = dict()
        for koodisto in self.koodistot:
            # Fetch external codes
            data[koodisto] = self.get_code_registry_data(koodisto)
            # Add local codes with status to distinguish them from other codes
            local_codes = {
                code["value"]: dict(code, status="LOCAL")
                for code in koodisto.local_codes
            }
            data[koodisto] |= local_codes
        return data

    def get_object(
        self,
        code_class: Type[codes.CodeBase],
        element: Dict,
        all_objects: Optional[Dict[Type[codes.CodeBase], Dict[str, Dict]]] = None,
    ) -> Optional[Dict]:
        """
        Returns database-ready dict of object to import, or None if the data
        was invalid.

        Optionally, you may include the dict containing all objects, to allow
        creating relationships between different classes of code objects.
        """
        # local codes are already in database-ready format
        if element["status"] == "LOCAL":
            return element
        code_dict = dict()
        # Use uuids from koodistot.suomi.fi. This way, we can save all the children
        # easily by referring to their parents.
        code_dict["id"] = element["id"]
        code_dict["value"] = element["codeValue"]
        short_name = element.get("shortName", None)
        if short_name:
            code_dict["short_name"] = short_name
        code_dict["name"] = iso_639_two_to_three_letter(element["prefLabel"])
        if "description" in element.keys():
            code_dict["description"] = iso_639_two_to_three_letter(
                element["description"]
            )
        code_dict["status"] = element["status"]
        code_dict["level"] = element["hierarchyLevel"]

        # Elements have already been ordered by hierarchyLeve, so parent already
        # exists whenever we are adding a lower level code!
        parent = element.get("broaderCode", None)
        if parent:
            code_dict["parent_id"] = parent["id"]

        # Some code classes may have relationships to *other* code classes. In this
        # case, we don't have the sqlalchemy objects created yet. However, we *do*
        # know the ids of the objects to be created, so we can provide a list
        # of the related ids that should be linked to this object, to be processed
        # later. Any relationships must be hardcoded here.
        if hasattr(code_class, "allowed_status_dict") and all_objects:
            statuses_with_code = [
                key
                for key, values in code_class.allowed_status_dict.items()
                if code_dict["value"] in values
            ]
            code_dict["allowed_status_ids"] = [
                all_objects[codes.LifeCycleStatus][value]["id"]
                for value in statuses_with_code
            ]
        return code_dict

    def update_remote_children_of_local_parents(
        self,
        instance: codes.CodeBase,
        child_values: List[str],
        session: Session,
    ) -> None:
        """
        After a local parent code is created, update any existing children to point
        to the local parent, overriding the remote parent. Everything is flushed
        to the database so that children are queryable.
        """
        session.flush()
        code_class = type(instance)
        children = (
            session.query(code_class).filter(code_class.value.in_(child_values)).all()
        )
        instance.children = children

    def update_or_create_object(
        self,
        code_class: Type[codes.CodeBase],
        incoming: Dict[str, Any],
        session: Session,
        saved_objects: Optional[Dict[str, codes.CodeBase]] = None,
    ) -> codes.CodeBase:
        """
        Find object based on its unique fields, or create new object. Update fields
        that are present in the incoming dict.

        However, do *not* try to update uuids. They may have references to them already,
        so we cannot set uuids, even if they are the same as before.

        Optionally, you may include the dict containing all saved objects, to allow
        creating relationships between different classes of code objects.
        """
        columns = code_class.__table__.columns
        unique_keys = set(column.key for column in columns if column.unique)
        unique_values = {
            key: incoming[key] for key in set(incoming.keys()).intersection(unique_keys)
        }
        instance = session.query(code_class).filter_by(**unique_values).first()
        column_keys = set(columns.keys())
        values = {
            key: incoming[key] for key in set(incoming.keys()).intersection(column_keys)
        }

        # Some code classes may have relationships to *other* code classes.
        # Relationships are stored in separate tables, so they will not be present in
        # the columns. Instead, we must provide the related objects to the relationship.
        # Any relationship names must be hardcoded here.
        if "allowed_status_ids" in incoming.keys() and saved_objects:
            values["allowed_statuses"] = [
                saved_objects[id] for id in incoming["allowed_status_ids"]
            ]

        if instance:
            # go figure, if we have the instance (and don't want to do the update right
            # now) sqlalchemy has no way of supplying attribute dict to be updated.
            # This is because dirtying sqlalchemy objects happens via the __setattr__
            # method, so we will have to update instance fields one by one.
            for key, value in values.items():
                if key != "id":
                    setattr(instance, key, value)
        else:
            instance = code_class(**values)
            session.add(instance)

        # If children are defined in the incoming dict, they must be updated manually.
        if "child_values" in incoming.keys():
            self.update_remote_children_of_local_parents(
                instance, incoming["child_values"], session
            )
            print("instance now has children")
            print(instance.children)
        return instance

    def save_objects(self, objects: Dict[Type[codes.CodeBase], Dict[str, dict]]) -> str:
        """
        Save all objects in the objects dict, grouped by object class.
        """
        saved_objects: Dict[str, codes.CodeBase] = dict()
        with self.Session() as session:
            for code_class, class_codes in objects.items():
                LOGGER.info(f"Importing codes to {code_class}...")
                for i, element in enumerate(class_codes.values()):
                    if i % 10 == 0:
                        LOGGER.info(
                            f"{100 * float(i) / len(class_codes)}% - {i}/{len(class_codes)}"  # noqa
                        )
                    code = self.get_object(code_class, element, objects)
                    if code is not None:
                        succeeded = self.update_or_create_object(
                            code_class, code, session, saved_objects
                        )
                        if succeeded:
                            saved_objects[succeeded.id] = succeeded
                        else:
                            LOGGER.debug(f"Could not save code data {element}")
                    else:
                        LOGGER.debug(f"Invalid code data {element}")
            session.commit()
        msg = f"{len(saved_objects)} inserted or updated. 0 deleted."
        LOGGER.info(msg)
        return msg


def handler(event: Event, _) -> Response:
    """Handler which is called when accessing the endpoint."""
    response: Response = {"statusCode": 200, "body": json.dumps("")}
    db_helper = DatabaseHelper(user=User.ADMIN)
    load_suomifi_codes = event.get("suomifi_codes", True)
    load_local_codes = event.get("local_codes", True)

    loader = KoodistotLoader(
        db_helper.get_connection_string(),
        load_suomifi_codes=load_suomifi_codes,
        load_local_codes=load_local_codes,
    )
    LOGGER.info("Getting objects...")
    objects = loader.get_objects()

    LOGGER.info("Saving objects...")
    msg = loader.save_objects(objects)
    response["body"] = json.dumps(msg)
    return response
