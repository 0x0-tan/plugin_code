
# -*- coding: utf-8 -*-
from functools import partial

from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from pipeline.core.flow.activity import Service
from pipeline.core.flow.io import StringItemSchema, ArrayItemSchema, IntItemSchema, ObjectItemSchema
from pipeline.component_framework.component import Component

from gcloud.conf import settings
from gcloud.utils.handlers import handle_api_error

__group_name__ = 'CC'  #插件所属平台
get_client_by_user = settings.ESB_GET_CLIENT_BY_USER
new_handle_api_error = partial(handle_api_error, __group_name__)


class CcListBizHostsService(Service): #后台执行逻辑
    def inputs_format(self): #输入参数定义
        return []

    def outputs_format(self): #输出参数定于
        return []

    def execute(self, data, parent_data): #标准插件执行逻辑
        executor = parent_data.get_one_of_inputs('executor')

        client = get_client_by_user(executor)
        if parent_data.get_one_of_inputs('language'):
            setattr(client, 'language', parent_data.get_one_of_inputs('language'))
            translation.activate(parent_data.get_one_of_inputs('language'))

        kwargs = data.get_inputs()
        result = client.cc.list_biz_hosts(kwargs)
        if result['result']: #结果分析，输出
            return True
        else:
            message = new_handle_api_error('cc.list_biz_hosts', kwargs, result)
            self.logger.error(message)
            data.set_outputs('ex_data', message)
            return False


class CcListBizHostsComponent(Component):#前后端服务绑定
    name = 'cc_list_biz_hosts'
    code = 'cc_list_biz_hosts'
    bound_service = CcListBizHostsService
    form = '%scomponents/atoms/cc/list_biz_hosts.js' % settings.STATIC_URL

