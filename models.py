#!/usr/bin/env python
# -*- coding=utf-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Mock 服务器
class MockServer(Base):
    # table name
    __tablename__ = 'mock_server'

    # table columns
    mock_server_id = Column(Integer, primary_key=True)
    mock_server_name = Column(String(50), nullable=True)
    mock_server_ip = Column(String(15), nullable=True)
    mock_server_port = Column(Integer, nullable=False)
    mock_server_protocol = Column(String(20), nullable=True)
    mock_server_desc = Column(String(20), nullable=True)
    is_enabled = Column(String(1), nullable=True)
    mock_server_status = Column(String(1), nullable=True)

    def __repr__(self):
        return "<MockServer('%s')>" % (self.mock_server_name)

# Mock 服务
class MockService(Base):
    # table name
    __tablename__ = 'mock_service'

    # table columns
    mock_service_id = Column(Integer, primary_key=True)
    mock_server_id = Column(Integer, ForeignKey('mock_server.mock_server_id'))
    mock_service_name = Column(String(50), nullable=True)
    mock_service_uri = Column(String(100), nullable=True)
    mock_service_action = Column(String(20), nullable=True)
    mock_service_type = Column(String(20), nullable=True)
    mock_service_request = Column(String(1000), nullable=True)
    mock_service_response_for_success = Column(String(1000), nullable=True)
    mock_service_response_for_failed = Column(String(1000), nullable=True)
    mock_service_rollback = Column(String(100), nullable=True)
    is_successful = Column(String(1), nullable=True)
    is_enabled = Column(String(1), nullable=True)

    def __repr__(self):
        return "<MockService('%s')>" % (self.mock_service_name)
