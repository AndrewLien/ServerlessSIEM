#!/usr/bin/env python
#    This file is part of python-evtx.
#
#   Copyright 2012, 2013 Willi Ballenthin <william.ballenthin@mandiant.com>
#                    while at Mandiant <http://www.mandiant.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   Version v0.1.1

import Evtx.Evtx as evtx
import xmltodict
import json
from google.cloud import pubsub_v1


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Dump a binary EVTX file into XML.")
    parser.add_argument("evtx", type=str,
                        help="Path to the Windows EVTX event log file, for example: %SystemRoot%\System32\Winevt\Logs\Security.evtx")
    parser.add_argument("topic_id", type=str,
                        help="Topic ID of the pubsub server")

    parser.add_argument("project_id", type=str,
                        help="project_id of the serverless project")


    args = parser.parse_args()
    batch_settings = pubsub_v1.types.BatchSettings(
        max_bytes=1024,  # One kilobyte
        max_latency=1,  # One second
    )

    # Adding in additional support to pubsub
    publisher = pubsub_v1.PublisherClient(batch_settings)
    topic_path = publisher.topic_path(args.project_id, args.topic_id)
    with evtx.Evtx(args.evtx) as log:
        for record in log.records():
            dict_xml = xmltodict.parse(record.xml())['Event']
            js_dump = json.dumps(dict_xml)
            data = js_dump.encode('utf-8')
            publisher.publish(topic_path, data=data)


if __name__ == "__main__":
    main()