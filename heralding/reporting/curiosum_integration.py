# Copyright (C) 2018 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import heralding.misc

import logging
import zmq

from heralding.reporting.base_logger import BaseLogger

logger = logging.getLogger(__name__)


class CuriosumIntegration(BaseLogger):
    def __init__(self, zmq_socket='ipc://zmq-socket'):
        super(CuriosumIntegration, self).__init__()

        context = heralding.misc.zmq_context
        self.socket = context.socket(zmq.PUSH)
        self.socket.bind(zmq_socket)

    def loggerStopped(self):
        self.socket.close()

    def handle_auth_log(self, data):
        pass

    def handle_session_log(self, data):
        message = {
            'SessionID': data['session_id'],
            'DstPort': data['destination_port'],
            'SrcIP': data['source_ip'],
            'SrcPort': data['source_port']}
        self.socket.send_string('{0} {1}'.format('session_ended', data))