from __future__ import annotations

import requests
import datetime
import types
import enum

from typing import TYPE_CHECKING
from typing import Any, Dict

from airflow.listeners import hookimpl
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import DagRunState, TaskInstanceState
from airflow.sdk.execution_time.task_runner import RuntimeTaskInstance

if TYPE_CHECKING:
    from airflow.models.dagrun import DagRun

API_BASE_ENDPOINT = "http://airflow-api-logger.airflow.svc.cluster.local:8000"
API_DAG_RUN_ENDPOINT = f"{API_BASE_ENDPOINT}/api/v1/airflow_v3/events/dag_run"
API_TASK_INSTANCE_ENDPOINT = f"{API_BASE_ENDPOINT}/api/v1/airflow_v3/events/task_instance"

PRIMITIVE_TYPES = (str, int, float, bool, type(None))

def instance_to_dict(instance: DagRun) -> Dict[str, Any]:
    result_dict = {}

    def process_value(value: Any) -> Any:
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        elif isinstance(value, datetime.date):
            return value.isoformat()
        elif isinstance(value, PRIMITIVE_TYPES) or isinstance(value, enum.Enum):
             if isinstance(value, enum.Enum):
                 return value.value if hasattr(value, 'value') else str(value)
             else:
                return value
        else:
            try:
                return str(value)
            except Exception as e:
                print(f"Warning: Could not convert value {value} to string: {e}")
                return None

    print("Warning: Input object doesn't look like a standard SQLAlchemy model instance. Falling back to vars().")
    try:
        for k, v in vars(instance).items():
            if not k.startswith('_') and not isinstance(v, types.MethodType) and not callable(v):
                result_dict[k] = process_value(v)
        return result_dict
    except TypeError:
         print("Error: Could not process the input object using vars().")
         return {}


def serialize_runtime_task_instance(
    task_instance: RuntimeTaskInstance,
    previous_state: TaskInstanceState,
    new_state: TaskInstanceState,
    error_message: str | None = None,
) -> dict:
    """
    Serialize the tsk instance to a dictionary.
    """
    payload = instance_to_dict(task_instance)
    payload["previous_state"] = previous_state
    payload["state"] = new_state
    payload["error_message"] = str(error_message) if error_message is not None else None
    return payload


def serialize_task_instance(
    task_instance: RuntimeTaskInstance | TaskInstance,
    previous_state: TaskInstanceState,
    new_state: TaskInstanceState,
    error_message: str | None = None,
) -> dict:
    """
    Serialize the task instance to a dictionary.
    """
    payload = instance_to_dict(task_instance)
    payload["previous_state"] = previous_state
    payload["state"] = new_state
    payload["error_message"] = str(error_message) if error_message is not None else None
    return payload

def send_task_instance_state(
    task_instance: RuntimeTaskInstance | TaskInstance,
    previous_state: TaskInstanceState,
    new_state: TaskInstanceState,
    error_message: str | None = None,
) -> int:
    """
    Send the task instance to the API.
    """
    payload = serialize_task_instance(task_instance, previous_state, new_state, error_message)
    response = requests.post(
        API_TASK_INSTANCE_ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json=payload,
    )

    if 200 <= response.status_code < 300:
        return response.status_code
    else:
        print(f"Payload: {payload}")
        raise Exception(
            f"Failed to send task instance state. Status code: {response.status_code}, Response: {response.text}"
        )


def serialize_dag_run(
    dag_run: DagRun,
    new_state: DagRunState,
    error_message: str | None = None,
) -> dict:
    payload = instance_to_dict(dag_run)
    payload["state"] = new_state
    payload["error_message"] = str(error_message) if error_message is not None else None
    return payload


def send_dag_run_state(
    dag_run: DagRun,
    new_state: DagRunState,
    error_message: str | None = None,
) -> bool:
    payload = serialize_dag_run(dag_run, new_state, error_message)
    response = requests.post(
        API_DAG_RUN_ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json=payload,
    )
    if 200 <= response.status_code < 300:
        return response.status_code
    else:
        print(f"Payload: {payload}")
        raise Exception(
            f"Failed to send task instance state. Status code: {response.status_code}, Response: {response.text}"
        )


@hookimpl
def on_task_instance_running(
    previous_state: TaskInstanceState, task_instance: RuntimeTaskInstance
):
    new_state = TaskInstanceState.RUNNING
    if isinstance(task_instance, RuntimeTaskInstance):
        context = task_instance.get_template_context()
        send_task_instance_state(
            task_instance=context["task_instance"],
            previous_state=previous_state,
            new_state=new_state,
        )
    elif isinstance(task_instance, TaskInstance):
        send_task_instance_state(
            task_instance=task_instance,
            previous_state=previous_state,
            new_state=new_state,
        )
    else:
        raise TypeError(
            f"Expected RuntimeTaskInstance or TaskInstance, got {type(task_instance)}"
        )

@hookimpl
def on_task_instance_success(
    previous_state: TaskInstanceState, task_instance: RuntimeTaskInstance | TaskInstance
):
    new_state = TaskInstanceState.SUCCESS
    if isinstance(task_instance, RuntimeTaskInstance):
        context = task_instance.get_template_context()
        send_task_instance_state(
            task_instance=context["task_instance"],
            previous_state=previous_state,
            new_state=new_state,
        )
    elif isinstance(task_instance, TaskInstance):
        send_task_instance_state(
            task_instance=task_instance,
            previous_state=previous_state,
            new_state=new_state,
        )
    else:
        raise TypeError(
            f"Expected RuntimeTaskInstance or TaskInstance, got {type(task_instance)}"
        )

@hookimpl
def on_task_instance_failed(
    previous_state: TaskInstanceState,
    task_instance: RuntimeTaskInstance | TaskInstance,
    error: None | str | BaseException,
):
    new_state = TaskInstanceState.FAILED
    if isinstance(task_instance, RuntimeTaskInstance):
        context = task_instance.get_template_context()
        send_task_instance_state(
            task_instance=context["task_instance"],
            previous_state=previous_state,
            new_state=new_state,
            error_message=str(error),
        )
    elif isinstance(task_instance, TaskInstance):
        send_task_instance_state(
            task_instance=task_instance,
            previous_state=previous_state,
            new_state=new_state,
            error_message=str(error),
        )
    else:
        raise TypeError(
            f"Expected RuntimeTaskInstance or TaskInstance, got {type(task_instance)}"
        )

@hookimpl
def on_dag_run_success(dag_run: DagRun, msg: str):
    send_dag_run_state(
        dag_run=dag_run,
        new_state=DagRunState.SUCCESS,
    )


@hookimpl
def on_dag_run_failed(dag_run: DagRun, msg: str):
    send_dag_run_state(
        dag_run=dag_run,
        new_state=DagRunState.FAILED,
        error_message=msg,
    )

@hookimpl
def on_dag_run_running(dag_run: DagRun, msg: str):
    send_dag_run_state(
        dag_run=dag_run,
        new_state=DagRunState.RUNNING,
    )

