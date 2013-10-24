# Copyright (c) 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

import ddt
import falcon
from falcon import testing

import base  # noqa


@ddt.ddt
class TestWSGIMediaType(base.TestBase):

    config_filename = 'wsgi_sqlite.conf'

    @ddt.data(
        ('GET', '/v1/queues'),
        ('GET', '/v1/queues/nonexistent/metadata'),
        ('GET', '/v1/queues/nonexistent/stats'),
        ('POST', '/v1/queues/nonexistent/messages'),
        ('GET', '/v1/queues/nonexistent/messages/deadbeaf'),
        ('POST', '/v1/queues/nonexistent/claims'),
        ('GET', '/v1/queues/nonexistent/claims/0ad'),
        ('GET', '/v1/health'),
    )
    def test_json_only_endpoints(self, (method, endpoint)):
        headers = {
            'Client-ID': str(uuid.uuid4()),
            'Accept': 'application/xml',
        }

        env = testing.create_environ(endpoint,
                                     method=method,
                                     headers=headers)

        self.app(env, self.srmock)
        self.assertEqual(self.srmock.status, falcon.HTTP_406)