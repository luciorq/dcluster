from dcluster.tests.test_dcluster import DclusterTest
from dcluster.tests.stubs import extended_stubs


class CreateExtendedHeadPlan(DclusterTest):
    '''
    Unit tests for node.planner.DefaultNodePlanner with extended stubs
    '''

    def setUp(self):
        self.maxDiff = None

    def test_create_head_plan(self):
        # given
        cluster_name = 'mycluster'
        subnet_str = u'172.30.0.0/24'
        compute_count = 3
        plan_data = extended_stubs.slurm_plan_data_stub(cluster_name, compute_count)

        # under test
        node_planner = extended_stubs.extended_node_planner_stub(cluster_name, subnet_str)

        # when
        result = node_planner.create_head_plan(plan_data)

        # then
        expected = {
            'hostname': 'head',
            'hostname_alias': 'head-ice1-1',
            'container': 'mycluster-head',
            'image': 'rhel76-slurm:v2',
            'ip_address': '172.30.0.253',
            'role': 'head',
            'static_text': '''        command:
          - slurmctld
        environment:
          MYSQL_DATABASE: slurm_acct_db
          MYSQL_PASSWORD: password
          MYSQL_RANDOM_ROOT_PASSWORD: 'yes'
          MYSQL_USER: slurm
        expose:
          - '6817'
          - '6819'
      ''',
            'volumes': [
                '/home:/home',
                '/opt/intel:/opt/intel',
                '/srv/shared:/srv/dcluster/shared',
                'var_lib_mysql:/var/lib/mysql',
                'etc_munge:/etc/munge',
                'etc_slurm:/etc/slurm',
                'slurm_jobdir:/data',
                'var_log_slurm:/var/log/slurm'
            ],
            'systemctl': False
        }
        self.assertEqual(dict(result._asdict()), expected)
