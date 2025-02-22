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

# Task

Synthora is a flexible workflow system inspired by tools like Celery, designed to orchestrate tasks in serial and parallel workflows with high customization capabilities. In this document, we will focus on **Tasks**, one of the fundamental building blocks of Synthora workflows.

---

## Task Overview

A **Task** in Synthora represents the smallest unit of execution. It can be a function or a callable object that performs a specific operation. Synthora provides multiple ways to define tasks and allows users to extend their behavior with advanced features like **signatures** and **immutability**.

---

### Defining Tasks

Tasks in Synthora can be created in two ways:

1. **Using Decorators**:
   Use the `@task` decorator to define a task with additional configurations.
   ```python
   from synthora.workflows import task

   @task
   def add(x: int, y: int) -> int:
       return x + y
   ```

2. **Using Classes**:
   Use the `BaseTask` class to define a task manually, especially when you need more control.
   ```python
   from synthora.workflows.base_task import BaseTask

   def multiply(x: int, y: int) -> int:
       return x * y

   multiply_task = BaseTask(multiply, name="multiply_task")
   ```

---

### Task Signature

**Signatures** in Synthora allow you to predefine and lock task parameters. This feature simplifies the reuse of tasks and helps build predictable workflows.

#### Predefining Task Parameters
A task signature can be used to set default arguments:
```python
add_task = add.s(1)  # Predefine the first parameter as 1
result = add_task(2)  # Executes add(1, 2) and returns 3
```

You can also achieve this using:
```python
add_task = add.signature(1)
```

#### Immutable Parameters
By default, task signatures are mutable, allowing additional arguments to be passed during execution. However, Synthora supports **immutable signatures**, ensuring the task ignores any external arguments and only uses predefined parameters.

Example:
```python
add_task = add.si(1, 2)  # Immutable signature
result = add_task(3, 3)  # The external arguments are ignored; executes add(1, 2) and returns 3
```

Alternate ways to create immutable signatures:
```python
add_task = add.signature(1, 2, immutable=True)
# or
add_task = add.signature_immutable(1, 2)
```

**Error Example**:
If a mutable signature is used and too many arguments are provided, an error is raised:
```python
try:
    add_task(1, 2, 3)  # Too many arguments
except TypeError as e:
    print(e)
# Output: add() takes 2 positional arguments but 3 were given
```

---

### Practical Examples

#### Example 1: Basic Task Execution
```python
@task
def greet(name: str) -> str:
    return f"Hello, {name}!"

greet_task = greet.s("Alice")
print(greet_task())  # Output: Hello, Alice!
```

#### Example 2: Using Signatures
```python
@task
def divide(x: int, y: int) -> float:
    return x / y

divide_task = divide.s(10)  # Predefine the numerator as 10
print(divide_task(2))  # Output: 5.0
```

#### Example 3: Immutable Parameters
```python
@task
def power(base: int, exp: int) -> int:
    return base ** exp

immutable_task = power.si(2, 3)  # Locks the parameters
print(immutable_task(4, 5))  # Output: 6 (only 2**3 is executed)
```

---

### Benefits of Task Signatures

1. **Reusability**: Signatures allow you to reuse tasks with preconfigured parameters.
2. **Consistency**: Immutable signatures ensure predictable behavior, unaffected by external inputs.
3. **Simplified Workflows**: Chaining tasks with signatures reduces boilerplate code.

Synthora’s approach to task signatures and immutability is inspired by Celery, a popular distributed task queue. However, Synthora enhances flexibility by integrating these features into a broader workflow orchestration system.

---

This concludes the first part of the Synthora documentation on **Tasks**. In subsequent sections, we will explore **Schedulers** and **Contexts**, completing the picture of how Synthora orchestrates workflows.
