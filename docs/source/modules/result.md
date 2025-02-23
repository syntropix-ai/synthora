<!-- LICENSE HEADER MANAGED BY add-license-header

Copyright 2024-2025 Syntropix

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Result

In the `synthora` framework, all tools and Agent return values are of the `Result` type. This unified structure ensures consistency in handling both successful outcomes and errors.

The `Result` type can represent one of two possible states:

1. **`Ok`**
2. **`Err`**

---

## **Ok**

An `Ok` result signifies a successful operation. It contains the normal return value of the operation.

### Attributes:
- **`value`**: The expected output of the operation.

### Example:
```python
result = Ok(value="Success!")
print(result.value)  # Output: Success!
```

---

## **Err**

An `Err` result indicates that an error occurred during the operation. It contains two components:
1. A human-readable **error message** (`str`) to help LLMs and developers understand the issue.
2. The **original exception** that caused the error, providing access to detailed exception information.

### Attributes:
- **`error`**: A string representation of the error message for understanding and debugging.
- **`value`**: The original exception object (`Exception`), which holds the detailed error information.

### Example:
```python
try:
    raise ValueError("Invalid input")
except ValueError as e:
    result = Err(error=str(e), value=e)

print(result.error)  # Output: Invalid input
print(result.value)  # Output: ValueError('Invalid input')
```

---

## Common Methods

### `unwrap()`
Retrieves the value from an `Ok` result. If the `Result` is `Err`, it raises a `RuntimeError`.

#### Example:
```python
result = Ok(value=42)
print(result.unwrap())  # Output: 42

err_result = Err(error="Something went wrong", value=ValueError("Error!"))
print(err_result.unwrap())  # Raises RuntimeError
```

---

### `unwrap_err()`
Retrieves the error from an `Err` result. If the `Result` is `Ok`, it raises a `RuntimeError`.

#### Example:
```python
err_result = Err(error="Something went wrong", value=ValueError("Error!"))
print(err_result.unwrap_err())  # Output: Something went wrong

ok_result = Ok(value=42)
print(ok_result.unwrap_err())  # Raises RuntimeError
```

---

### `unwrap_err_val()`
Retrieves the original exception object from an `Err` result. If the `Result` is `Ok`, it raises a `RuntimeError`.

#### Example:
```python
err_result = Err(error="Something went wrong", value=ValueError("Error!"))
print(err_result.unwrap_err_val())  # Output: ValueError('Error!')

ok_result = Ok(value=42)
print(ok_result.unwrap_err_val())  # Raises RuntimeError
```

---

## Key Properties

### `is_ok`
Returns `True` if the `Result` is an `Ok`, otherwise `False`.

### Example:
```python
result = Ok(value="Success!")
print(result.is_ok)  # Output: True

err_result = Err(error="Failed", value=Exception("Failure"))
print(err_result.is_ok)  # Output: False
```

---

### `is_err`
Returns `True` if the `Result` is an `Err`, otherwise `False`.

### Example:
```python
result = Ok(value="Success!")
print(result.is_err)  # Output: False

err_result = Err(error="Failed", value=Exception("Failure"))
print(err_result.is_err)  # Output: True
```

---

By utilizing the `Result` type, `synthora` ensures consistent handling of both successful and error states, making it easier for developers to write robust and reliable code.
