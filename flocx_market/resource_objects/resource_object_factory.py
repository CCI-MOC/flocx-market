#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from flocx_market.common import exception
from flocx_market.resource_objects import dummy_node
from flocx_market.resource_objects import ironic_node
from flocx_market.resource_objects import resource_types


class ResourceObjectFactory(object):

    @staticmethod
    def get_resource_object(resource_type, resource_id):
        if resource_type == resource_types.IRONIC_NODE:
            return ironic_node.IronicNode(resource_id)
        elif resource_type == resource_types.DUMMY_NODE:
            return dummy_node.DummyNode(resource_id)
        raise exception.ResourceTypeUnknown(resource_type=resource_type)
