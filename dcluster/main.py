'''
Main entry point of dcluster.
'''

import argparse
import logging
import os
import sys

# from six.moves import input

from . import ansible_facade
from . import inventory
from . import networking


def process_creation(args):

    log = logging.getLogger()
    log.info('Got create parameters %s %s %s' % (args.cluster_name, args.compute_count,
                                                 args.basepath))

    # create the docker network
    cluster_network = networking.create(args.cluster_name)

    # create the inventory
    host_details = cluster_network.build_host_details(int(args.compute_count))
    network_name = cluster_network.network_name()
    ansible_environment = inventory.AnsibleEnvironment.create(network_name,
                                                              host_details, args.basepath)

    # call Ansible playbook
    docker_path = os.path.join(ansible_environment.cluster_home, 'docker')
    extra_vars = 'docker_path=%s' % docker_path
    ansible_facade.run_playbook('cluster.yml', ansible_environment.ansible_home,
                                extra_vars=extra_vars)

    log.info('Docker cluster %s -  %s created!' % (network_name, str(cluster_network)))


def configure_create_parser(create_parser):
    create_parser.add_argument('cluster_name', help='name of the Docker cluster')
    create_parser.add_argument('compute_count', help='number of compute nodes in cluster')

    msg = 'directory where cluster files are created (set to $PWD by script)'
    create_parser.add_argument('--basepath', help=msg)

    # default function to call
    create_parser.set_defaults(func=process_creation)


def processRequest():

    # top level parser
    desc = 'clustertest: deploy clusters of Docker containers'
    parser = argparse.ArgumentParser(prog='clustertest', description=desc)
    subparsers = parser.add_subparsers(help='Run clustertest <command> for additional help')

    # below we create subparsers for the subcommands
    create_parser = subparsers.add_parser('create', help='create a cluster')
    configure_create_parser(create_parser)

    # show help if no subcommand is given
    # assume 'basepath <basepath>' is always passed (by script)
    if len(sys.argv) == 3:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # activate parsing and sub-command function call
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    log_level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s - %(levelname)6s | %(message)s',
                        level=log_level, datefmt='%d-%b-%y %H:%M:%S')
    processRequest()