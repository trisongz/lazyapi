
from lazycls.envs import *
from lazycls.utils import get_parent_path, to_path, exec_cmd, exec_daemon, find_binary_in_path, get_cwd
from .config import logger
import time

## port of internal lib used to start services
try: from redis import Redis as RedisClient
except ImportError: RedisClient = None


def require_redis():
    if RedisClient is None: raise ImportError('Redis')
    #global RedisClient
    #if RedisClient is not None: return


class RedisCfg:
    host = envToStr('REDIS_HOST', '127.0.0.1')
    port = envToInt('REDIS_PORT', 6379)
    password = envToStr('REDIS_PASS', None)
    database = envToInt('REDIS_DB', 0)
    cachedir = envToStr('REDIS_CACHEDIR', None)
    sentinel = envToBool('REDIS_SENTINEL', 'false')
    sentinel_master = envToStr('REDIS_SENTINEL_MASTER')
    fallback_enabled: bool = envToBool('REDIS_FALLBACK_ENABLED', 'true')
    local_redis: bool = envToBool('REDIS_LOCAL', 'true')
    is_deployment: bool = envToBool('REDIS_DEPLOYMENT', 'false')
    startup_delay: int = envToInt('REDIS_STARTUP_DELAY', 7)
    
    @classmethod
    def check_redis_connection(cls):
        """Doing a quick ping and then timeout. If does not connect in 5 secs, then is not fast enough."""
        require_redis()
        r = RedisClient(host=cls.host, port=cls.port, db=cls.database, password=cls.password, socket_timeout = 5.0, socket_connect_timeout = 5.0, socket_keepalive = False)
        try: return bool(r.ping())
        except: return False

    @classmethod
    def set_to_default_redis_config(cls):
        """ Changes Redis cfg to default"""
        cls.host = '127.0.0.1'
        cls.port = 6379
        cls.password = None

    @classmethod
    def set_config(cls, **kwargs):
        for k,v in kwargs.items():
            if getattr(cls, k, None):
                setattr(cls, k, v)

    @classmethod
    def get_cachedir(cls):
        d = to_path(cls.cachedir) if cls.cachedir else get_cwd('db', posix=False)
        d.mkdir(parents=True)
        return d.as_posix()

    
    @classmethod
    def ensure_local_redis(cls):
        """ Ensures that local redis is running if local_redis = true or manually called if not able to connect to external redis"""
        # Doing System Platform Check
        if not find_binary_in_path('redis-server'):
            import platform
            host_os = platform.system().lower()
            if host_os == 'darwin':
                logger.info('Installing redis-server for MacOS')
                exec_cmd('brew install redis')
            elif host_os == 'windows':
                logger.info('Sorry, I dont know windows.')
                raise
            else:
                logger.info(f'Assuming Linux:{host_os}. Installing redis with apt')
                exec_cmd('apt-get update -y && apt-get install redis-server -y')
        rstatus = exec_cmd('redis-cli ping', raise_error=False)
        if not rstatus:
            if cls.is_deployment: exec_daemon('redis-server', cwd=cls.get_cachedir(), set_proc_uid=False)
            else: exec_daemon('redis-server', cwd=cls.get_cachedir())
            time.sleep(cls.startup_delay)
        cls.set_to_default_redis_config()

    @classmethod
    def ensure_redis(cls):
        """If external redis, checks connect.
            falls back to creating internal redis.
        """
        if not cls.local_redis and cls.check_redis_connection(): return logger.info('External Redis Connection Successful')
        if not cls.fallback_enabled: raise RuntimeError('Unable to Establish Redis connection')
        if cls.local_redis:
            logger.info('Setting up Local Redis Connection')
            cls.ensure_local_redis()
            if cls.check_redis_connection(): return logger.info('Local Redis Connection Successful')
        logger.info('Unable to Establish Redis Connection')
        raise


    @classmethod
    def get_redis_cfg(cls):
        return dict(
            host = cls.host,
            port = cls.port,
            password = cls.password,
            database = cls.database,
            sentinel = cls.sentinel,
            sentinel_master = cls.sentinel_master
        )
    
