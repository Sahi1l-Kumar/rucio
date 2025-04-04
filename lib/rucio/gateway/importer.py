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

from typing import TYPE_CHECKING, Any

from rucio.common import exception
from rucio.common.schema import validate_schema
from rucio.common.types import InternalAccount
from rucio.core import importer
from rucio.db.sqla.session import transactional_session
from rucio.gateway import permission

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


@transactional_session
def import_data(data: dict[str, Any], issuer: str, vo: str = 'def', *, session: "Session") -> None:
    """
    Import data to add/update/delete records in Rucio.

    :param data: data to be imported.
    :param issuer: the issuer.
    :param vo: the VO of the issuer.
    :param session: The database session in use.
    """
    kwargs = {'issuer': issuer}
    validate_schema(name='import', obj=data, vo=vo)
    auth_result = permission.has_permission(issuer=issuer, vo=vo, action='import', kwargs=kwargs, session=session)
    if not auth_result.allowed:
        raise exception.AccessDenied('Account %s can not import data. %s' % (issuer, auth_result.message))

    for account in data.get('accounts', []):
        account['account'] = InternalAccount(account['account'], vo=vo)
    return importer.import_data(data, vo=vo, session=session)
