#!/usr/bin/env python
################################################################################
#                 _    ____ ___   _____           _ _    _ _                   #
#                / \  / ___|_ _| |_   _|__   ___ | | | _(_) |_                 #
#               / _ \| |    | |    | |/ _ \ / _ \| | |/ / | __|                #
#              / ___ \ |___ | |    | | (_) | (_) | |   <| | |_                 #
#        ____ /_/   \_\____|___|___|_|\___/ \___/|_|_|\_\_|\__|                #
#       / ___|___   __| | ___  / ___|  __ _ _ __ ___  _ __ | | ___  ___        #
#      | |   / _ \ / _` |/ _ \ \___ \ / _` | '_ ` _ \| '_ \| |/ _ \/ __|       #
#      | |__| (_) | (_| |  __/  ___) | (_| | | | | | | |_) | |  __/\__ \       #
#       \____\___/ \__,_|\___| |____/ \__,_|_| |_| |_| .__/|_|\___||___/       #
#                                                    |_|                       #
################################################################################
#                                                                              #
# Copyright (c) 2015 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
#    Licensed under the Apache License, Version 2.0 (the "License"); you may   #
#    not use this file except in compliance with the License. You may obtain   #
#    a copy of the License at                                                  #
#                                                                              #
#         http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                              #
#    Unless required by applicable law or agreed to in writing, software       #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################
"""
Simple application that shows all of the processes running on a switch
"""
import json
import sys

import acitoolkit as ACI
from acitoolkit.acitoolkitlib import Credentials


def main():
    """
    Main show Process routine
    :return: None
    """
    description = 'Simple application that logs on to the APIC and check cluster information for a fabric'
    creds = Credentials('apic', description)

    args = creds.get()

    session = ACI.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print '%% Could not login to APIC'
        sys.exit(0)

    cluster = ACI.Cluster('Cluster')
    configured_size = cluster.get_config_size(session)
    cluster_size = cluster.get_cluster_size(session)
    cluster_info = cluster.get_cluster_info(session)

    if configured_size != cluster_size:
        print("*******************************************************")
        sys.stdout.write("WARNING, configured cluster size ")
        sys.stdout.write(configured_size)
        sys.stdout.write(" :not equal to the actual size ")
        print cluster_size
        print "WARNING, desired stats collection might be lost"
        print("*******************************************************")
        print("APICs in the cluster are:")
        for apic in cluster_info:
            print json.dumps(apic['infraCont']['attributes']['dn'], indent=4, sort_keys=True)
    else:
        print("PASS")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
