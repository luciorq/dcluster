

def configure_stop_parser(stop_parser):
    '''
    Configure argument parser for stop subcommand.
    '''
    stop_parser.add_argument('cluster_name', help='name of the virtual cluster')

    # default function to call
    stop_parser.set_defaults(func=process_stop_cli_call)


def configure_start_parser(start_parser):
    '''
    Configure argument parser for start subcommand.
    '''
    start_parser.add_argument('cluster_name', help='name of the virtual cluster')

    # default function to call
    start_parser.set_defaults(func=process_start_cli_call)


def configure_rm_parser(rm_parser):
    '''
    Configure argument parser for rm subcommand.
    '''
    rm_parser.add_argument('cluster_name', help='name of the Docker cluster')

    # default function to call
    rm_parser.set_defaults(func=process_rm_cli_call)


def process_stop_cli_call(args):
    '''
    Process the stop request through command line.
    '''
    # to avoid chain of dependencies (docker!) before dcluster init
    from dcluster.actions import manage as manage_action

    manage_action.stop_cluster(args.cluster_name)
    print('Stopped cluster: {}'.format(args.cluster_name))


def process_start_cli_call(args):
    '''
    Process the start request through command line.
    '''
    # to avoid chain of dependencies (docker!) before dcluster init
    from dcluster.actions import manage as manage_action

    manage_action.start_cluster(args.cluster_name)


def process_rm_cli_call(args):
    '''
    Process the remove request through command line.
    '''
    # to avoid chain of dependencies (docker!) before dcluster init
    from dcluster.actions import manage as manage_action

    manage_action.remove_cluster(args.cluster_name)
    print('Removed cluster: {}'.format(args.cluster_name))
