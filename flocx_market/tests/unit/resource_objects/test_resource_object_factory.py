import pytest
import unittest.mock as mock

from flocx_market.common import exception
from flocx_market.resource_objects import resource_object_factory
from flocx_market.resource_objects import resource_types


@mock.patch('flocx_market.resource_objects.ironic_node.IronicNode')
def test_resource_object_factory_ironic(ironic_node):
    resource_object_factory.ResourceObjectFactory.get_resource_object(
        resource_types.IRONIC_NODE,
        '1234'
    )
    ironic_node.assert_called_once_with('1234')


@mock.patch('flocx_market.resource_objects.dummy_node.DummyNode')
def test_resource_object_factory_dummy(dummy_node):
    resource_object_factory.ResourceObjectFactory.get_resource_object(
        resource_types.DUMMY_NODE,
        '1234'
    )
    dummy_node.assert_called_once_with('1234')


def test_resource_object_factory_bad_type():
    with pytest.raises(exception.ResourceTypeUnknown):
        assert resource_object_factory \
            .ResourceObjectFactory.get_resource_object(
                'BAD-NODE-TYPE',
                '1234'
            )
