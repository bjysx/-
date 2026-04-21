"""
操作日志工具类
"""
from .models import OperationLog


class LogManager:
    """操作日志管理器"""
    
    @staticmethod
    def log_login(user, ip_address=None, user_agent=None, status='success', message=''):
        """记录登录日志"""
        return OperationLog.objects.create(
            user=user,
            action='LOGIN',
            module='系统',
            description=f'用户 {user.username} 登录系统',
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
            message=message
        )
    
    @staticmethod
    def log_logout(user, ip_address=None, user_agent=None):
        """记录登出日志"""
        return OperationLog.objects.create(
            user=user,
            action='LOGOUT',
            module='系统',
            description=f'用户 {user.username} 退出系统',
            ip_address=ip_address,
            user_agent=user_agent,
            status='success'
        )
    
    @staticmethod
    def log_create(user, module, object_type, object_id, object_name, details=None, ip_address=None):
        """记录创建操作"""
        return OperationLog.objects.create(
            user=user,
            action='CREATE',
            module=module,
            object_type=object_type,
            object_id=str(object_id) if object_id else None,
            object_name=object_name,
            description=f'创建{object_type}: {object_name}',
            details=details,
            ip_address=ip_address,
            status='success'
        )
    
    @staticmethod
    def log_update(user, module, object_type, object_id, object_name, details=None, ip_address=None):
        """记录更新操作"""
        return OperationLog.objects.create(
            user=user,
            action='UPDATE',
            module=module,
            object_type=object_type,
            object_id=str(object_id) if object_id else None,
            object_name=object_name,
            description=f'更新{object_type}: {object_name}',
            details=details,
            ip_address=ip_address,
            status='success'
        )
    
    @staticmethod
    def log_delete(user, module, object_type, object_id, object_name, details=None, ip_address=None):
        """记录删除操作"""
        return OperationLog.objects.create(
            user=user,
            action='DELETE',
            module=module,
            object_type=object_type,
            object_id=str(object_id) if object_id else None,
            object_name=object_name,
            description=f'删除{object_type}: {object_name}',
            details=details,
            ip_address=ip_address,
            status='success'
        )
    
    @staticmethod
    def log_view(user, module, object_type, object_id=None, object_name=None, ip_address=None):
        """记录查看操作"""
        description = f'查看{object_type}'
        if object_name:
            description += f': {object_name}'
        return OperationLog.objects.create(
            user=user,
            action='VIEW',
            module=module,
            object_type=object_type,
            object_id=str(object_id) if object_id else None,
            object_name=object_name,
            description=description,
            ip_address=ip_address,
            status='success'
        )
    
    @staticmethod
    def log_export(user, module, object_type, description, ip_address=None):
        """记录导出操作"""
        return OperationLog.objects.create(
            user=user,
            action='EXPORT',
            module=module,
            object_type=object_type,
            description=description,
            ip_address=ip_address,
            status='success'
        )
    
    @staticmethod
    def log_import(user, module, object_type, description, ip_address=None):
        """记录导入操作"""
        return OperationLog.objects.create(
            user=user,
            action='IMPORT',
            module=module,
            object_type=object_type,
            description=description,
            ip_address=ip_address,
            status='success'
        )
    
    @staticmethod
    def log_upload(user, module, file_name, description, ip_address=None):
        """记录文件上传操作"""
        return OperationLog.objects.create(
            user=user,
            action='UPLOAD',
            module=module,
            object_name=file_name,
            description=description,
            ip_address=ip_address,
            status='success'
        )
    
    @staticmethod
    def log_download(user, module, file_name, description, ip_address=None):
        """记录文件下载操作"""
        return OperationLog.objects.create(
            user=user,
            action='DOWNLOAD',
            module=module,
            object_name=file_name,
            description=description,
            ip_address=ip_address,
            status='success'
        )
    
    @staticmethod
    def log_error(user, module, action, description, message, ip_address=None):
        """记录错误日志"""
        return OperationLog.objects.create(
            user=user,
            action=f'ERROR_{action}',
            module=module,
            description=description,
            message=message,
            ip_address=ip_address,
            status='failed'
        )


def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """获取用户代理信息"""
    return request.META.get('HTTP_USER_AGENT', '')


# 便捷函数，用于快速记录操作日志
def log_operation(user, action, module, description, **kwargs):
    """
    记录操作日志的便捷函数
    
    参数:
        user: 用户对象
        action: 操作类型 (LOGIN, LOGOUT, CREATE, UPDATE, DELETE, VIEW, etc.)
        module: 模块名称
        description: 操作描述
        **kwargs: 其他可选参数 (object_type, object_id, object_name, details, ip_address, etc.)
    """
    return OperationLog.objects.create(
        user=user,
        action=action,
        module=module,
        description=description,
        **kwargs
    )
