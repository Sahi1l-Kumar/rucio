# Copyright European Organization for Nuclear Research (CERN) since 2012
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from json import dumps, loads
from typing import TYPE_CHECKING, Optional, Union
from urllib.parse import quote_plus

from requests.status_codes import codes

from rucio.client.baseclient import BaseClient, choice
from rucio.common.utils import build_url

if TYPE_CHECKING:
    from rucio.db.sqla.constants import KeyType


class MetaConventionClient(BaseClient):

    """Metadata client class for working with data identifier attributes"""

    META_BASEURL = 'meta_conventions'

    def add_key(self, key: str, key_type: Union['KeyType', str], value_type: Optional[str] = None, value_regexp: Optional[str] = None) -> Optional[bool]:
        """
        Sends the request to add an allowed key for DID metadata (update the DID Metadata Conventions table with a new key).

        :param key: the name for the new key.
        :param key_type: the type of the key: all(container, dataset, file), collection(dataset or container), file, derived(compute from file for collection).
        :param value_type: the type of the value, if defined.
        :param value_regexp: the regular expression that values should match, if defined.

        :return: True if key was created successfully.
        :raises Duplicate: if key already exists.
        """

        path = '/'.join([self.META_BASEURL, quote_plus(key)])
        url = build_url(choice(self.list_hosts), path=path)
        data = dumps({'value_type': value_type and str(value_type),
                      'value_regexp': value_regexp,
                      'key_type': key_type})

        r = self._send_request(url, type_='POST', data=data)

        if r.status_code == codes.created:
            return True
        else:
            exc_cls, exc_msg = self._get_exception(headers=r.headers, status_code=r.status_code, data=r.content)
            raise exc_cls(exc_msg)

    def list_keys(self) -> Optional[list[str]]:
        """
        Sends the request to list all keys for DID Metadata Conventions.

        :return: a list containing the names of all keys.
        """
        path = self.META_BASEURL + '/'
        url = build_url(choice(self.list_hosts), path=path)
        r = self._send_request(url)
        if r.status_code == codes.ok:
            keys = loads(r.text)
            return keys
        else:
            exc_cls, exc_msg = self._get_exception(headers=r.headers, status_code=r.status_code, data=r.content)
            raise exc_cls(exc_msg)

    def list_values(self, key: str) -> Optional[list[str]]:
        """
        Sends the request to lists all allowed values for a DID key (all values for a key in DID Metadata Conventions).
.

        :return: a list containing the names of all values for a key.
        """
        path = '/'.join([self.META_BASEURL, quote_plus(key)]) + '/'
        url = build_url(choice(self.list_hosts), path=path)
        r = self._send_request(url)
        if r.status_code == codes.ok:
            values = loads(r.text)
            return values
        else:
            exc_cls, exc_msg = self._get_exception(headers=r.headers, status_code=r.status_code, data=r.content)
            raise exc_cls(exc_msg)

    def add_value(self, key: str, value: str) -> Optional[bool]:
        """
        Sends the request to add a value for a key in DID Metadata Convention.

        :param key: the name for key.
        :param value: the value.

        :return: True if value was created successfully.
        :raises Duplicate: if valid already exists.
        """

        path = '/'.join([self.META_BASEURL, quote_plus(key)]) + '/'
        data = dumps({'value': value})
        url = build_url(choice(self.list_hosts), path=path)
        r = self._send_request(url, type_='POST', data=data)
        if r.status_code == codes.created:
            return True
        else:
            exc_cls, exc_msg = self._get_exception(headers=r.headers, status_code=r.status_code, data=r.content)
            raise exc_cls(exc_msg)

    def del_value(self, key, value):
        """
        Delete a key in the DID Metadata Conventions table.

        :param key: the name for key.
        :param value: the value.
        """
        pass

    def del_key(self, key):
        """
        Delete an allowed key.

        :param key: the name for key.
        """
        pass

    def update_key(self, key, type_=None, regexp=None):
        """
        Update a key.

        :param key: the name for key.
        :param type_: the type of the value, if defined.
        :param regexp: the regular expression that values should match, if defined.
        """
        pass
