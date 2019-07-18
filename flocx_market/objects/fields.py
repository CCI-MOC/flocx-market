import ast
import six

from oslo_versionedobjects import fields as object_fields


class DateTimeField(object_fields.DateTimeField):
    def __init__(self, **kwargs):
        super(DateTimeField, self).__init__(False, **kwargs)


class FlexibleDict(object_fields.FieldType):
    @staticmethod
    def coerce(obj, attr, value):
        if isinstance(value, six.string_types):
            value = ast.literal_eval(value)
        return dict(value)


class FlexibleDictField(object_fields.AutoTypedField):
    AUTO_TYPE = FlexibleDict()

    def _null(self, obj, attr):
        if self.nullable:
            return {}
        super(FlexibleDictField, self)._null(obj, attr)


class IntegerField(object_fields.IntegerField):
    pass


class FloatField(object_fields.FloatField):
    pass


class ListOfObjectsField(object_fields.ListOfObjectsField):
    pass


class ObjectField(object_fields.ObjectField):
    pass


class StringField(object_fields.StringField):
    pass


class UUIDField(object_fields.UUIDField):
    pass
