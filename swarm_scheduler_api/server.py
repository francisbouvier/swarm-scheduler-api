#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import json
import random
import argparse

import docker
from tornado import ioloop, web


class CreateContainer(web.RequestHandler):

    def _select_node(self, nodes):
        """Dummmy random function to select node"""
        return random.choice(nodes)

    def post(self):

        # Parse arguments
        args = json.loads(self.request.body)
        node = self._select_node(args['Nodes'])
        host = node['Addr'].replace('http', 'tcp')
        if args['Name'] == '':
            name = None
        else:
            name = args['Name']

        # Create and start container
        client = docker.Client(base_url=host)
        container = client.create_container_from_config(
            config=args['Container'], name=name)
        # Hack: use Container json config and not docker-py python args
        start_url = client._url('/containers/%s/start' % container['Id'])
        client._post_json(start_url, data=args['Container'])

        # Response
        self.set_header('Content-Type', 'application/json')
        self.write({'Id': container['Id'], 'Node': node['Addr']})


class Container(web.RequestHandler):

    def delete(self, pk):

        # Parse arguments
        args = json.loads(self.request.body)
        node = args['Node']
        host = node['Addr'].replace('http', 'tcp')
        force = args['Force']

        # Delete container
        client = docker.Client(base_url=host)
        client.remove_container(pk, force=force)

        # Response
        self.set_status(204)
        self.finish()


def main():

    # Command
    parser = argparse.ArgumentParser(description='Swarm Scheduler example')
    parser.add_argument(
        '--host', default='127.0.0.1:8888',
        help="Host to listen. Default 127.0.0.1:8888")
    parser.add_argument(
        '--debug', action='store_false', help="Server debug mode")
    args = parser.parse_args()

    app = web.Application([
        (r'/containers/create', CreateContainer),
        (r'/containers/(?P<pk>\w+)', Container),
    ], debug=args.debug)
    host, port = args.host.split(':')
    app.listen(port=int(port), address=host)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
