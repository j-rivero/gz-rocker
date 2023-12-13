import em
import pkgutil
import sys
from rocker.extensions import RockerExtension, name_to_argument


class Gazebo(RockerExtension):
    @staticmethod
    def get_name():
        return 'gazebo'

    @staticmethod
    def get_releases():
        return {'citadel', 'dome', 'edifice', 'fortress'}

    @staticmethod
    def get_OSs():
        return {'bionic', 'focal'}

    def __init__(self):
        self._env_subs = {}
        self.name = Gazebo.get_name()

    def precondition_environment(self, cli_args):
        pass

    def validate_environment(self, cli_args):
        pass

    def get_preamble(self, cli_args):
        return ''

    def get_snippet(self, cli_args):
        gz_ver, linux_ver = cli_args[Gazebo.get_name()].split(':')

        if (gz_ver not in Gazebo.get_releases()):
            print("WARNING specified Gazebo version '%s' is not valid, must \
                   choose from " % gz_ver, Gazebo.get_releases())
            sys.exit(1)
        if (linux_ver not in Gazebo.get_OSs()):
            print("WARNING specified OS '%s' is not valid, must choose from \
                  % linux_ver", Gazebo.get_OSs())
            sys.exit(1)

        self._env_subs['gz_distro'] = gz_ver
        self._env_subs['system_version'] = linux_ver
        snippet = pkgutil.get_data(
            'gz_rocker',
            'templates/%s_snippet.Dockerfile.em' % self.name).decode('utf-8')
        return em.expand(snippet, self._env_subs)

    def get_docker_args(self, cli_args):
        return ''

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument(
            name_to_argument(Gazebo.get_name()),
            default=defaults.get(Gazebo.get_name(), None),
            metavar='$GAZEBO_VERSION:$SYSTEM_VERSION',
            help="Install a specific version of the Gazebo Robotics binary \
                  packages, along with the Gazebo version's build \
                  dependencies for a particular platform. $GAZEBO_VERSION \
                  must be either %s, and $SYSTEM_VERSION must be either %s. \
                  $SYSTEM_VERSION should match the base image being used."
                    % (Gazebo.get_releases(), Gazebo.get_OSs()))
