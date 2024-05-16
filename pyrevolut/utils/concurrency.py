from typing import Awaitable, TypeVar, Any
import asyncio

T = TypeVar("T")


CONCURRENT = True


async def execute_async_group(
    tasks_list: list[Awaitable[T]] | None = None,
    tasks_dict: dict[str, Awaitable[T]] | None = None,
    concurrent: bool | None = None,
    raise_exceptions: bool = True,
) -> list[T | BaseException] | dict[str, T | BaseException]:
    """Method to execute a list of async tasks in concurrently or sequentially. If
    an error occurs, the first exception will be raised.

    Parameters
    ----------
    tasks_list : list[Awaitable[T]], optional
        List of async tasks to execute.
    tasks_dict : dict[str, Awaitable[T]], optional
        Dict of async tasks to execute.
    concurrent : bool, optional
        If True, execute tasks in concurrently, else execute sequentially.
        If None, will use the default concurrency settings.
    raise_exceptions : bool, optional
        If True, raise the first exception that occurs. If False, continue
        with all tasks and return the exception in the results.

    Returns
    -------
    list[R] | dict[str, R]
        List or Dict of results from the async tasks.
    """
    if concurrent is None:
        concurrent = CONCURRENT

    results_list: list[T | BaseException] = []
    results_dict: dict[str, T | BaseException] = {}
    exception_to_raise = None
    if concurrent:
        if tasks_list is not None:
            results_list = await asyncio.gather(*tasks_list, return_exceptions=True)
            for res in results_list:
                if isinstance(res, Exception):
                    exception_to_raise = res
                    break
        elif tasks_dict is not None:
            results_dict = {
                key: value
                for key, value in zip(
                    tasks_dict.keys(),
                    await asyncio.gather(*tasks_dict.values(), return_exceptions=True),
                )
            }
            for res in results_dict.values():
                if isinstance(res, Exception):
                    exception_to_raise = res
                    break
            # try:
            #     async with asyncio.TaskGroup() as tg:
            #         new_tasks = {
            #             key: tg.create_task(task) for key, task in tasks_dict.items()
            #         }
            #     results = {key: task.result() for key, task in new_tasks.items()}
            # except* Exception as exc:
            #     exception_to_raise = exc.exceptions[0]
    else:
        if tasks_list is not None:
            results_list = []
            for task in tasks_list:
                try:
                    results_list.append(await task)
                except Exception as exc:
                    if exception_to_raise is None:
                        exception_to_raise = exc
        elif tasks_dict is not None:
            results_dict = {}
            for key, task in tasks_dict.items():
                try:
                    results_dict[key] = await task
                except Exception as exc:
                    if exception_to_raise is None:
                        exception_to_raise = exc

    # Raise first exception (if any)
    if exception_to_raise is not None and raise_exceptions:
        raise exception_to_raise

    if tasks_list is not None:
        return results_list
    elif tasks_dict is not None:
        return results_dict
    else:
        raise ValueError("Either tasks_list or tasks_dict must be provided")


async def empty_async(return_value: Any = None):
    """
    A coroutine that returns the inputted return_value.

    Parameters
    ----------
    return_value: Any
        The value to return.

    Returns
    -------
    Any
        The inputted return_value.
    """
    return return_value
