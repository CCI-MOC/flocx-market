from oslo_log import log
from oslo_versionedobjects import base as object_base
import datetime


LOG = log.getLogger(__name__)


class FLOCXMarketObject(object_base.VersionedObject):

    OBJ_SERIAL_NAMESPACE = 'flocx_market_object'
    OBJ_PROJECT_NAMESPACE = 'flocx_market'

    @staticmethod
    def _from_db_object(obj, db_obj):
        for key in obj.fields:
            setattr(obj, key, db_obj[key])
            obj.obj_reset_changes()
        return obj

    @classmethod
    def _from_db_object_list(cls, db_objs):
        all_objs = [cls._from_db_object(cls(), db_obj) for db_obj in db_objs]
        return all_objs

    def to_dict(self):
        ret = dict()
        for k in self.fields:
            val = getattr(self, k)
            if type(val) == datetime.datetime:
                ret[k] = val.isoformat()
            else:
                ret[k] = val
        return ret
