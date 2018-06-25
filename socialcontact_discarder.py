##
# Cisco SocialMiner Bulk SocialContact Discarder
#
# This python script does the following:
#
#    0. Invokes a `/search` REST API request on SocialMiner for all socialcontacts
#       with specified sourceType and state, 200 at a time
#    1. Status of each socialcontact in the search result is updated to DISCARDED
#
# Requires:
#   - Python 3.x
#   - Requests (https://pypi.org/project/requests/)
#
# Licensed under the MIT License. For more details, see LICENSE file
#
# Cisco™ and SocialMiner™ are registered trademarks of Cisco Systems, Inc. (https://cisco.com)
#

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import argparse
import logging
import xml.etree.ElementTree as ElementTree
try:
    import requests
except ImportError:
    sys.exit("""
        The `requests` module must be pre-installed to run this script.

        Please install using:

            * pip (run "pip install requests"),
            * easy_install (run "easy_install requests")

        and try running this script again.
    """)

# CONSTANTS
SEARCH_API_URL = "http://{}/ccp-webapp/ccp/search/contacts?q="
SEARCH_API_PARAMS = "sc.sourceType:{}%20AND%20sc.socialContactStatus:{}%20AND%20sc.tags:{}&count={}&startIndex={}"
SC_STATUS_UPDATE_XML = "<SocialContact><status>{}</status><statusTimestamp>{}</statusTimestamp></SocialContact>"
SEARCH_MAX_BATCH_COUNT = 200
ATOM_NAMESPACE = {"atom": "http://www.w3.org/2005/Atom"}
OPENSEARCH_NAMESPACE = {"opensearch": "http://a9.com/-/spec/opensearch/1.1/"}
CCP_NAMESPACE = {"ccp": "http://www.cisco.com/ccbu/ccp/xml/socialcontact/1.0/"}

# log to STDOUT with a decent timestamp
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s: %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

def process_args():
    argParser = argparse.ArgumentParser(description="SocialMiner Contact Update")
    argParser.add_argument("--host", help="Hostname / IP Address of SocialMiner", required=True)
    argParser.add_argument("--user", help="Username of application admin account in SocialMiner", required=True)
    argParser.add_argument("--password", help="Password of application admin account in SocialMiner", required=True)
    argParser.add_argument("--sourceType", help="Source Type of Social Contacts", required=True)
    argParser.add_argument("--status", help="Source Type of Social Contacts", required=True)
    argParser.add_argument("--tag", help="Tag of Social Contacts", required=True)
    return vars(argParser.parse_args())


def search_contacts(host, user, password, sourceType, scStatus, tag, batchCount, startIndex):
    url = SEARCH_API_URL.format(host) + SEARCH_API_PARAMS.format(sourceType, scStatus, tag, batchCount, startIndex)
    logging.debug("Requesting GET {} ...".format(url))
    response = requests.get(url, auth=(user, password), verify=False)
    if response.status_code != requests.codes.ok:
        logging.error("FATAL - API request to SocialMiner failed with status {}. Error response: {}".format(response.status_code, response.text))
        sys.exit(1)
    return ElementTree.fromstring(response.text)


def update_contact_status(url, user, password, status, statusTimestamp):
    logging.debug("Updating SC [{}] status to [{}] ...".format(url, status))
    response = requests.put(url, data=SC_STATUS_UPDATE_XML.format(status, statusTimestamp), auth=(user, password), headers={"Content-Type": "application/xml"}, verify=False)
    if response.status_code != requests.codes.ok:
        logging.error("WARNING - Failed to update status of SC [{}] to [{}]. Error response: {}".format(url, status, response.text))


def discard_contacts(user, password, contacts):
    for contact in contacts:
        scRefURL = contact.find("atom:link[@rel='socialcontact']", ATOM_NAMESPACE).attrib['href']
        scStatusTimestamp = contact.find("ccp:scstatustimestamp", CCP_NAMESPACE).text
        update_contact_status(scRefURL, user, password, "discarded", scStatusTimestamp)


def main():
    args = process_args()
    logging.info("Running script with arguments: {}".format(args))

    while(True):
        responseXML = search_contacts(args["host"], args["user"], args["password"], args["sourceType"], args["status"], args["tag"], SEARCH_MAX_BATCH_COUNT, 0)
        total_contacts = int(responseXML.find("opensearch:totalResults", OPENSEARCH_NAMESPACE).text)
        if (total_contacts == 0):
            logging.info("No more contacts matching search query. Looks like we're all done.")
            break
        discard_contacts(args["user"], args["password"], responseXML.findall("atom:entry", ATOM_NAMESPACE))


if __name__ == '__main__':
    main()
