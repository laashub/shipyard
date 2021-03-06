# Copyright 2017 AT&T Intellectual Property.  All other rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
from unittest import mock

from shipyard_client.api_client.base_client import BaseClient
from shipyard_client.api_client.shipyard_api_client import ShipyardClient
from shipyard_client.api_client.shipyardclient_context import \
    ShipyardClientContext


def replace_get_endpoint(self):
    """Fake get endpoint method to isolate testing"""
    return 'http://shipyard/api/v1.0'


def replace_post_rep(self, url, query_params={}, data={}, content_type=''):
    """Replaces call to shipyard client

    :returns: dict with url and parameters
    """
    return {'url': url, 'params': query_params, 'data': data}


def replace_get_resp(self, url, query_params={}, json=False):
    """Replaces call to shipyard client.

    :returns: dict with url and parameters
    """
    return {'url': url, 'params': query_params}


def get_api_client():
    """
    get a instance of shipyard client
    :returns: shipyard client with no context object
    """
    keystone_auth = {
        'project_domain_name': 'projDomainTest',
        'user_domain_name': 'userDomainTest',
        'project_name': 'projectTest',
        'username': 'usernameTest',
        'password': 'passwordTest',
        'auth_url': 'urlTest'
    },

    context = ShipyardClientContext(
        debug=True,
        keystone_auth=keystone_auth,
        context_marker='88888888-4444-4444-4444-121212121212')
    return ShipyardClient(context)


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_post_config_docs(*args):
    shipyard_client = get_api_client()
    buffermode = 'rejectoncontents'
    result = shipyard_client.post_configdocs('ABC', buffer_mode=buffermode)
    params = result['params']
    assert result['url'] == '{}/configdocs/ABC'.format(
        shipyard_client.get_endpoint())
    assert params['buffermode'] == buffermode


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_get_config_docs(*args):
    shipyard_client = get_api_client()
    version = 'buffer'
    result = shipyard_client.get_configdocs('ABC', version=version)
    params = result['params']
    assert result['url'] == '{}/configdocs/ABC'.format(
        shipyard_client.get_endpoint())
    assert params['version'] == version


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_get_configdocs_status(*args):
    shipyard_client = get_api_client()
    result = shipyard_client.get_configdocs_status()
    assert result['url'] == '{}/configdocs'.format(
        shipyard_client.get_endpoint())


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_rendered_config_docs(*args):
    shipyard_client = get_api_client()
    version = 'buffer'
    result = shipyard_client.get_rendereddocs(version=version)
    params = result['params']
    assert result['url'] == '{}/renderedconfigdocs'.format(
        shipyard_client.get_endpoint())
    assert params['version'] == version


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_commit_configs(*args):
    shipyard_client = get_api_client()
    force_mode = True
    dryrun_mode = True
    result = shipyard_client.commit_configdocs(force_mode, dryrun_mode)
    params = result['params']
    assert result['url'] == '{}/commitconfigdocs'.format(
        shipyard_client.get_endpoint())
    assert params['force'] == force_mode
    assert params['dryrun'] == dryrun_mode


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_get_actions(*args):
    shipyard_client = get_api_client()
    result = shipyard_client.get_actions()
    assert result['url'] == '{}/actions'.format(shipyard_client.get_endpoint())


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_post_actions(*args):
    shipyard_client = get_api_client()
    name = 'good action'
    parameters = {'hello': 'world'}
    result = shipyard_client.post_actions(name, parameters)
    data = json.loads(result['data'])
    assert result['url'] == '{}/actions'.format(shipyard_client.get_endpoint())
    assert data['name'] == name
    assert data['parameters']['hello'] == 'world'


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_action_details(*args):
    shipyard_client = get_api_client()
    action_id = 'GoodAction'
    result = shipyard_client.get_action_detail(action_id)
    assert result['url'] == '{}/actions/{}'.format(
        shipyard_client.get_endpoint(), action_id)


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_get_val_details(*args):
    shipyard_client = get_api_client()
    action_id = 'GoodAction'
    validation_id = 'Validation'
    result = shipyard_client.get_validation_detail(action_id, validation_id)
    assert result['url'] == '{}/actions/{}/validations/{}'.format(
        shipyard_client.get_endpoint(), action_id, validation_id)


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_get_step_details(*args):
    shipyard_client = get_api_client()
    action_id = 'GoodAction'
    step_id = 'TestStep'
    result = shipyard_client.get_step_detail(action_id, step_id)
    assert result['url'] == '{}/actions/{}/steps/{}'.format(
        shipyard_client.get_endpoint(), action_id, step_id)


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_post_control(*args):
    shipyard_client = get_api_client()
    action_id = 'GoodAction'
    control_verb = 'Control'
    result = shipyard_client.post_control_action(action_id, control_verb)
    assert result['url'] == '{}/actions/{}/control/{}'.format(
        shipyard_client.get_endpoint(), action_id, control_verb)


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_get_note_details(*args):
    shipyard_client = get_api_client()
    note_id = "ABC123ABC123ZZABC123ABC123"
    result = shipyard_client.get_note_details(note_id)
    assert result['url'] == '{}/notedetails/{}'.format(
        shipyard_client.get_endpoint(), note_id)


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_get_workflows(*args):
    shipyard_client = get_api_client()
    since_mode = 'TestSince'
    result = shipyard_client.get_workflows(since_mode)
    assert result['url'] == '{}/workflows'.format(
        shipyard_client.get_endpoint())

    params = result['params']
    assert 'since' in params


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_get_dag_details(*args):
    shipyard_client = get_api_client()
    workflow_id = 'TestWorkflow'
    result = shipyard_client.get_dag_detail(workflow_id)
    assert result['url'] == '{}/workflows/{}'.format(
        shipyard_client.get_endpoint(), workflow_id)


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_get_step_log(*args):
    shipyard_client = get_api_client()
    action_id = '01C9VVQSCFS7V9QB5GBS3WFVSE'
    step_id = 'action_xcom'
    try_number = '2'
    result = shipyard_client.get_step_log(action_id, step_id, try_number)
    params = result['params']
    assert result['url'] == '{}/actions/{}/steps/{}/logs'.format(
        shipyard_client.get_endpoint(), action_id, step_id)
    assert params['try'] == try_number


@mock.patch.object(BaseClient, 'post_resp', replace_post_rep)
@mock.patch.object(BaseClient, 'get_resp', replace_get_resp)
@mock.patch.object(BaseClient, 'get_endpoint', replace_get_endpoint)
def test_get_site_statuses(*args):
    shipyard_client = get_api_client()
    fltrs = 'nodes-provision-status,machines-power-state'
    result = shipyard_client.get_site_statuses(fltrs=fltrs)
    params = result['params']
    assert result['url'] == '{}/site_statuses'.format(
        shipyard_client.get_endpoint())
    assert params['filters'] == fltrs
