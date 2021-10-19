"""Script to build a Jenkins job and report on the result."""
import sys
from time import sleep
from urllib import parse

import requests


def get_build_url_and_why(url: str, jenkins_creds: tuple) -> (str, str):
    """Function to retrieve build url and queue status from a queued item."""
    response = requests.get(url, auth=jenkins_creds)
    print(f"Response {response.status_code} from GET on build url")
    json = response.json()
    build_url = json.get("executable").get("url") if "executable" in json else None
    return build_url, json.get("why")


def get_build_result_and_building(url: str, jenkins_creds: tuple) -> (str, bool):
    """Function to retrieve if build is still building and the result status."""
    response = requests.get(url, auth=jenkins_creds)
    print(f"Response {response.status_code} from GET on queue item")
    return response.json().get("result"), response.json().get("building")


def main(job: str, creds: str) -> None:
    """Main function."""
    print("Starting Jenkins job building script")

    # process inputs
    job_url = parse.urljoin(job, "build")  # /build endpoint to kick off job
    jenkins_creds = tuple(creds.split(":"))  # "abc:123" -> ("abc", "123")
    token = jenkins_creds[1]
    print("Got token:", token[0] + "*" * (len(token) - 2) + token[-1])  # useful debug

    # request build
    print("Making POST to request new build")
    response = requests.post(job_url, auth=jenkins_creds)
    print(f"Response {response.status_code} from POST on {job_url}")
    queued_item = response.headers["Location"]
    print("Item queued")

    # get build url from queued item
    print("Polling queued item:", queued_item)
    queued_item_url = parse.urljoin(queued_item, "api/json")
    build_url, why = get_build_url_and_why(queued_item_url, jenkins_creds)
    wait = 2
    while not build_url:
        wait = min(round(wait * 1.2, 2), 3600)  # increase wait by 20% with max 1 hour
        print(f"Still in queue. Reason: '{why}'. Retrying in {wait}s")
        sleep(wait)
        build_url, why = get_build_url_and_why(queued_item_url, jenkins_creds)
    print("Build started")

    # get result from build
    print("Polling build:", build_url)
    wait = 5
    build_url_json = parse.urljoin(build_url, "api/json")
    result, building = get_build_result_and_building(build_url_json, jenkins_creds)
    while result is None or building is True:
        wait = min(round(wait * 1.5, 2), 3600)  # increase wait by 50% with max 1 hour
        print(f"Build in progress. Status: {result}. Retrying in {wait}s")
        sleep(wait)
        result, building = get_build_result_and_building(build_url_json, jenkins_creds)

    # report on result
    print("Build complete. Result:", result)
    # exit(1) will mark workflow as failed and send email to repo maintainers
    sys.exit(0) if result == "SUCCESS" else sys.exit(1)


main(sys.argv[1], sys.argv[2])
