#!/usr/bin/env python
"""
You can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 2
of the License.

Copyright Andrea Briganti a.k.a 'Kbyte'
"""

import nagiosplugin
import subprocess
import io


class SystemdStatus(nagiosplugin.Resource):
    name = 'SYSTEMD'

    def probe(self):
        # Execute systemctl --failed --no-legend and get output
        try:
            p = subprocess.Popen(['systemctl', '--failed', '--no-legend'],
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            pres, err = p.communicate()
        except FileNotFoundError as e:
            raise nagiosplugin.CheckError(e)

        if err:
            raise nagiosplugin.CheckError(err)

        if pres:
            result = ""
            for line in io.StringIO(pres.decode('utf-8')):
                result = "%s %s" % (result, line.split(' ')[0])

            return [nagiosplugin.Metric('systemd', (False, result), context='systemd')]

        return [nagiosplugin.Metric('systemd', (True, None), context='systemd')]


class SystemdContext(nagiosplugin.Context):
    def __init__(self):
        super(SystemdContext, self).__init__('systemd')

    def evaluate(self, metric, resource):
        value, output = metric.value
        if value:
            return self.result_cls(nagiosplugin.Ok, metric=metric)
        else:
            return self.result_cls(nagiosplugin.Critical, metric=metric, hint='failed units: %s' % output)


def main():
    check = nagiosplugin.Check(
        SystemdStatus(),
        SystemdContext())

    check.main()


if __name__ == '__main__':
    main()
