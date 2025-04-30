from __future__ import annotations
# [BEGIN] Import modules
import importlib.util
file_path = "/opt/airflow/plugins/event_listener.py"
spec = importlib.util.spec_from_file_location("event_listener", file_path)
event_listener = importlib.util.module_from_spec(spec)
spec.loader.exec_module(event_listener)
# [END] Import modules
from airflow.plugins_manager import AirflowPlugin

class MetadataCollectionPlugin(AirflowPlugin):
    name = "MetadataCollectionPlugin"
    listeners = [event_listener]