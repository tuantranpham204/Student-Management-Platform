import functools
from tkinter import messagebox
from typing import Any, Callable


def handle_exceptions(default_return_value: Any = None) -> Callable:
    """
    A decorator for UI functions that call service methods.
    It catches exceptions and displays them in a Tkinter error messagebox.

    Args:
        default_return_value: The value to return if an exception occurs
                             (e.g., [] for functions that return lists,
                             None for functions that return a single object).
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                # Try to execute the original function (e.g., your button click handler)
                return func(*args, **kwargs)
            except Exception as e:
                # If any exception "bubbles up" from the service, catch it
                # and display it in a user-friendly error box.
                error_message = f"An unexpected error occurred:\n\n{type(e).__name__}: {e}"
                messagebox.showerror("Application Error", error_message)

                # Return the specified default value so the UI doesn't crash
                return default_return_value

        return wrapper

    return decorator
