#!/usr/bin/env python
"""
You can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 2
of the License.
Copyright Andrea Briganti a.k.a 'Kbyte'
"""
import io
import subprocess
import argparse

import nagiosplugin


class SystemdStatus(nagiosplugin.Resource):
    name = 'SYSTEMD'

    def probe(self):
        # Execute systemctl --failed --no-legend and get output
        try:
            p = subprocess.Popen(['systemctl', '--failed', '--no-legend'],
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            stdout, stderr = p.communicate()
        except OSError as e:
            raise nagiosplugin.CheckError(e)

        if stderr:
            raise nagiosplugin.CheckError(stderr)

        if stdout:
            for line in io.StringIO(stdout.decode('utf-8')):
                split_line = line.split()
                unit = split_line[0]
                active = split_line[2]
                yield nagiosplugin.Metric(unit, active, context='systemd')
        else:
            yield nagiosplugin.Metric('all', None, context='systemd')


class ServiceStatus(nagiosplugin.Resource):
    name = 'SYSTEMD'

    def __init__(self, *args, **kwargs):
        self.service = kwargs.pop('service')
        super(nagiosplugin.Resource, self).__init__(*args, **kwargs)

    def probe(self):
        # Execute systemctl is-active and get output
        try:
            p = subprocess.Popen(['systemctl', 'is-active', self.service],
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            stdout, stderr = p.communicate()
        except OSError as e:
            raise nagiosplugin.CheckError(e)

        if stderr:
            raise nagiosplugin.CheckError(stderr)
        if stdout:
            for line in io.StringIO(stdout.decode('utf-8')):
                yield nagiosplugin.Metric(self.service, line.strip(), context='systemd')


class SystemdContext(nagiosplugin.Context):

    def __init__(self):
        super(SystemdContext, self).__init__('systemd')

    def evaluate(self, metric, resource):
        hint = '%s: %s' % (metric.name, metric.value) if metric.value else metric.name
        if metric.value and metric.value != 'active':
            return self.result_cls(nagiosplugin.Critical, metric=metric, hint=hint)
        else:
            return self.result_cls(nagiosplugin.Ok, metric=metric, hint=hint)


class SystemdSummary(nagiosplugin.Summary):

    def problem(self, results):
        return ', '.join(['{0}'.format(result) for result in results.most_significant])

    def verbose(self, results):
        return ['{0}: {1}'.format(result.state, result) for result in results]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--service", type=str, dest="service", help="Name of the Service that is beeing tested")
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase output verbosity (use up to 3 times)')

    args = parser.parse_args()

    if args.service is None:
        check = nagiosplugin.Check(
            SystemdStatus(),
            SystemdContext(),
            SystemdSummary())
    else:
        check = nagiosplugin.Check(
            ServiceStatus(service=args.service),
            SystemdContext(),
            SystemdSummary())
    check.main(args.verbose)


if __name__ == '__main__':
    main()
