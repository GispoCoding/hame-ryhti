import io
import json
import logging
import os
import tempfile
import time
import zipfile
from typing import Dict, Optional, TypedDict
from xml.etree import ElementTree

import pygml
import requests
from codes import AdministrativeRegion, Municipality
from db_helper import DatabaseHelper, User
from geoalchemy2.shape import from_shape
from shapely.geometry import MultiPolygon, shape
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
For populating administrative regions (Maakunta) and municipalities (Kunta) with
geometries, adapted from Tarmo lambda functions
"""

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class Response(TypedDict):
    statusCode: int  # noqa N815
    body: str


class MMLLoader:
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    api_base = "https://avoin-paikkatieto.maanmittauslaitos.fi/tiedostopalvelu/ogcproc/v1/processes/hallinnolliset_aluejaot_vektori_koko_suomi"  # noqa
    job_api_base = (
        "https://avoin-paikkatieto.maanmittauslaitos.fi/tiedostopalvelu/dl/v1/"
    )
    payload = {
        "id": "hallinnolliset_aluejaot_vektori_koko_suomi",
        "inputs": {
            "fileFormatInput": "GML",
            "dataSetInput": "kuntajako_250k",
            "yearInput": 2023,
        },
    }

    def __init__(
        self, connection_string: str, api_url: Optional[str] = None, api_key: str = ""
    ) -> None:
        if api_url:
            self.api_base = api_url
        self.api_key = api_key

        engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=engine)
        LOGGER.info("Loader initialized")

    def get_geometries(self) -> Dict:
        """
        Gets administrative region geometries from from MML OGC API Process.
        """
        session = requests.Session()

        with tempfile.TemporaryDirectory() as output_dir:
            year = str(self.payload["inputs"]["yearInput"])  # type: ignore
            size = str(self.payload["inputs"]["dataSetInput"]).split("_")[-1]  # type: ignore # noqa

            url = f"{self.api_base}/execution?api-key={self.api_key}"
            LOGGER.info(f"Starting OGC API process on {self.api_base}/execution")
            r = session.post(url, headers=self.HEADERS, json=self.payload)
            r.raise_for_status()
            id_job = r.json()["jobID"]
            url_results = (
                f"{self.job_api_base}{id_job}/TietoaKuntajaosta_{year}_{size}.zip"
            )

            max_retries = 100
            attempts = 0
            while attempts < max_retries:
                try:
                    r = session.get(url_results)
                    r.raise_for_status()
                    break
                except requests.exceptions.HTTPError:
                    time.sleep(3)
                attempts += 1
                if attempts == max_retries:
                    raise requests.exceptions.RetryError(
                        f"Maximum retry limit of {max_retries} reached."
                    )

            zip_data = io.BytesIO(r.content)

            with zipfile.ZipFile(zip_data, "r") as zip_ref:
                zip_ref.extractall(output_dir)

            geoms = self.parse_gml(output_dir, year, size)

        return geoms

    def parse_gml(self, output_dir: str, year: str, size: str) -> Dict:
        """
        Parses a GML file to extract geometry data
        """
        tree = ElementTree.parse(
            f"{output_dir}/SuomenHallinnollisetYksikot_{year}_{size}.xml"
        )
        root = tree.getroot()
        namespaces = {
            "gml": "http://www.opengis.net/gml/3.2",
            f"au{size}": f"http://xml.nls.fi/inspire/au/4.0/{size}",
        }

        with self.Session() as session:
            region_codes = [
                value[0]
                for value in (
                    session.query(AdministrativeRegion.value)
                    .order_by(AdministrativeRegion.value)
                    .all()
                )
            ]
            municipality_codes = [
                value[0]
                for value in (
                    session.query(Municipality.value).order_by(Municipality.value).all()
                )
            ]

        polygons = {}

        au_elements = root.findall(f".//au{size}:AdministrativeUnit_{size}", namespaces)
        prefix = "{" + namespaces["gml"] + "}"
        for au_elem in au_elements:
            au_id = au_elem.get(prefix + "id")

            if au_id and (
                au_id.startswith("FI_AU_ADMINISTRATIVEUNIT_REGION_")
                or au_id.startswith("FI_AU_ADMINISTRATIVEUNIT_MUNICIPALITY_")
            ):
                gml_elements = au_elem.findall(".//gml:*", namespaces)
                for gml_elem in gml_elements:
                    gml_string = ElementTree.tostring(
                        gml_elem, encoding="unicode", method="xml"
                    )
                    # Extract polygons
                    if gml_string.startswith("<ns0:Polygon"):
                        id = au_id.split("_")[-1]
                        polygons[id] = gml_string

        # Parse GML elements into shapely geometries
        geoms = {}
        for region_code in region_codes:
            if region_code in polygons:
                geom = pygml.parse(polygons[region_code])
                geoms[region_code] = from_shape(
                    MultiPolygon([(shape(geom.__geo_interface__))])
                )
        for municipality_code in municipality_codes:
            if municipality_code in polygons:
                geom = pygml.parse(polygons[municipality_code])
                geoms[municipality_code] = from_shape(
                    MultiPolygon([(shape(geom.__geo_interface__))])
                )

        return geoms

    def save_geometries(self, geoms: Dict) -> str:
        """
        Save all geometries into the corresponding tables.
        """
        successful_actions = 0
        with self.Session() as session:
            admin_regions = session.query(AdministrativeRegion).all()
            municipalities = session.query(Municipality).all()
            for admin_region in admin_regions:
                LOGGER.info(
                    f"Adding geometry to administrative region {admin_region.value}..."
                )
                if geom := geoms.get(admin_region.value):
                    admin_region.geom = geom
                    LOGGER.info(
                        f"Geometry added to administrative region {admin_region.value}"  # noqa
                    )
                    successful_actions += 1
            for municipality in municipalities:
                LOGGER.info(f"Adding geometry to municipality {municipality.value}...")
                if geom := geoms.get(municipality.value):
                    municipality.geom = geom
                    LOGGER.info(
                        f"Geometry added to municipality {municipality.value}"  # noqa
                    )
                    successful_actions += 1
            session.commit()
        msg = f"{successful_actions} inserted or updated. 0 deleted."
        LOGGER.info(msg)
        return msg


def handler(event, _) -> Response:
    """Handler which is called when accessing the endpoint."""
    response: Response = {"statusCode": 200, "body": json.dumps("")}
    db_helper = DatabaseHelper(user=User.ADMIN)
    api_key = os.environ.get("MML_APIKEY")
    if not api_key:
        raise ValueError(
            "Please set MML_APIKEY environment variable to fetch geometries."  # noqa
        )

    loader = MMLLoader(db_helper.get_connection_string(), api_key=api_key)
    LOGGER.info("Getting objects...")
    geoms = loader.get_geometries()

    LOGGER.info("Saving objects...")
    msg = loader.save_geometries(geoms)
    response["body"] = json.dumps(msg)
    return response
