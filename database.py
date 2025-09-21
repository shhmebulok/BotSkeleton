# DATABASE

# ---------------------------------------------------------------------------------------------------------------------
# import libraries
import ast
import json
import time
from typing import List, Optional, TypeVar, Generic, Type


from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.sqltypes import BigInteger

import config
from log_functions import log_error

# ---------------------------------------------------------------------------------------------------------------------
# Configuration

DATABASE_URL = "sqlite:///database/db.sqlite3"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True)
Session = scoped_session(sessionmaker(bind=engine))

# Base Model
T = TypeVar('T', bound='BaseModel')


# ---------------------------------------------------------------------------------------------------------------------

class BaseModel(Base, Generic[T]):
    __abstract__ = True

    @declared_attr
    def id(cls):
        if 'id' not in cls.__dict__:
            return Column(BigInteger, primary_key=True, autoincrement=True)

    @classmethod
    def get(cls: Type[T], pk: object) -> Optional[T]:
        session = Session()
        try:
            instance = session.query(cls).get(pk)
            if instance:
                cls._process_json_columns(instance)
            return instance
        except OperationalError as e:
            log_error(e)
            time.sleep(3)  # Wait before retrying
            return cls.get(pk)
        except Exception as e:
            log_error(e)
        finally:
            session.close()
        return None

    @classmethod
    def _process_json_columns(cls, instance: T):
        for column in instance.__table__.columns:
            try:
                if isinstance(column.type, JSON):
                    data = getattr(instance, column.name)
                    if data is None:
                        setattr(instance, column.name, {})
                    elif isinstance(data, str):
                        data = data.replace('null', 'None')
                        setattr(instance, column.name, eval(data))

            except Exception as e:
                log_error(e)

    @classmethod
    def _process_json_columns_for_list(cls, instances: List[T]):
        for instance in instances:
            cls._process_json_columns(instance)

    @classmethod
    def filter(cls: Type[T], *args, **kwargs) -> List[T]:
        session = Session()
        try:
            instances = session.query(cls).filter(*args, **kwargs).all()
            cls._process_json_columns_for_list(instances)
            return instances
        except OperationalError as e:
            log_error(e)
            time.sleep(3)  # Wait before retrying
            return cls.filter(*args, **kwargs)
        except Exception as e:
            log_error(e)
        finally:
            session.close()
        return []

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        session = Session()
        try:
            instances = session.query(cls).all()
            cls._process_json_columns_for_list(instances)
            return instances
        except OperationalError as e:
            log_error(e)
            time.sleep(3)  # Wait before retrying
            return cls.all()
        except Exception as e:
            log_error(e)
        finally:
            session.close()
        return []

    @classmethod
    def values(cls: Type[T], *columns):
        session = Session()
        try:
            results = session.query(*columns).all()
            processed_results = []
            for row in results:
                processed_row = []
                for column, value in zip(columns, row):
                    if isinstance(column.type, JSON):
                        if isinstance(value, str):
                            try:
                                value = ast.literal_eval(value)
                            except Exception as e:
                                log_error(e)
                        elif value is None:
                            value = {}
                    processed_row.append(value)
                processed_results.append(tuple(processed_row))
            return processed_results
        except OperationalError as e:
            log_error(e)
            time.sleep(3)  # Wait before retrying
            return cls.values(*columns)
        except Exception as e:
            log_error(e)
        finally:
            session.close()
        return []

    def delete(self):
        session = Session()
        try:
            session.delete(self)
            session.commit()
        except OperationalError as e:
            log_error(e)
            time.sleep(3)  # Wait before retrying
            self.delete()
        except Exception as e:
            log_error(e)
        finally:
            session.close()

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        instance = cls(**kwargs)
        return instance.save()

    def save(self) -> T:
        session = Session()
        try:
            self._convert_dicts_to_json_strings()
            session.add(self)
            session.commit()
            session.refresh(self)
            self._process_json_columns(self)
            return self
        except OperationalError as e:
            log_error(e)
            time.sleep(3)  # Wait before retrying
            return self.save()
        except Exception as e:
            log_error(e)
            session.rollback()
            raise
        finally:
            session.close()

    def _convert_dicts_to_json_strings(self):
        for column in self.__table__.columns:
            if isinstance(column.type, JSON) and isinstance(getattr(self, column.name), dict):
                setattr(self, column.name, json.dumps(getattr(self, column.name)))
