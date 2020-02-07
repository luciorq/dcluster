from dcluster import config
from dcluster.cluster import simple as simple_cluster


def get(cluster_name):
    return simple_cluster.DeployedCluster.from_docker(cluster_name)


def stop_cluster(cluster_name):
    cluster = get(cluster_name)
    cluster.stop()


def remove_cluster(cluster_name):
    cluster = get(cluster_name)
    cluster.remove()


def ssh(args):
    '''
    Performs SSH to a node in the cluster. The target can have username@hostname, or only hostname
    (uses default ssh_user)
    '''
    (cluster_name, username, hostname, _) = interpret_ssh_args(args)

    # delegate ssh to cluster object
    cluster = get(cluster_name)
    cluster.ssh_to_node(username, hostname)


def scp(args):
    '''
    Performs SSH to a node in the cluster. The target can have username@hostname, or only hostname
    (uses default ssh_user)
    '''
    (cluster_name, username, hostname, target_dir) = interpret_ssh_args(args)

    files = args.files
    if not isinstance(args.files, list):
        files = [args.files, ]

    # delegate ssh to cluster object
    cluster = get(cluster_name)
    cluster.scp_to_node(username, hostname, target_dir, files)


def interpret_ssh_args(args):
    cluster_name = args.cluster_name
    target_dir = ''

    # handle user@hostname
    if '@' in args.target:
        (username, hostname) = args.target.split('@')
    else:
        username = config.prefs('ssh_user')
        hostname = args.target

    # handle scp target dir
    if ':' in hostname:
        (hostname, target_dir) = hostname.split(':')

    return (cluster_name, username, hostname, target_dir)
